import io
import re
from datetime import datetime
from typing import Any, Dict

import pdfplumber
import pytesseract


class OCRProcessor:
    @staticmethod
    def extract_text_from_image(image_bytes: bytes) -> str:
        """Extract text from image using Tesseract OCR."""
        from PIL import Image

        image = Image.open(io.BytesIO(image_bytes))
        return pytesseract.image_to_string(image)

    @staticmethod
    def extract_text_from_pdf(pdf_bytes: bytes) -> str:
        """Extract text from PDF."""
        text = ""
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    @staticmethod
    def parse_receipt_data(text: str) -> Dict[str, Any]:
        """Parse receipt text to extract structured data."""
        data: Dict[str, Any] = {
            "merchant_name": None,
            "amount": None,
            "tax": None,
            "date": None,
            "currency": "INR",
            "items": [],
            "category": "others",
            "confidence": 0.7,
        }

        amount_pattern = r"(?:total|amount|grand\s*total)[:\s]*(?:inr|\$|rs\.?)?\s*(\d+(?:\.\d+)?)"
        amount_match = re.search(amount_pattern, text, re.IGNORECASE)
        if amount_match:
            data["amount"] = float(amount_match.group(1))

        tax_pattern = r"(?:tax|vat|gst)[:\s]*(?:inr|\$|rs\.?)?\s*(\d+(?:\.\d+)?)"
        tax_match = re.search(tax_pattern, text, re.IGNORECASE)
        if tax_match:
            data["tax"] = float(tax_match.group(1))

        date_pattern = r"(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})"
        date_match = re.search(date_pattern, text)
        if date_match:
            raw_date = date_match.group(1).replace("-", "/")
            for date_format in ("%d/%m/%Y", "%d/%m/%y", "%m/%d/%Y", "%m/%d/%y"):
                try:
                    data["date"] = datetime.strptime(raw_date, date_format).isoformat()
                    break
                except ValueError:
                    continue

        lines = [line.strip() for line in text.splitlines() if line.strip()]
        if lines:
            data["merchant_name"] = lines[0][:255]

        text_lower = text.lower()
        if any(word in text_lower for word in ["food", "restaurant", "cafe", "dining"]):
            data["category"] = "food"
        elif any(word in text_lower for word in ["uber", "taxi", "flight", "hotel"]):
            data["category"] = "travel"
        elif any(word in text_lower for word in ["amazon", "flipkart", "store", "shop"]):
            data["category"] = "shopping"

        if data["amount"] is None and data["merchant_name"] is None:
            data["confidence"] = 0.2

        return data
