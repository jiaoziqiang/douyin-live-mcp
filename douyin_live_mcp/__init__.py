from mcp.server.fastmcp import FastMCP
import re
import requests

mcp = FastMCP("DouyinLive")

headers = {
    'authority': 'v.douyin.com',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
}

@mcp.tool(name="get_douyin_stream_url", description="获取抖音直播推流地址(RTMP/HLS)，输入直播间链接或19位room_id")
def get_douyin_stream_url(url: str) -> dict:
    """获取抖音直播推流地址"""
    url = url.strip()
    
    if re.match(r'^\d{19}$', url):
        room_id = url
    else:
        url_match = re.search(r'(https?://[^\s]+)', url)
        if not url_match:
            return {"error": "无效的链接格式"}
        
        try:
            response = requests.head(url_match.group(1), headers=headers, allow_redirects=False)
            location = response.headers.get('location', '')
            match = re.search(r'\d{19}', location)
            if not match:
                return {"error": "无法获取room_id"}
            room_id = match[0]
        except Exception as e:
            return {"error": f"获取room_id失败: {str(e)}"}

    try:
        api_headers = {
            'authority': 'webcast.amemv.com',
            'cookie': '_tea_utm_cache_1128={%22utm_source%22:%22copy%22%2C%22utm_medium%22:%22android%22%2C%22utm_campaign%22:%22client_share%22}',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1'
        }
        params = {
            'type_id': '0',
            'live_id': '1',
            'room_id': room_id,
            'app_id': '1128'
        }
        response = requests.get('https://webcast.amemv.com/webcast/room/reflow/info/', 
                                 headers=api_headers, params=params)
        data = response.json()
        
        if not data.get('data') or not data['data'].get('room'):
            return {"error": "获取直播信息失败，可能主播未开播"}
        
        stream_url = data['data']['room'].get('stream_url', {})
        return {
            "room_id": room_id,
            "rtmp_pull_url": stream_url.get('rtmp_pull_url', ''),
            "hls_pull_url": stream_url.get('hls_pull_url', '')
        }
    except Exception as e:
        return {"error": f"获取直播地址失败: {str(e)}"}


import sys

def main(transport: str = None):
    if transport:
        mcp.run(transport=transport)
    else:
        if len(sys.argv) > 1 and sys.argv[1] == 'http':
            mcp.run(transport='streamable-http', host='0.0.0.0', port=8000)
        elif len(sys.argv) > 1 and sys.argv[1] == 'sse':
            mcp.run(transport='sse', host='0.0.0.0', port=8000)
        else:
            mcp.run()


if __name__ == '__main__':
    main()

__all__ = ['get_douyin_stream_url', 'main']