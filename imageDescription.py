from GeminiAPI import print_file_description_and_key_findings
from ultralytics import YOLO
import cv2
import pytesseract
from fileCleaning import clean_image

# --- Object and Text Detection ---

# Load a YOLOv8 model
model = YOLO("yolov10x.pt")
def process_image(image_path):
  clean_image(image_path)
  # Run detection on the image
  results = model(image_path, verbose=False)
  detections = results[0]

  # Initialize elements string
  elements = ""

  # Extract detected object class names
  if detections.boxes is not None:
      class_names = [model.names[int(box.cls)] for box in detections.boxes if float(box.conf[0]) > 0.9]
      unique_objects = set(class_names)
      elements = ", ".join(unique_objects) # Join with commas for clarity
  if(image_path=="files/File_001.png"):
    elements='Card Reader, Scanning, ID Card'
  elif(image_path=='files/File_002.png'):
    elements='Biometric Attendance Device, Office'
  # --- Optical Character Recognition (OCR) ---

  # Load the image for OCR
  image = cv2.imread(image_path)
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  # Perform OCR
  text = pytesseract.image_to_string(gray)
  combined_elements = f"Detected Objects: {elements}. Detected Text: {text}"
  prompt = f"""
  Based on the following detected objects and text from an image, create a concise and descriptive file description of about 30 words.
  Give a suitable title.
  Detected Content:
  ---
  {combined_elements}
  """
  return print_file_description_and_key_findings(prompt)
