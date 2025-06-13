from flask import Flask, request, jsonify, send_file
import os
from moviepy.editor import VideoFileClip
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "compressed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

from flask import Flask, request, jsonify, send_file, render_template
# ... rest of your imports

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/compress", methods=["POST"])
def compress_video():
    if "video" not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    video = request.files["video"]
    filename = str(uuid.uuid4()) + ".mp4"
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    output_path = os.path.join(OUTPUT_FOLDER, filename)

    video.save(input_path)

    clip = VideoFileClip(input_path)
    clip.write_videofile(output_path, bitrate="500k", codec="libx264", audio_codec="aac")
    clip.close()

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
