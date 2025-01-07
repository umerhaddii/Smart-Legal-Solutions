import fitz
import pytesseract
from PIL import Image
import logging
import os

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF with fallback if OCR is unavailable"""
    text_output = ""
    try:
        with fitz.open(pdf_path) as pdf:
            for page_num in range(pdf.page_count):
                page = pdf[page_num]
                # Try standard text extraction first
                text = page.get_text("text")
                if text.strip():
                    text_output += text + "\n"
                else:
                    try:
                        # Attempt OCR only if text is empty
                        pix = page.get_pixmap()
                        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                        ocr_text = pytesseract.image_to_string(img, lang="srp")
                        text_output += ocr_text + "\n"
                    except pytesseract.TesseractNotFound:
                        # Fallback if OCR is unavailable
                        logging.warning("Tesseract OCR not available - skipping image-based text extraction")
                        text_output += "[Image content - OCR unavailable]\n"
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {e}")
        raise
    return text_output
