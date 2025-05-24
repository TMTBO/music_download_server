import requests
from flask import Blueprint, request, jsonify
import time

kg = Blueprint('kg', __name__, url_prefix='/kg')

@kg.route('/search', methods=['GET'])
def musicSearch():
    """
    调用酷狗音乐搜索接口
    :param keyword: 搜索关键词
    :param page: 页码，从0开始
    :param pagesize: 每页数量
    :return: 搜索结果的JSON数据
    """
    keyword = request.args.get('keyword', '')
    page = int(request.args.get('page', 0))
    pagesize = int(request.args.get('pagesize', 10))
    print(f"keyword: {keyword}, page: {page}, pagesize: {pagesize}")
    if not keyword:
        return jsonify({'error': 'keyword is required'}), 400

    url = (
        "https://songsearch.kugou.com/song_search_v2"
        f"?keyword={requests.utils.quote(keyword)}"
        f"&page={page}"
        f"&pagesize={pagesize}"
        "&userid=0"
        "&clientver="
        "&platform=WebFilter"
        "&filter=2"
        "&iscorrection=1"
        "&privilege_filter=0"
        "&area_code=1"
    )
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

@kg.route('/qualityDetail', methods=['POST'])
def qualityDetail():
    """
    获取音质详情
    :return: 音质详情的JSON数据
    """
    hashList = request.get_json()
    # hashList = data.get('hashList', [])
    if not isinstance(hashList, list) or not hashList:
        return jsonify({'error': 'hashList is required and must be a list'}), 400

    resources = [{"id": 0, "type": "audio", "hash": h} for h in hashList]

    clienttime = int(time.time() * 1000)  # 等价于 JS 的 Date.now()

    url = f"https://gateway.kugou.com/goodsmstore/v1/get_res_privilege?appid=1005&clientver=20049&clienttime={clienttime}&mid=NeZha"

    payload = {
        "behavior": "play",
        "clientver": "20049",
        "resource": resources,
        "area_code": "1",
        "quality": "128",
        "qualities": [
            "128", "320", "flac", "high", "dolby",
            "viper_atmos", "viper_tape", "viper_clear"
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }

    resp = requests.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()
