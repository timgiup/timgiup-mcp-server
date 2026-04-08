# API: `/api/search`

Public REST API tìm kiếm bài đăng trên [timgiup.com](https://timgiup.com).

## Endpoint

```
GET https://timgiup.com/api/search
```

## Tham số

| Tên        | Bắt buộc | Kiểu   | Mô tả                                                                       |
| ---------- | -------- | ------ | --------------------------------------------------------------------------- |
| `q`        | ✅ Có    | string | Từ khóa tìm kiếm. Hỗ trợ tiếng Việt có dấu hoặc không dấu. Không được rỗng. |
| `category` | ❌ Không | string | Slug danh mục cha. Xem [`categories.md`](categories.md).                    |
| `province` | ❌ Không | string | Mã tỉnh/thành (2 chữ số). Xem [`provinces.md`](provinces.md).               |

## Rate Limit

**30 requests / phút / IP**. Vượt quá → HTTP 429.

## Response Schema

### 200 OK

```json
{
  "total": 42,
  "count": 20,
  "query": "cccd",
  "results": [
    {
      "title": "Mất CCCD tại Quận 1",
      "status": "active",
      "description": "Tôi bị mất CCCD vào sáng nay khi đi chợ Bến Thành...",
      "category": "Đồ thất lạc",
      "subcategory": "Tìm giấy tờ tùy thân",
      "created_at": "2026-04-01T17:00:00+07:00",
      "date_event": "2026-03-30",
      "province": "Thành phố Hồ Chí Minh",
      "ward": "Phường Bến Nghé",
      "address": "123 Nguyễn Huệ",
      "source_url": "https://timgiup.com/do-that-lac/mat-cccd-tai-quan-1",
      "images": ["https://timgiup.com/uploads/posts/abc123.jpg"]
    }
  ]
}
```

### Field Reference

| Field                   | Kiểu                 | Mô tả                                   |
| ----------------------- | -------------------- | --------------------------------------- |
| `total`                 | int                  | Tổng số kết quả khớp (toàn bộ DB)       |
| `count`                 | int                  | Số kết quả trả về trong response (≤ 20) |
| `query`                 | string               | Từ khóa đã được trim                    |
| `results[].title`       | string               | Tiêu đề bài đăng                        |
| `results[].status`      | string               | Trạng thái: `active` (đang tìm), `resolved` (đã tìm thấy), `expired` (hết hạn — vẫn hiển thị để tra cứu) |
| `results[].description` | string               | Mô tả chi tiết                          |
| `results[].category`    | string               | Tên danh mục cha (VN)                   |
| `results[].subcategory` | string?              | Tên danh mục con (có thể null)          |
| `results[].created_at`  | string (ISO 8601)    | Thời gian đăng bài (múi giờ Việt Nam +07:00) |
| `results[].date_event`  | string? (YYYY-MM-DD) | Ngày xảy ra sự việc                     |
| `results[].province`    | string?              | Tên tỉnh/thành                          |
| `results[].ward`        | string?              | Tên phường/xã                           |
| `results[].address`     | string?              | Địa chỉ chi tiết                        |
| `results[].source_url`  | string               | URL bài viết gốc trên timgiup.com       |
| `results[].images`      | string[]?            | Mảng URL ảnh tuyệt đối (nếu có)         |

### Errors

| HTTP | Body                                        | Khi nào             |
| ---- | ------------------------------------------- | ------------------- |
| 400  | `{"error":"missing_query","message":"..."}` | `q` rỗng hoặc thiếu |
| 429  | (rate limit)                                | Vượt 30 req/phút    |
| 500  | `{"error":"internal_error"}`                | Lỗi server          |

## Ví dụ cURL

```bash
# Tìm cơ bản
curl 'https://timgiup.com/api/search?q=cccd'

# Lọc theo tỉnh (TP HCM = 79)
curl 'https://timgiup.com/api/search?q=vi+da&province=79'

# Lọc theo danh mục + tỉnh
curl 'https://timgiup.com/api/search?q=cho&category=thu-cung-that-lac&province=01'
```

## Ghi chú

- Trả về bài có status `active`, `resolved` (đã tìm thấy) hoặc `expired` (hết hạn — vẫn có giá trị tra cứu lịch sử).
- Sắp xếp: bài ghim trước, sau đó theo thời gian tạo mới nhất.
- Tìm kiếm normalize tiếng Việt (không phân biệt dấu) — `"vi"` sẽ match `"ví"`.
