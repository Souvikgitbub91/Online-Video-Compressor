from flask import Flask, request, send_file
import os
import subprocess

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_file = request.files.get('video')
        if video_file:
            input_path = 'input.mp4'
            output_path = 'output.mp4'
            try:
                video_file.save(input_path)
                result = subprocess.run(['ffmpeg', '-i', input_path, '-vcodec', 'libx264', '-crf', '28', output_path], capture_output=True, text=True)
                if result.returncode != 0:
                    raise Exception(result.stderr)
                return send_file(output_path, as_attachment=True)
            except Exception as e:
                return f"Error: {str(e)}", 500
    return '''
    <h1>Online Video Compressor</h1>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="video" accept="video/*">
        <input type="submit" value="Compress">
    </form>
    '''
