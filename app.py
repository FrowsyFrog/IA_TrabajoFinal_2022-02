from flask import Flask, render_template, request, jsonify
import cv2 as cv
import numpy as np
import base64
import io, sys
import scripts.poseEstimation as pe
from PIL import Image

app = Flask(__name__)

@app.route("/processing", methods=["POST"])
def process():
    # Get image ---
    file = request.files['image'].read() ## byte file
    npimg = np.fromstring(file, np.uint8)
    img = cv.imdecode(npimg,cv.IMREAD_COLOR)

    # Process image ---
    img = pe.pose_estimation(img, thickness=10)
    img = pe.resize_image(img, 150, 200)
    img = pe.crop_image(img)
    img = pe.resize_image(img, 28,28)

    # Return image ---
    img = Image.fromarray(img)
    rawBytes = io.BytesIO()
    img.save(rawBytes, "PNG")
    rawBytes.seek(0)
    img_base64 = base64.b64encode(rawBytes.read())
    return jsonify({'status':str(img_base64)})

@app.after_request
def after_request(response):
    print("log: setting cors" , file = sys.stderr)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)