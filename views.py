# Important imports
from app import app
from flask import request, render_template
import os
from skimage.metrics import structural_similarity
import imutils
import cv2
from PIL import Image

# Adding path to config
app.config['INITIAL_FILE_UPLOADS'] = 'app/static/uploads'
app.config['EXISTNG_FILE'] = 'app/static/original'
app.config['GENERATED_FILE'] = 'app/static/generated'

# Ensure directories exist
os.makedirs(app.config['INITIAL_FILE_UPLOADS'], exist_ok=True)
os.makedirs(app.config['EXISTNG_FILE'], exist_ok=True)
os.makedirs(app.config['GENERATED_FILE'], exist_ok=True)

# Route to home page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        if 'file_upload' not in request.files:
            return render_template('index.html', pred='No file part')

        file_upload = request.files['file_upload']
        if file_upload.filename == '':
            return render_template('index.html', pred='No selected file')

        # Save uploaded image
        if file_upload:
            filename = 'image.jpg'
            file_path = os.path.join(app.config['INITIAL_FILE_UPLOADS'], filename)
            file_upload.save(file_path)

            # Resize and save the uploaded image
            uploaded_image = Image.open(file_path).resize((250, 160))
            uploaded_image.save(file_path)

            # Ensure the original image is available
            original_file_path = os.path.join(app.config['EXISTNG_FILE'], filename)
            if not os.path.isfile(original_file_path):
                return render_template('index.html', pred='Original image not found')

            original_image = Image.open(original_file_path).resize((250, 160))
            original_image.save(original_file_path)

            # Read images
            original_image_cv = cv2.imread(original_file_path)
            uploaded_image_cv = cv2.imread(file_path)

            # Convert images to grayscale
            original_gray = cv2.cvtColor(original_image_cv, cv2.COLOR_BGR2GRAY)
            uploaded_gray = cv2.cvtColor(uploaded_image_cv, cv2.COLOR_BGR2GRAY)

            # Compute structural similarity
            (score, diff) = structural_similarity(original_gray, uploaded_gray, full=True)
            diff = (diff * 255).astype("uint8")

            # Threshold and find contours
            thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)

            # Draw contours
            for c in cnts:
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(original_image_cv, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.rectangle(uploaded_image_cv, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # Save results
            cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_original.jpg'), original_image_cv)
            cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_uploaded.jpg'), uploaded_image_cv)
            cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_diff.jpg'), diff)
            cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_thresh.jpg'), thresh)

            return render_template('index.html', pred=str(round(score * 100, 2)) + '%' + ' correct')

# Main function
if __name__ == '__main__':
    app.run(debug=True)
