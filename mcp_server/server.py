"""MCP server expose 3 tools cho AI Agent tìm kiếm đồ thất lạc tại Việt Nam."""

from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from .client import TimgiupClient

DATA_DIR = Path(__file__).parent / "data"

# Khởi tạo server + client
_base_url = os.environ.get("TIMGIUP_API_BASE_URL", "https://timgiup.com")
_client = TimgiupClient(base_url=_base_url)
server: Server = Server("lost-item-search-vietnam")


def _load_json(filename: str) -> Any:
    """Đọc file JSON từ thư mục data."""
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


@server.list_tools()
async def list_tools() -> list[Tool]:
    """Danh sách tools MCP expose."""
    return [
        Tool(
            name="search_lost_items",
            description=(
                "Tìm kiếm bài đăng giấy tờ thất lạc, đồ thất lạc, thú cưng thất lạc, "
                "người thân thất lạc, đồ nhặt được tại Việt Nam qua timgiup.com. "
                "Trả về tối đa 20 kết quả với title, description, category, "
                "địa điểm (tỉnh/phường/địa chỉ), ngày xảy ra, ảnh và link bài viết."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": (
                            "Từ khóa tìm kiếm BẮT BUỘC. Hỗ trợ tiếng Việt có dấu. "
                            "Ví dụ: 'cccd', 'ví da', 'chó poodle', 'điện thoại iphone'."
                        ),
                    },
                    "category": {
                        "type": "string",
                        "description": (
                            "Slug danh mục cha (tùy chọn) để lọc. "
                            "Dùng tool list_categories để xem danh sách. "
                            "Ví dụ: 'do-that-lac', 'thu-cung-that-lac'."
                        ),
                    },
                    "province": {
                        "type": "string",
                        "description": (
                            "Mã tỉnh/thành 2 chữ số (tùy chọn) để lọc theo địa lý. "
                            "Dùng tool list_provinces để xem danh sách. "
                            "Ví dụ: '79' = TP HCM, '01' = Hà Nội."
                        ),
                    },
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="list_categories",
            description=(
                "Lấy danh sách 6 danh mục cha trên timgiup.com. "
                "API search chỉ hỗ trợ lọc theo danh mục cha. "
                "Dùng để chọn slug cho tham số 'category' khi gọi search_lost_items."
            ),
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="list_provinces",
            description=(
                "Lấy danh sách 34 tỉnh/thành Việt Nam (sau sáp nhập 2025) "
                "với mã code và tên. Dùng để chọn 'province' khi gọi search_lost_items."
            ),
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Xử lý tool call từ MCP client."""
    if name == "search_lost_items":
        try:
            result = await _client.search(
                query=arguments.get("query", ""),
                category=arguments.get("category"),
                province=arguments.get("province"),
            )
            return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        except ValueError as e:
            return [TextContent(type="text", text=f"Lỗi đầu vào: {e}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Lỗi gọi API: {e}")]

    if name == "list_categories":
        data = _load_json("categories.json")
        return [TextContent(type="text", text=json.dumps(data, ensure_ascii=False, indent=2))]

    if name == "list_provinces":
        data = _load_json("provinces.json")
        return [TextContent(type="text", text=json.dumps(data, ensure_ascii=False, indent=2))]

    return [TextContent(type="text", text=f"Tool không tồn tại: {name}")]


async def _run() -> None:
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main() -> None:
    """Entry point — chạy MCP server qua stdio."""
    asyncio.run(_run())


if __name__ == "__main__":
    main()
