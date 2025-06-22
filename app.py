from flask import Flask, request, send_file
import os
import subprocess
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_file = request.files.get('video')
        if video_file:
            input_path = '/tmp/input.mp4'
            output_path = '/tmp/output.mp4'
            try:
                video_file.save(input_path)
                logging.info(f"Saved input file to {input_path}")
                result = subprocess.run(
                    ['ffmpeg', '-i', input_path, '-vcodec', 'libx264', '-crf', '28', '-y', output_path],
                    capture_output=True, text=True, timeout=300  # 5-minute timeout
                )
                logging.info(f"FFmpeg stdout: {result.stdout}")
                if result.returncode != 0:
                    raise Exception(f"FFmpeg failed: {result.stderr}")
                if not os.path.exists(output_path):
                    raise Exception("Compression failed: Output file not created")
                return send_file(output_path, as_attachment=True)
            except subprocess.TimeoutExpired as e:
                logging.error(f"Timeout: {str(e)}")
                return "Error: Compression timed out", 500
            except Exception as e:
                logging.error(f"Error: {str(e)}")
                return f"Error: {str(e)}", 500
            finally:
                for path in (input_path, output_path):
                    if os.path.exists(path):
                        os.remove(path)
        return "No video file uploaded", 400
    return '''
    <h1>Online Video Compressor</h1>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="video" accept="video/*">
        <input type="submit" value="Compress">
    </form>
    '''
