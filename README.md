# Douyin Live MCP

抖音直播推流地址获取MCP工具

## 功能

获取抖音直播间的RTMP/HLS推流地址，支持输入直播间链接或19位room_id。

## 安装

```bash
pip install douyin-live-mcp
```

## 使用方法

### 命令行

```bash
douyin-live-mcp
```

### 配置到MCP客户端

```json
{
  "mcpServers": {
    "douyin-live": {
      "command": "douyin-live-mcp"
    }
  }
}
```

## 工具

- `get_douyin_stream_url`: 获取抖音直播推流地址

## 示例输入

- 直播间链接: https://live.douyin.com/1234567890123456789
- room_id: 7283763263223100974