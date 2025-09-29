from presidio_image_redactor import ImageRedactorEngine
from PIL import Image

import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

image = Image.open("test.jpeg")

redactor = ImageRedactorEngine()
# Perform redaction
redacted_image = redactor.redact(image=image)

# Save the redacted image to disk
redacted_image.save("redacted_test.png")