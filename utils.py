import pytesseract
from PIL import Image
import os

def preprocess_data(nutrition_image):
    text = pytesseract.image_to_string(Image.open(nutrition_image))
    # Process the extracted text to identify important nutritional values
    return text