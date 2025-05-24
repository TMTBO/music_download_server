import requests
from flask import Blueprint, request, jsonify

tx = Blueprint('tx', __name__, url_prefix='/tx')

@tx.route('/search', methods=['GET'])
def musicSearch():
    """
    调用腾讯音乐搜索接口
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

    url = "https://u.y.qq.com/cgi-bin/musicu.fcg"
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    }
    payload = {
        "comm": {
            "ct": 11,
            "cv": "1003006",
            "v": "1003006",
            "os_ver": "12",
            "phonetype": "0",
            "devicelevel": "31",
            "tmeAppID": "qqmusiclight",
            "nettype": "NETWORK_WIFI"
        },
        "req": {
            "module": "music.search.SearchCgiService",
            "method": "DoSearchForQQMusicLite",
            "param": {
                "query": keyword,
                "search_type": 0,
                "num_per_page": limit,
                "page_num": page,
                "nqc_flag": 0,
                "grp": 1
            }
        }
    }
    resp = requests.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    if 'req' in data and 'data' in data['req']:
        return jsonify(data['req']['data'])
    else:
        return jsonify({'error': 'No results found'}), 404
