# Provinces — 34 Tỉnh/Thành Việt Nam (sau sáp nhập 2025)

Việt Nam đã sáp nhập từ 63 → 34 tỉnh/thành. File JSON kèm theo cung cấp **alias** (tên cũ) để AI Agent ánh xạ về `code` mới khi gọi API `/api/search`.

JSON: [`mcp_server/data/provinces.json`](../mcp_server/data/provinces.json)

| Code | Tên hiện tại | Tên cũ (aliases) |
|------|--------------|------------------|
| `01` | Thành phố Hà Nội | — |
| `04` | Cao Bằng | — |
| `08` | Tuyên Quang | Hà Giang |
| `11` | Điện Biên | — |
| `12` | Lai Châu | — |
| `14` | Sơn La | — |
| `15` | Lào Cai | Yên Bái |
| `19` | Thái Nguyên | Bắc Kạn |
| `20` | Lạng Sơn | — |
| `22` | Quảng Ninh | — |
| `24` | Bắc Ninh | Bắc Giang |
| `25` | Phú Thọ | Vĩnh Phúc, Hòa Bình |
| `31` | Thành phố Hải Phòng | Hải Dương |
| `33` | Hưng Yên | Thái Bình |
| `37` | Ninh Bình | Hà Nam, Nam Định |
| `38` | Thanh Hóa | — |
| `40` | Nghệ An | — |
| `42` | Hà Tĩnh | — |
| `44` | Quảng Trị | Quảng Bình |
| `46` | Thành phố Huế | — |
| `48` | Thành phố Đà Nẵng | Quảng Nam |
| `51` | Quảng Ngãi | Kon Tum |
| `52` | Gia Lai | Bình Định |
| `56` | Khánh Hòa | Ninh Thuận |
| `66` | Đắk Lắk | Phú Yên |
| `68` | Lâm Đồng | Đắk Nông, Bình Thuận |
| `75` | Đồng Nai | Bình Phước |
| `79` | Thành phố Hồ Chí Minh | Bà Rịa - Vũng Tàu, Bình Dương |
| `80` | Tây Ninh | Long An |
| `82` | Đồng Tháp | Tiền Giang |
| `86` | Vĩnh Long | Bến Tre, Trà Vinh |
| `91` | An Giang | Kiên Giang |
| `92` | Thành phố Cần Thơ | Sóc Trăng, Hậu Giang |
| `96` | Cà Mau | Bạc Liêu |

## Cách dùng

API `/api/search` chỉ chấp nhận **code mới** (2 chữ số). Khi user nhắc tới tên tỉnh cũ (vd "Bình Dương", "Kiên Giang"), AI Agent nên:
1. Gọi tool `list_provinces` để lấy bảng mapping
2. Tìm `code` mà alias chứa tên cũ
3. Truyền `code` đó vào `province` của `search_lost_items`

Ví dụ: user hỏi "tìm CCCD ở Bình Dương" → AI map "Bình Dương" → code `79` (TP HCM) → gọi `search_lost_items(query="cccd", province="79")`.
