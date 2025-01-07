import fitz  # PyMuPDF for PDF text extraction
import pytesseract  # Tesseract OCR
from PIL import Image
import logging
import os
import platform

def setup_tesseract():
    """Configure Tesseract based on environment"""
    try:
        if platform.system() == "Windows":
            # Windows configuration
            pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        else:
            # Linux/Cloud configuration
            os.environ["TESSDATA_PREFIX"] = "/usr/share/tesseract-ocr/4.00/tessdata"
    except Exception as e:
        logging.warning(f"Tesseract setup warning: {e}")

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file using PyMuPDF and Tesseract OCR for image-based pages.
    """
    try:
        setup_tesseract()
        text_output = ""
        
        with fitz.open(pdf_path) as pdf:
            for page_num in range(pdf.page_count):
                page = pdf[page_num]
                # Try basic text extraction first
                text = page.get_text("text")
                if text.strip():
                    text_output += text + "\n"
                else:
                    try:
                        # Try OCR if available
                        pix = page.get_pixmap()
                        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                        ocr_text = pytesseract.image_to_string(img, lang="srp")
                        text_output += ocr_text + "\n"
                    except Exception as ocr_error:
                        # Fallback to basic extraction if OCR fails
                        logging.warning(f"OCR failed, using basic extraction: {ocr_error}")
                        text_output += page.get_text("text") + "\n"
        
        return text_output
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {e}")
        raise
