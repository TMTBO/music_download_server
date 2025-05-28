import os
import requests
from flask import Blueprint, request, jsonify, Response, stream_with_context
from app.musicSdk.kw import kw
from app.musicSdk.kg import kg
from app.musicSdk.tx import tx
from app.musicSdk.mg import mg
from app.musicSdk.wy import wy
from app.musicSdk.ikun import ikun

# Create a Blueprint for the app
music = Blueprint('music', __name__, url_prefix='/music')
music.register_blueprint(kw)
music.register_blueprint(kg)
music.register_blueprint(tx)
music.register_blueprint(mg)
music.register_blueprint(wy)
music.register_blueprint(ikun) 

@music.route('/download', methods=['POST'])
def download():
    """
    通过 body 中的 musicURL 下载文件，并命名为 body 中的 musicName，保存到 ~/Music 目录。
    持续回调下载进度。
    """
    data = request.get_json()
    music_url = data.get('url')
    music_name = data.get('name')
    if not music_url or not music_name:
        return jsonify({'error': 'musicURL and musicName are required'}), 400

    music_dir = os.environ.get('MUSIC_DIR')
    os.makedirs(music_dir, exist_ok=True)
    file_path = os.path.join(music_dir, music_name)

    def generate():
        try:
            resp = requests.get(music_url, stream=True)
            resp.raise_for_status()
            total = int(resp.headers.get('content-length', 0))
            downloaded = 0
            with open(file_path, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        percent = int(downloaded * 100 / total) if total else 0
                        yield f"{{\"progress\": {percent}}}"
            yield f"{{\"message\": \"Downloaded as {file_path}\"}}"
        except Exception as e:
            yield f"{{\"error\": \"{str(e)}\"}}"

    return Response(stream_with_context(generate()), mimetype='text/event-stream')



