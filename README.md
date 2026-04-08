# timgiup-mcp-server

> Công cụ MCP (Model Context Protocol) cho phép AI Agent (Claude Desktop, Claude Code, Cline, Cursor, …) tìm kiếm **giấy tờ thất lạc**, **đồ thất lạc**, **thú cưng thất lạc**, **người thân thất lạc** và **đồ nhặt được** tại Việt Nam thông qua nền tảng [timgiup.com](https://timgiup.com).

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-1.0+-purple.svg)](https://modelcontextprotocol.io)

## Tính năng

- **Tìm kiếm bài đăng** theo từ khóa (tiếng Việt có/không dấu), lọc theo danh mục và tỉnh/thành
- **Reference data live từ API**: 6 danh mục cha (`/api/categories`) + 34 tỉnh/thành Việt Nam sau sáp nhập 2025 (`/api/provinces`) kèm aliases tên cũ
- **3 MCP tools**: `search_lost_items`, `list_categories`, `list_provinces`
- **8 MCP resources** expose tài nguyên public (đọc trực tiếp, không cần tool call):
  - `https://timgiup.com/openapi.json` — OpenAPI 3.1 spec
  - `https://timgiup.com/llms.txt` — AI/LLM discovery guide (chuẩn llmstxt.org)
  - `https://timgiup.com/rss/tat-ca.rss` — Feed tất cả bài
  - `https://timgiup.com/rss/do-that-lac.rss` — Feed đồ thất lạc
  - `https://timgiup.com/rss/thu-cung-that-lac.rss` — Feed thú cưng thất lạc
  - `https://timgiup.com/rss/nguoi-than-that-lac.rss` — Feed người thân thất lạc
  - `https://timgiup.com/rss/do-nhat-duoc.rss` — Feed đồ nhặt được
  - `https://timgiup.com/sitemap.xml` — Sitemap index
- Trả về tối đa 20 kết quả mỗi lần với đầy đủ: title, status, mô tả, danh mục, địa chỉ, ngày xảy ra, ảnh, link bài viết gốc

## API Endpoints sử dụng

MCP server gọi các REST API công khai sau (rate limit 30 req/phút/IP):
- `GET /api/search?q={keyword}&category={slug}&province={code}` — tìm kiếm
- `GET /api/categories` — danh mục cha
- `GET /api/provinces` — tỉnh/thành + aliases
- `GET /openapi.json`, `GET /llms.txt`, `GET /rss/{slug}.rss`, `GET /sitemap.xml` — exposed làm MCP resources

## Yêu cầu

- Python ≥ 3.10
- [`uv`](https://github.com/astral-sh/uv) (cung cấp `uvx`)

Cài `uv`:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Chạy thử

```bash
uvx --from git+https://github.com/timgiup/timgiup-mcp-server timgiup-mcp
```

(Server sẽ chờ JSON-RPC qua stdin — đây là behavior đúng. `Ctrl+C` để thoát.)

## Cấu hình Claude Code (CLI)

```bash
claude mcp add timgiup "$(which uvx)" -- --from git+https://github.com/timgiup/timgiup-mcp-server timgiup-mcp
```

Hoặc thêm thủ công vào `~/.claude.json`:

```json
{
  "mcpServers": {
    "timgiup": {
      "type": "stdio",
      "command": "/home/<user>/.local/bin/uvx",
      "args": [
        "--from",
        "git+https://github.com/timgiup/timgiup-mcp-server",
        "timgiup-mcp"
      ]
    }
  }
}
```

**Lưu ý:** Claude Code không load PATH của user shell → phải dùng **absolute path** cho `command`. Tìm bằng `which uvx`.

Restart Claude Code → kiểm tra bằng `/mcp` → `timgiup` phải `connected`.

## Cấu hình Claude Desktop

Mở file config:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

Thêm:

```json
{
  "mcpServers": {
    "timgiup": {
      "command": "/home/<user>/.local/bin/uvx",
      "args": [
        "--from",
        "git+https://github.com/timgiup/timgiup-mcp-server",
        "timgiup-mcp"
      ]
    }
  }
}
```

Khởi động lại Claude Desktop.

## Tích hợp các AI Agent khác

Xem [`examples/README.md`](examples/README.md) cho Cursor, Cline, Continue, Windsurf, Zed, Gemini CLI, OpenCode, Antigravity.

## Ví dụ prompt cho AI Agent

- "Tìm tin báo mất CCCD ở TP HCM gần đây nhất"
- "Có ai nhặt được ví da đen ở quận Hoàn Kiếm Hà Nội không?"
- "Tìm bài đăng tìm chó poodle thất lạc"
- "Liệt kê các danh mục bài đăng trên timgiup.com"
- "Tìm điện thoại iPhone bị mất ở Đà Nẵng, kèm link bài viết"

## API & Reference

- [`docs/api.md`](docs/api.md) — Tài liệu chi tiết REST API `/api/search`
- [`docs/mcp-server.md`](docs/mcp-server.md) — Hướng dẫn cài đặt MCP server đầy đủ
- [`docs/categories.md`](docs/categories.md) — 6 danh mục cha
- [`docs/provinces.md`](docs/provinces.md) — 34 tỉnh/thành Việt Nam + aliases tên cũ

## Đóng góp

PRs welcome. Bug/feature request: mở [issue](https://github.com/timgiup/timgiup-mcp-server/issues).

## License

[MIT](LICENSE) © 2026 [timgiup.com](https://timgiup.com)
