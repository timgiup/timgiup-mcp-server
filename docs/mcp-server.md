# MCP Server — Hướng dẫn cài đặt và tích hợp

## Tổng quan

MCP server này cung cấp 3 tools cho AI Agent để tìm kiếm bài đăng trên timgiup.com:

| Tool | Mục đích | Input |
|------|----------|-------|
| `search_lost_items` | Tìm bài đăng theo từ khóa | `query` (required), `category`, `province` |
| `list_categories` | Lấy danh sách danh mục | (không) |
| `list_provinces` | Lấy danh sách 34 tỉnh/thành | (không) |

Server giao tiếp qua **stdio** theo chuẩn MCP 1.0+.

## Yêu cầu

- Python ≥ 3.10
- pip hoặc [uv](https://github.com/astral-sh/uv)

## Cài đặt

### Phương án A: chạy trực tiếp với `uvx` (khuyến nghị)
Không cần cài đặt local. `uvx` tự động tải và chạy:
```bash
uvx --from git+https://github.com/timgiup/lost-item-search-api-vietnam lost-item-search-mcp
```

### Phương án B: clone & cài đặt editable
```bash
git clone https://github.com/timgiup/lost-item-search-api-vietnam.git
cd lost-item-search-api-vietnam
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
lost-item-search-mcp
```

### Phương án C: pip install từ git
```bash
pip install git+https://github.com/timgiup/lost-item-search-api-vietnam.git
lost-item-search-mcp
```

## Biến môi trường

| Biến | Mặc định | Mô tả |
|------|----------|-------|
| `TIMGIUP_API_BASE_URL` | `https://timgiup.com` | URL gốc API. Đổi nếu chạy môi trường staging/local. |

## Tích hợp Claude Desktop

File config: `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) hoặc `%APPDATA%\Claude\claude_desktop_config.json` (Windows).

```json
{
  "mcpServers": {
    "lost-item-search-vn": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/timgiup/lost-item-search-api-vietnam",
        "lost-item-search-mcp"
      ],
      "env": {
        "TIMGIUP_API_BASE_URL": "https://timgiup.com"
      }
    }
  }
}
```

Khởi động lại Claude Desktop. Tools sẽ xuất hiện trong UI.

## Tích hợp Cline / Cursor / Continue

Các IDE extension hỗ trợ MCP đều dùng cùng schema `mcpServers`. Copy block JSON ở trên vào file config của IDE.

## Test thử

### Test client riêng (không qua MCP)
```bash
python -c "
import asyncio
from mcp_server.client import TimgiupClient
client = TimgiupClient()
result = asyncio.run(client.search('cccd', province='79'))
print(f\"Tìm thấy {result['total']} kết quả\")
for r in result['results'][:3]:
    print(f\"- {r['title']} → {r['source_url']}\")
"
```

### Test MCP server qua stdio
Server sẽ chờ JSON-RPC message qua stdin. Test bằng MCP Inspector:
```bash
npx @modelcontextprotocol/inspector lost-item-search-mcp
```

## Ví dụ prompt cho AI Agent

- "Tìm tin báo mất CCCD ở TP HCM tuần qua"
- "Có ai nhặt được ví da đen ở Hà Nội không?"
- "Liệt kê 6 danh mục chính trên timgiup.com"
- "Tìm bài đăng về chó poodle thất lạc"
- "Tìm điện thoại iPhone bị mất ở Đà Nẵng, kèm link bài viết"

## Troubleshooting

| Lỗi | Nguyên nhân | Giải pháp |
|-----|-------------|-----------|
| `ModuleNotFoundError: mcp` | MCP SDK chưa cài | `pip install mcp>=1.0.0` |
| `httpx.ConnectError` | Không kết nối được API | Kiểm tra `TIMGIUP_API_BASE_URL` và mạng |
| `429 Too Many Requests` | Vượt rate limit (30/min) | Đợi 1 phút rồi thử lại |
| Tool không xuất hiện trong Claude | Sai config path | Kiểm tra file config + restart Claude Desktop |

## Kiến trúc

```
┌──────────────┐  stdio   ┌──────────────┐  HTTPS  ┌──────────────┐
│  AI Agent    │ ──JSON──▶│ MCP Server   │ ───────▶│ timgiup.com  │
│  (Claude…)   │ ◀─RPC────│ (Python)     │ ◀───────│  /api/search │
└──────────────┘          └──────────────┘         └──────────────┘
```

- `mcp_server/server.py` — MCP protocol handler, tool registry
- `mcp_server/client.py` — async HTTP client (httpx)
- `mcp_server/data/` — reference data (categories, provinces)
