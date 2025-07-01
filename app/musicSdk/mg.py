def createSignature(time, str, deviceId):
    import hashlib
    
    signatureMd5 = '6cdc72a439cef99a3418d2a78aa28c73'
    sign = hashlib.md5(f"{str}{signatureMd5}yyapp2d16148780a1dcc7408e06336b98cfd50{deviceId}{time}".encode('utf-8')).hexdigest()
    return sign

import requests
from flask import Blueprint, request, jsonify

mg = Blueprint('mg', __name__, url_prefix='/mg')

@mg.route('/search', methods=['GET'])
def musicSearch():
    """
    调用咪咕音乐搜索接口
    :param keyword: 搜索关键词
    :param page: 页码，从0开始
    :param limit: 每页数量
    :return: 搜索结果的JSON数据
    """
    keyword = request.args.get('keyword', '')
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    
    if not keyword:
        return jsonify({'error': 'keyword is required'}), 400
    
    timestamp = str(int(requests.utils.default_headers().get('Date', 0) / 1000))
    deviceId = '963B7AA0D21511ED807EE5846EC87D20'
    sign = createSignature(timestamp, keyword, deviceId)

    url = "https://jadeite.migu.cn/music_search/v3/search/searchAll"
    params = {
        'isCorrect': 0,
        'isCopyright': 1,
        'searchSwitch': '{"song":1,"album":0,"singer":0,"tagSong":1,"mvSong":0,"bestShow":1,"songlist":0,"lyricSong":0}',
        'pageSize': limit,
        'text': keyword,
        'pageNo': page,  # 页码从1开始
        'sort': 0,
        'sid': 'USS'
    }
    
    headers = {
        'uiVersion': 'A_music_3.6.1',
        'deviceId': deviceId,
        'timestamp': timestamp,
        'sign': sign,  # 需要根据实际情况生成
        'channel': '0146921',
        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 11.0.0; zh-cn; MI 11 Build/OPR1.170623.032) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
    }
    
    resp = requests.get(url, params=params, headers=headers)
    resp.raise_for_status()
    
    data = resp.json()

    if 'songResultData' in data:
        return jsonify(data['songResultData'])
    else:
        return jsonify({'error': 'No results found'}), 404

@mg.route('/getPicURL', methods=['GET'])
def getPicURL():
    """
    获取咪咕音乐歌曲图片链接
    :param songId: 歌曲ID
    :return: 图片链接的JSON数据
    """
    songId = request.args.get('songId', '')
    
    if not songId:
        print("songId is required")
        return jsonify({'picUrl': ""})
    
    url = f"http://music.migu.cn/v3/api/music/audioPlayer/getSongPic?songId={songId}"
    
    headers = {
        'Referer': 'http://music.migu.cn/v3/music/player/audio?from=migu',
    }
    
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()

    print(f"Response from {url}: {resp.text}")
    
    data = resp.json()
    
    if data['returnCode'] != '000000':
        print(f"Error fetching picture URL: {data.get('returnCode', 'Unknown error')}")
        return jsonify({'picUrl': ""})
    
    pic_url = data.get('largePic') or data.get('mediumPic') or data.get('smallPic')
    
    if not pic_url.startswith(('http:', 'https:')):
        pic_url = 'http:' + pic_url
    
    return jsonify({'picUrl': pic_url})
