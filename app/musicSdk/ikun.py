import os
import requests
from flask import Blueprint, request, jsonify


API_URL = os.environ.get("IKUN_API_URL")
API_KEY = os.environ.get("IKUN_API_KEY")
MUSIC_QUALITY = {
    "kw":["128k","320k","flac","flac24bit","hires"],
    "mg":["128k","320k","flac","flac24bit","hires"],
    "kg":["128k","320k","flac","flac24bit","hires","atmos","master"],
    "tx":["128k","320k","flac","flac24bit","hires","atmos","atmos_plus","master"],
    "wy":["128k","320k","flac","flac24bit","hires","atmos","master"]
}

ikun = Blueprint('ikun', __name__, url_prefix='/ikun')

@ikun.route('/getMusicURL', methods=['GET'])
def getMusicURL():
    """
    获取音乐播放链接
    :param source: 来源 (如 'kw', 'kg', 'tx', 'wy', 'mg')
    :param musicId: 歌曲ID
    :param quality: 音质类型 (如 '128k', '320k', 'flac')
    :return: 音乐播放链接的JSON数据
    """
    source = request.args.get('source')
    musicId = request.args.get('musicId')
    quality = request.args.get('quality', '128k')
    if not source or not musicId:
        return jsonify({'error': 'source and musicId are required'}), 400
    if source not in MUSIC_QUALITY.keys():
        return jsonify({'error': 'unsupport source: ${source}'}), 400
    if quality not in MUSIC_QUALITY[source]:
        return jsonify({'error': 'unsupport quality: ${quality}'}), 400
    try:
        resp = requests.get(
            f"{API_URL}/url?source={source}&songId={musicId}&quality={quality}",
            headers={
                "Content-Type": "application/json",
                "User-Agent": "lx-music-request/3.2.2",
                "X-Request-Key": API_KEY,
            },
            timeout=10
        )
        resp.raise_for_status()
        return jsonify(resp.json())
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500

#    v12
#   const request = await httpFetch(
#     `${API_URL}/url?source=${source}&songId=${songId}&quality=${quality}`,
#     {
#       method: "GET",
#       headers: {
#         "Content-Type": "application/json",
#         "User-Agent": `${
#           env ? `lx-music-${env}/${version}` : `lx-music-request/${version}`
#         }`,
#         "X-Request-Key": API_KEY,
#       },
#       follow_max: 5,
#     }
#   );