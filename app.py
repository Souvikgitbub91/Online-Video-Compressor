from flask import Flask, request, jsonify, send_file, render_template
import os
import uuid
import subprocess

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "compressed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/compress", methods=["POST"])
def compress_video():
    if "video" not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    video = request.files["video"]
    filename = str(uuid.uuid4())
    input_path = os.path.join(UPLOAD_FOLDER, filename + ".mp4")
    output_path = os.path.join(OUTPUT_FOLDER, filename + "_compressed.mp4")

    video.save(input_path)

    try:
        # Run ffmpeg to compress
        subprocess.run(
            ["ffmpeg", "-i", input_path, "-vcodec", "libx264", "-crf", "28", output_path],
            check=True
        )
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Compression failed", "details": str(e)}), 500

    return send_file(output_path, as_attachment=True)
