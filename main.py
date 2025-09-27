from pptDescription import process_PPT
from pdfDescription import process_PDF
from imageDescription import process_image
import os

files=["File_003.png","File_007.png","File_013.png","File_012.pdf","File_014.pptx"]

def process_file(file_name):
    # Get file extension in lowercase
    _, ext = os.path.splitext(file_name)
    ext = ext.lower()

    # Dispatch table for file types
    dispatch = {
        ".jpg": process_image,
        ".png": process_image,
        ".pptx": process_PPT,
        ".pdf":process_PDF,
    }

    if ext in dispatch:
        dispatch[ext](file_name)
    else:
        print(f"Unsupported file type: {ext}")

for file in files:
    print("\n------"+file+"-------")
    process_file(file)