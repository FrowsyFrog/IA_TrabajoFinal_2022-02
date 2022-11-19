from flask import Flask, render_template, request, jsonify
import cv2 as cv
import numpy as np
import base64
import io, sys
import scripts.poseEstimation as pe
import scripts.posePrediction as pp
from PIL import Image

app = Flask(__name__)

@app.route("/processing", methods=["POST"])
def process():
    # Get image ---

    file = request.files['image'].read() ## byte file
    tck = int(request.values['thickness'])
    thr = float(request.values['thr'])
    npimg = np.fromstring(file, np.uint8)
    img = cv.imdecode(npimg,cv.IMREAD_COLOR)

    # Process image ---
    img = pe.pose_estimation(img, tck, thr)
    print("pose si")
    img = pe.resize_image(img, 150, 200)
    img = pe.crop_image(img)
    text = "Error..."

    if img.shape == (0,0):
        img = Image.open("static/img/error.png")
    else:
        img = pe.resize_image(img, 28,28)
        img = Image.fromarray(img)
        text = pp.prediction(img)

    # Return image ---

    print("predict si")

    rawBytes = io.BytesIO()
    img.save(rawBytes, "PNG")
    print("save si")
    rawBytes.seek(0)
    img_base64 = base64.b64encode(rawBytes.read())
    return jsonify({'status':str(img_base64),'text':str(text)})

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