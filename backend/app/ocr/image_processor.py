import cv2
import numpy as np
from PIL import Image
from typing import Tuple
import io

class ImageProcessor:
    @staticmethod
    def preprocess_image(image_bytes: bytes) -> np.ndarray:
        """Preprocess receipt image for OCR"""
        # Read image
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply threshold
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        
        # Denoise
        denoised = cv2.fastNlMeansDenoising(thresh, None, 10, 10, 21)
        
        # Upscale
        scale_factor = 2
        upscaled = cv2.resize(
            denoised,
            None,
            fx=scale_factor,
            fy=scale_factor,
            interpolation=cv2.INTER_CUBIC
        )
        
        return upscaled
    
    @staticmethod
    def get_receipt_contours(image: np.ndarray) -> Tuple[np.ndarray, list]:
        """Find receipt contours in image"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        
        contours, _ = cv2.findContours(
            edges,
            cv2.RETR_TREE,
            cv2.CHAIN_APPROX_SIMPLE
        )
        
        return image, contours
    
    @staticmethod
    def crop_receipt(image: np.ndarray, contour) -> np.ndarray:
        """Crop receipt from image"""
        x, y, w, h = cv2.boundingRect(contour)
        return image[y:y+h, x:x+w]
