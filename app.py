from flask import Flask, request, send_file
import os
import subprocess

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_file = request.files['video']
        if video_file:
            input_path = 'input.mp4'
            output_path = 'output.mp4'
            video_file.save(input_path)
            # Simple FFmpeg command to compress (adjust as needed)
            subprocess.run(['ffmpeg', '-i', input_path, '-vcodec', 'libx264', '-crf', '28', output_path])
            return send_file(output_path, as_attachment=True)
    return '''
    <h1>Online Video Compressor</h1>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="video" accept="video/*">
        <input type="submit" value="Compress">
    </form>
    '''

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
