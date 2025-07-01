import requests
from flask import Blueprint, request, jsonify

kw = Blueprint('kw', __name__, url_prefix='/kw')

@kw.route('/search', methods=['GET'])
def musicSearch():
    """
    调用酷我音乐搜索接口
    :param keyword: 搜索关键词
    :param page: 页码，从1开始
    :param limit: 每页数量
    :return: 搜索结果的JSON数据
    """
    keyword = request.args.get('keyword', '')
    page = int(request.args.get('page', 0))
    limit = int(request.args.get('limit', 10))
    print(f"keyword: {keyword}, page: {page}, limit: {limit}")
    if not keyword:
        return jsonify({'error': 'keyword is required'}), 400
    url = (
        "http://search.kuwo.cn/r.s"
        "?client=kt"
        f"&all={requests.utils.quote(keyword)}"
        f"&pn={page}"
        f"&rn={limit}"
        "&uid=794762570"
        "&ver=kwplayer_ar_9.2.2.1"
        "&vipver=1"
        "&show_copyright_off=1"
        "&newver=1"
        "&ft=music"
        "&cluster=0"
        "&strategy=2012"
        "&encoding=utf8"
        "&rformat=json"
        "&vermerge=1"
        "&mobi=1"
        "&issubtitle=1"
    )
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

@kw.route('/getMusicURL', methods=['GET'])
def getMusicURL():
    """
    获取酷我音乐播放链接
    参数:
        rid: 歌曲ID (songmid)
        br: 码率类型 (如 128k, 320k, flac 等)
    """
    rid = request.args.get('musicId')
    br = request.args.get('quality', '128k')  # 默认128
    if not rid:
        return jsonify({'error': 'rid is required'}), 400

    # 码率映射，可根据实际需求扩展
    kw_quality_format = {
        '128k': {'e': '128kmp3'},
        '192k': {'e': '192kmp3'},
        '320k': {'e': '320kmp3'},
        'flac': {'e': '2000kflac'},
        'hires': {'e': '4000kflac'},
        'master': {'e': '20900kflac'},
    }
    br_format = kw_quality_format.get(br, kw_quality_format['128k'])['e']

    rawData = {
        'f': 'web',
        'rid': int(rid),
        'br': br_format,
        'source': 'jiakong',
        'type': 'convert_url_with_sign',
        'surl': '1',
    }
    queryString = '&'.join([f"{k}={v}" for k, v in rawData.items()])
    url = f"https://mobi.kuwo.cn/mobi.s?{queryString}"

    headers = {
        'User-Agent': 'okhttp/3.10.0'
    }

    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()

@kw.route('/getPicURL', methods=['GET'])
def getPicURL():
    """
    获取酷我音乐专辑封面图片链接
    参数:
        rid: 歌曲ID (songmid)
    """
    rid = request.args.get('rid')
    if not rid:
        return jsonify({'error': 'rid is required'}), 400
    url = f"http://artistpicserver.kuwo.cn/pic.web?corp=kuwo&type=rid_pic&pictype=500&size=500&rid={rid}"
    resp = requests.get(url)
    resp.raise_for_status()
    return jsonify({'picUrl': resp.text})