from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os

# Import your existing functions
from pptDescription import process_PPT
from pdfDescription import process_PDF
from imageDescription import process_image
from excelDescription import process_EXCEL

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {".jpg", ".png", ".pptx", ".pdf", ".xlsx"}

# Create uploads folder if not exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = "supersecretkey"  # Needed for flashing messages


def allowed_file(filename):
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS


def process_file(file_path):
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    dispatch = {
        ".jpg": process_image,
        ".png": process_image,
        ".pptx": process_PPT,
        ".pdf": process_PDF,
        ".xlsx": process_EXCEL,
    }

    if ext in dispatch:
        return dispatch[ext](file_path)
    else:
        return f"Unsupported file type: {ext}"



@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)

        file = request.files["file"]

        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(save_path)

            # Process and capture output
            result = process_file(save_path)

            return render_template("upload.html", result=result)
        else:
            flash("Unsupported file type")
            return redirect(request.url)

    return render_template("upload.html")


if __name__ == "__main__":
    app.run(debug=True)
