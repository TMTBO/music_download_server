import requests
from flask import Blueprint, request, jsonify
from app.musicSdk.wy_utils import eapi

wy = Blueprint('wy', __name__, url_prefix='/wy')

@wy.route('/search', methods=['GET'])
def musicSearch():
    """
    调用网易云音乐搜索接口
    :param keyword: 搜索关键词
    :param page: 页码，从0开始
    :param limit: 每页数量
    :return: 搜索结果的JSON数据
    """
    keyword = request.args.get('keyword', '')
    page = int(request.args.get('page', 0))
    limit = int(request.args.get('limit', 10))
    
    if not keyword:
        return jsonify({'error': 'keyword is required'}), 400

    url = "http://interface.music.163.com/eapi/batch"
    params = {
        's': keyword,
        'type': 1,  # 1: 单曲, 10: 专辑, 100: 歌手, 1000: 歌单, 1002: 用户, 1004: MV, 1006: 歌词, 1009: 电台, 1014: 视频
        'limit': limit,
        'offset': page * limit,
        'total': page == 1,
    }
    data = eapi('/api/cloudsearch/pc', params)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'origin': 'https://music.163.com'
    }
    
    resp = requests.post(url, data=data, headers=headers)
    resp.raise_for_status()
    
    data = resp.json()

    if 'result' in data and 'songs' in data['result']:
        return jsonify(data)
    else:
        return jsonify({'error': 'No results found'}), 404
    
@wy.route('/qualityDetail', methods=['GET'])
def qualityDetail():
    """
    获取网易云音乐单曲音质详情
    :param song_id: 歌曲ID
    :return: 音质详情的JSON数据
    """
    songId = request.args.get('songId', '')
    url = f"https://music.163.com/api/song/music/detail/get"
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'origin': 'https://music.163.com',
    }
    params = {'songId': songId}
    resp = requests.get(url, params=params, headers=headers)
    resp.raise_for_status()
    return resp.json()
