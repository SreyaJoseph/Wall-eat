import os
import pytesseract
from PIL import Image
import pandas as pd

# Path to dataset folder
dataset_path = 'dataset'

# Set up the path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Change this path to your installation

# Keywords typically found in nutritional information
nutrition_keywords = ['calories', 'fat', 'protein', 'carbohydrate', 'sugar', 'sodium', 'fiber']

data = []

# Function to filter text based on nutrition keywords
def filter_nutrition_info(text):
    filtered_lines = []
    for line in text.split('\n'):
        # Check if any nutrition-related keyword is in the line
        if any(keyword in line.lower() for keyword in nutrition_keywords):
            filtered_lines.append(line)
    return "\n".join(filtered_lines)

# Loop through each subfolder (e.g., chips, ketchup) and each image within
for category in os.listdir(dataset_path):
    category_path = os.path.join(dataset_path, category)
    if os.path.isdir(category_path):
        for img_name in os.listdir(category_path):
            img_path = os.path.join(category_path, img_name)
            try:
                # Open image using PIL
                img = Image.open(img_path)

                # Use Tesseract OCR to extract text from the image
                extracted_text = pytesseract.image_to_string(img)

                # Filter the text to keep only nutrition-related information
                nutrition_info = filter_nutrition_info(extracted_text)

                # Store the extracted nutrition text and corresponding category
                data.append({'category': category, 'text': nutrition_info})

            except Exception as e:
                print(f"Error processing {img_path}: {e}")

# Convert the data into a DataFrame and save it to a CSV file
df = pd.DataFrame(data)
df.to_csv('nutrition_data.csv', index=False)

print("Text extraction and filtering completed, saved to 'nutrition_data.csv'")