"""MCP server expose tools + resources cho AI Agent tìm kiếm đồ thất lạc tại Việt Nam."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, TextContent, Tool
from pydantic import AnyUrl

from .client import TimgiupClient

TIMGIUP_BASE_URL = "https://timgiup.com"

# Khởi tạo server + client
_client = TimgiupClient(base_url=TIMGIUP_BASE_URL)
server: Server = Server("timgiup-mcp")


# Danh sách MCP Resources expose ra cho AI Agent — cho phép đọc trực tiếp
# các file public (OpenAPI spec, llms.txt, RSS feeds) mà không cần tool call.
# URI scheme dùng https:// để client trực quan dễ hiểu.
_RESOURCES: list[tuple[str, str, str, str]] = [
    (
        f"{TIMGIUP_BASE_URL}/openapi.json",
        "OpenAPI 3.1 Specification",
        "Full machine-readable API spec (OAS 3.1.0) — paste vào codegen tool để sinh client tự động",
        "application/json",
    ),
    (
        f"{TIMGIUP_BASE_URL}/llms.txt",
        "llms.txt — AI/LLM Discovery Guide",
        "Index theo chuẩn llmstxt.org liệt kê API, MCP, RSS, sitemap để AI/LLM hiểu website",
        "text/plain",
    ),
    (
        f"{TIMGIUP_BASE_URL}/rss/tat-ca.rss",
        "RSS — Tất cả bài đăng",
        "Feed RSS 2.0 chứa 20 bài đăng mới nhất từ tất cả danh mục",
        "application/rss+xml",
    ),
    (
        f"{TIMGIUP_BASE_URL}/rss/do-that-lac.rss",
        "RSS — Đồ thất lạc",
        "Feed RSS bài đăng đồ thất lạc (điện thoại, ví, giấy tờ, ...)",
        "application/rss+xml",
    ),
    (
        f"{TIMGIUP_BASE_URL}/rss/thu-cung-that-lac.rss",
        "RSS — Thú cưng thất lạc",
        "Feed RSS bài đăng thú cưng thất lạc",
        "application/rss+xml",
    ),
    (
        f"{TIMGIUP_BASE_URL}/rss/nguoi-than-that-lac.rss",
        "RSS — Người thân thất lạc",
        "Feed RSS bài đăng tìm người thân thất lạc",
        "application/rss+xml",
    ),
    (
        f"{TIMGIUP_BASE_URL}/rss/do-nhat-duoc.rss",
        "RSS — Đồ nhặt được",
        "Feed RSS bài đăng đồ nhặt được, chờ trả lại chủ",
        "application/rss+xml",
    ),
    (
        f"{TIMGIUP_BASE_URL}/sitemap.xml",
        "Sitemap Index",
        "Root sitemap index cho SEO crawler",
        "application/xml",
    ),
]


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
                "Lấy danh sách 6 danh mục cha trên timgiup.com (live từ /api/categories). "
                "API search chỉ hỗ trợ lọc theo danh mục cha. "
                "Dùng để chọn slug cho tham số 'category' khi gọi search_lost_items."
            ),
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="list_provinces",
            description=(
                "Lấy danh sách 34 tỉnh/thành Việt Nam (sau sáp nhập 2025) "
                "với mã code, tên hiện tại và 'aliases' (tên cũ trước sáp nhập). "
                "Live từ /api/provinces. "
                "Dùng để chọn 'province' khi gọi search_lost_items. "
                "Khi user nhắc tỉnh cũ (vd 'Bình Dương', 'Kiên Giang'), tìm code "
                "mà aliases chứa tên đó và dùng code mới."
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
        try:
            data = await _client.list_categories()
            return [TextContent(type="text", text=json.dumps(data, ensure_ascii=False, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"Lỗi gọi API: {e}")]

    if name == "list_provinces":
        try:
            data = await _client.list_provinces()
            return [TextContent(type="text", text=json.dumps(data, ensure_ascii=False, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"Lỗi gọi API: {e}")]

    return [TextContent(type="text", text=f"Tool không tồn tại: {name}")]


@server.list_resources()
async def list_resources() -> list[Resource]:
    """Expose các tài nguyên public (OpenAPI, llms.txt, RSS, sitemap) như MCP Resources."""
    return [
        Resource(
            uri=AnyUrl(uri),
            name=name,
            description=desc,
            mimeType=mime,
        )
        for uri, name, desc, mime in _RESOURCES
    ]


@server.read_resource()
async def read_resource(uri: AnyUrl) -> str:
    """Fetch nội dung resource từ timgiup.com."""
    uri_str = str(uri)
    if not uri_str.startswith(TIMGIUP_BASE_URL):
        raise ValueError(f"URI không thuộc timgiup.com: {uri_str}")
    path = uri_str[len(TIMGIUP_BASE_URL):]
    return await _client.fetch_text(path)


async def _run() -> None:
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main() -> None:
    """Entry point — chạy MCP server qua stdio."""
    asyncio.run(_run())


if __name__ == "__main__":
    main()
