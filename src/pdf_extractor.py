import fitz  # PyMuPDF for PDF text extraction
import pytesseract  # Tesseract OCR
from PIL import Image
import logging
import os

# Ensure TESSDATA_PREFIX is set to the tessdata directory
os.environ["TESSDATA_PREFIX"] = r"C:\Program Files\Tesseract-OCR\tessdata"

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file using PyMuPDF and Tesseract OCR for image-based pages.
    """
    text_output = ""
    try:
        with fitz.open(pdf_path) as pdf:
            for page_num in range(pdf.page_count):
                page = pdf[page_num]
                text = page.get_text("text")
                if text.strip():
                    text_output += text + "\n"
                else:
                    # Convert PDF page to image
                    pix = page.get_pixmap()
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    # Use Tesseract to extract text from image (using Serbian)
                    ocr_text = pytesseract.image_to_string(img, lang="srp")
                    text_output += ocr_text + "\n"
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {e}")
        raise
    return text_output