# Lost Item Search API Vietnam — MCP Server

> Công cụ MCP (Model Context Protocol) cho phép AI Agent (Claude Desktop, Cline, Cursor, …) tìm kiếm **giấy tờ thất lạc**, **đồ thất lạc**, **thú cưng thất lạc**, **người thân thất lạc** và **đồ nhặt được** tại Việt Nam thông qua nền tảng [timgiup.com](https://timgiup.com).

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-1.0+-purple.svg)](https://modelcontextprotocol.io)

## Tính năng

- 🔎 **Tìm kiếm bài đăng** theo từ khóa (tiếng Việt có dấu), lọc theo danh mục và tỉnh/thành
- 📚 **Reference data** đầy đủ: 6 danh mục cha + 53 danh mục con, 34 tỉnh/thành Việt Nam (sau sáp nhập 2025)
- 🤖 **3 MCP tools** sẵn sàng cho AI Agent: `search_lost_items`, `list_categories`, `list_provinces`
- 🌐 Trả về tối đa 20 kết quả mỗi lần với đầy đủ: title, mô tả, danh mục, địa chỉ, ngày xảy ra, ảnh, và link bài viết gốc

## Cài đặt nhanh

### Cách 1: dùng `uvx` (khuyến nghị)
```bash
uvx --from git+https://github.com/timgiup/lost-item-search-api-vietnam lost-item-search-mcp
```

### Cách 2: clone & cài local
```bash
git clone https://github.com/timgiup/lost-item-search-api-vietnam.git
cd lost-item-search-api-vietnam
pip install -e .
lost-item-search-mcp
```

## Cấu hình Claude Desktop

Mở `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) hoặc `%APPDATA%\Claude\claude_desktop_config.json` (Windows), thêm:

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

Khởi động lại Claude Desktop. Tool sẽ xuất hiện trong danh sách MCP tools.

Xem thêm: [`examples/claude-desktop-config.json`](examples/claude-desktop-config.json)

## Ví dụ sử dụng (prompt cho AI Agent)

- "Tìm tin báo mất CCCD ở TP HCM gần đây nhất"
- "Có ai nhặt được ví da đen ở quận Hoàn Kiếm Hà Nội không?"
- "Tìm bài đăng tìm chó poodle thất lạc"
- "Liệt kê các danh mục bài đăng trên timgiup.com"
- "Tìm điện thoại iPhone bị mất ở Đà Nẵng"

## API & Reference

- 📖 [`docs/api.md`](docs/api.md) — Tài liệu chi tiết REST API `/api/search`
- 📖 [`docs/mcp-server.md`](docs/mcp-server.md) — Hướng dẫn cài đặt và tích hợp MCP server
- 📋 [`docs/categories.md`](docs/categories.md) — Danh sách 6 danh mục cha + subcategory
- 📋 [`docs/provinces.md`](docs/provinces.md) — Danh sách 34 tỉnh/thành Việt Nam

## Yêu cầu

- Python ≥ 3.10
- `mcp` ≥ 1.0.0
- `httpx` ≥ 0.27.0

## Đóng góp

PRs welcome! Nếu phát hiện bug hoặc muốn đề xuất tính năng, vui lòng mở [issue](https://github.com/timgiup/lost-item-search-api-vietnam/issues).

## License

[MIT](LICENSE) © 2026 [timgiup.com](https://timgiup.com)
