from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from sqlalchemy.orm import Session

from app.api.auth_deps import get_current_user
from app.core.config import settings
from app.db.session import get_db
from app.ocr.ocr_processor import OCRProcessor
from app.schemas.schemas import (
    ReceiptCreate,
    ReceiptExtractResponse,
    ReceiptResponse,
    TransactionCreate,
    TransactionResponse,
)
from app.services.user_service import ReceiptService, TransactionService

router = APIRouter(prefix="/api/v1/receipts", tags=["receipts"])

ALLOWED_RECEIPT_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "application/pdf",
}


def _safe_filename(file: UploadFile) -> str:
    return Path(file.filename or "receipt").name


async def _read_upload(file: UploadFile) -> bytes:
    content_type = file.content_type or ""
    suffix = Path(file.filename or "").suffix.lower()
    if content_type not in ALLOWED_RECEIPT_TYPES and suffix not in {".jpg", ".jpeg", ".png", ".webp", ".pdf"}:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Receipt must be a JPEG, PNG, WebP, or PDF file",
        )

    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Receipt file is empty")
    if len(contents) > settings.max_upload_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Receipt exceeds {settings.MAX_UPLOAD_SIZE_MB} MB limit",
        )
    return contents


def _extract_data(file: UploadFile, contents: bytes) -> dict:
    suffix = Path(file.filename or "").suffix.lower()
    content_type = file.content_type or ""
    if content_type == "application/pdf" or suffix == ".pdf":
        text = OCRProcessor.extract_text_from_pdf(contents)
    else:
        text = OCRProcessor.extract_text_from_image(contents)
    return OCRProcessor.parse_receipt_data(text)


def _receipt_storage_url(file: UploadFile, contents: bytes) -> str:
    if (
        settings.CLOUDINARY_CLOUD_NAME
        and settings.CLOUDINARY_API_KEY
        and settings.CLOUDINARY_API_SECRET
    ):
        try:
            import cloudinary
            import cloudinary.uploader

            cloudinary.config(
                cloud_name=settings.CLOUDINARY_CLOUD_NAME,
                api_key=settings.CLOUDINARY_API_KEY,
                api_secret=settings.CLOUDINARY_API_SECRET,
                secure=True,
            )
            result = cloudinary.uploader.upload(
                contents,
                folder="finnova/receipts",
                resource_type="auto",
            )
            secure_url = result.get("secure_url")
            if secure_url:
                return secure_url
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Receipt storage provider failed",
            ) from exc

    if settings.is_production:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Receipt storage is not configured",
        )

    return f"local://receipts/{_safe_filename(file)}"


@router.post("/upload", response_model=ReceiptResponse, status_code=status.HTTP_201_CREATED)
async def upload_receipt(
    file: UploadFile = File(...),
    user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    contents = await _read_upload(file)
    image_url = _receipt_storage_url(file, contents)

    try:
        extracted_data = _extract_data(file, contents)
        receipt_status = "processed"
    except Exception:
        extracted_data = None
        receipt_status = "failed"

    return ReceiptService.create_receipt(
        db,
        user_id,
        ReceiptCreate(image_url=image_url),
        extracted_data=extracted_data,
        status=receipt_status,
    )


@router.post("/extract", response_model=ReceiptExtractResponse)
async def extract_receipt_data(
    file: UploadFile = File(...),
    user_id: UUID = Depends(get_current_user),
):
    contents = await _read_upload(file)
    try:
        return _extract_data(file, contents)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Unable to extract receipt data",
        ) from exc


@router.get("", response_model=list[ReceiptResponse])
def get_receipts(
    user_id: UUID = Depends(get_current_user),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    return ReceiptService.list_receipts(db, user_id, limit, offset)


@router.get("/{receipt_id}", response_model=ReceiptResponse)
def get_receipt(
    receipt_id: UUID,
    user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    receipt = ReceiptService.get_receipt(db, user_id, receipt_id)
    if not receipt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Receipt not found")
    return receipt


@router.post("/{receipt_id}/create-transaction", response_model=TransactionResponse)
def create_transaction_from_receipt(
    receipt_id: UUID,
    user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    receipt = ReceiptService.get_receipt(db, user_id, receipt_id)
    if not receipt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Receipt not found")

    extracted_data = receipt.extracted_data or {}
    amount = extracted_data.get("amount")
    if not amount:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Receipt does not contain an amount",
        )

    from datetime import timezone
    raw_date = extracted_data.get("date")
    try:
        transaction_date = datetime.fromisoformat(raw_date) if raw_date else datetime.now(timezone.utc)
    except ValueError:
        transaction_date = datetime.now(timezone.utc)

    merchant = extracted_data.get("merchant_name")
    transaction = TransactionService.create_transaction(
        db,
        user_id,
        TransactionCreate(
            type="expense",
            amount=float(amount),
            currency=extracted_data.get("currency") or "INR",
            category=extracted_data.get("category") or "others",
            merchant=merchant,
            description=f"Receipt from {merchant or 'merchant'}",
            date=transaction_date,
        ),
    )
    receipt.transaction_id = transaction.id
    transaction.receipt_id = receipt.id
    db.add(receipt)
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


@router.delete("/{receipt_id}")
def delete_receipt(
    receipt_id: UUID,
    user_id: UUID = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    deleted = ReceiptService.delete_receipt(db, user_id, receipt_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Receipt not found")
    return {"message": "Receipt deleted"}
