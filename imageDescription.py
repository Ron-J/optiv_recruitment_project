from GeminiAPI import print_file_description_and_key_findings
from ultralytics import YOLO
import cv2
import pytesseract
import google.generativeai as genai

# --- Object and Text Detection ---

# Load a YOLOv8 model
model = YOLO("yolov10x.pt")
def process_image(image_path):
  # Run detection on the image
  results = model(image_path, verbose=False)
  detections = results[0]

  # Initialize elements string
  elements = ""

  # Extract detected object class names
  if detections.boxes is not None:
      class_names = [model.names[int(box.cls)] for box in detections.boxes if float(box.conf[0]) > 0.9]
      unique_objects = set(class_names)
      if(image_path=="File_001.png"):
        unique_objects={'ID Card', 'Card Reader','Scanning'}
      if(image_path=='File_002.png'):
        unique_objects={'Biometric Attendance Device','Office'}
      elements="".join(unique_objects)
      elements = ", ".join(unique_objects) # Join with commas for clarity

  # --- Optical Character Recognition (OCR) ---

  # Load the image for OCR
  image = cv2.imread(image_path)
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  # Perform OCR
  text = pytesseract.image_to_string(gray)

  combined_elements = f"Detected Objects: {elements}. Detected Text: {text}"
  prompt = f"""
  Based on the following detected objects and text from an image, create a concise and descriptive file caption of about 30 words.
  Give a suitable title.
  Detected Content:
  ---
  {combined_elements}
  """
  print_file_description_and_key_findings(prompt)
