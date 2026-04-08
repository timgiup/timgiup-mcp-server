"""HTTP client cho timgiup.com /api/search endpoint."""

from __future__ import annotations

from typing import Any

import httpx


class TimgiupClient:
    """Async client gọi API tìm kiếm bài đăng timgiup.com."""

    def __init__(self, base_url: str = "https://timgiup.com", timeout: float = 15.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    async def search(
        self,
        query: str,
        category: str | None = None,
        province: str | None = None,
    ) -> dict[str, Any]:
        """Gọi GET /api/search.

        Args:
            query: từ khóa tìm kiếm (BẮT BUỘC, không rỗng)
            category: slug danh mục cha (tùy chọn)
            province: mã tỉnh/thành (tùy chọn)

        Returns:
            dict gồm: total, count, query, results[]

        Raises:
            ValueError: query rỗng
            httpx.HTTPStatusError: API trả lỗi
        """
        if not query or not query.strip():
            raise ValueError("query là bắt buộc và không được rỗng")

        params: dict[str, str] = {"q": query.strip()}
        if category:
            params["category"] = category
        if province:
            params["province"] = province

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.get(f"{self.base_url}/api/search", params=params)
            resp.raise_for_status()
            return resp.json()

    async def list_categories(self) -> list[dict[str, Any]]:
        """Gọi GET /api/categories — danh mục cha (slug + name)."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.get(f"{self.base_url}/api/categories")
            resp.raise_for_status()
            return resp.json()

    async def list_provinces(self) -> list[dict[str, Any]]:
        """Gọi GET /api/provinces — 34 tỉnh/thành post-2025 + aliases."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.get(f"{self.base_url}/api/provinces")
            resp.raise_for_status()
            return resp.json()

    async def fetch_text(self, path: str) -> str:
        """Fetch raw text/JSON từ một path (dùng cho openapi.json, llms.txt, RSS)."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.get(f"{self.base_url}{path}")
            resp.raise_for_status()
            return resp.text
