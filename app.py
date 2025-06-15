from flask import Flask, request, send_file, jsonify
from moviepy.editor import VideoFileClip
import os
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return '''
    <h2>Online Video Compressor</h2>
    <form action="/compress" method="post" enctype="multipart/form-data">
      <input type="file" name="video" accept="video/*">
      <button type="submit">Compress</button>
    </form>
    '''

@app.route("/compress", methods=["POST"])
def compress_video():
    if "video" not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    video = request.files["video"]
    filename = str(uuid.uuid4()) + ".mp4"
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    output_path = os.path.join(OUTPUT_FOLDER, filename)

    video.save(input_path)

    try:
        clip = VideoFileClip(input_path)
        # Resize to 720p and compress
        clip_resized = clip.resize(height=720)
        clip_resized.write_videofile(output_path, bitrate="800k", codec="libx264", audio_codec="aac")
        clip.close()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return send_file(output_path, as_attachment=True)
