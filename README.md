# Salon Store API

Backend RESTful API cho hệ thống quản lý Salon Tóc bằng Django và Django REST Framework.

## 1. Hướng Dẫn Nhanh (Quick Start)
Cài đặt thư viện: `pip install -r requirements.txt`
Chạy Migrations: `python manage.py makemigrations && python manage.py migrate`
Khởi động Server: `python manage.py runserver`
Chạy Unit Tests: `python manage.py test`

Tài liệu API (Swagger UI): `http://127.0.0.1:8000/swagger/`

---

## 2. Chi Tiết Các Models (Cơ Sở Dữ Liệu)

Dự án sử dụng cơ sở dữ liệu quan hệ chặt chẽ. Dưới đây là các Model chính thống:

### `User` (Kế thừa AbstractUser)
- **Ứng dụng:** `accounts`
- **Mô tả:** Đại diện cho toàn danh tính trên hệ thống. Bất kể là `Customer`, `Staff` hay `Admin`, tất cả đều thuộc `User` kết hợp phân quyền.
- **Trường nổi bật:** `email` (unique - dùng để check trùng), trường `role` phân loại khách/nhân viên, và các trường thông tin cơ bản như `full_name`, `gender`, `phone`.

### `Stylist` (Thợ làm tóc)
- **Ứng dụng:** `stylists`
- **Mô tả:** Được thiết kế quan hệ 1-1 (`OneToOneField`) với bảng `User`. Nếu một User có `role`='staff', họ có thể được gắn thêm hồ sơ Stylist.
- **Trường nổi bật:** `nickname` (tên gọi của thợ), `specialty` (chuyên môn).

### `Service` (Dịch vụ)
- **Ứng dụng:** `services`
- **Mô tả:** Bảng lưu giá trị dịch vụ của Salon.
- **Trường nổi bật:** `price` (giá), `duration` (thời lượng phút - cực kỳ quan trọng để tính thời gian đặt lịch).

### `Promotion` (Khuyến mãi)
- **Ứng dụng:** `promotions`
- **Mô tả:** Các chương trình giảm giá.
- **Trường nổi bật:** `discount_percent`, `discount_amount`, `is_active`, `start_date`, `end_date`.

### `Appointment` (Lịch hẹn)
- **Ứng dụng:** `appointments`
- **Mô tả:** Cốt lõi của hệ thống chứa giao dịch Booking.
- **Trường nổi bật:** 
  - `customer` (Ai đặt), `service` (Cắt cái gì), `stylist` (Ai cắt).
  - `start_time` và `end_time` (Thời gian khung).
  - `status`: ['pending', 'confirmed', 'cancelled', 'completed', 'rejected'].

---

## 3. Chi Tiết Các Serializers (Cầu Nối Dữ Liệu)

Các Serializers vừa làm nhiệm vụ biến đổi Dữ liệu JSON <-> Model, vừa thực thi các luật lệ xác thực (Validation Rules):

### `RegisterSerializer` & `UserSerializer` (`accounts`)
- `RegisterSerializer`: Chỉ cho phép `write_only` ở trường password (để không bị lộ ngược ra ngoài). Hàm `create()` bị ghi đè để băm mật khẩu bằng `create_user()`.
- `UserSerializer`: Làm nhiệm vụ trả về dữ liệu cá nhân (`MeView`). Gần đây đã được thêm tính năng `update()` để bắt trúng các thay đổi mật khẩu (password hash update) nếu Khách hàng yêu cầu đổi khẩu.

### `ServiceSerializer` & `PromotionSerializer`
Ngắn gọn và sử dụng `ModelSerializer` mặc định, chuyển đổi toàn bộ `__all__` qua cấu trúc model. Không có ràng buộc đặc biệt.

### `AppointmentSerializer` (`appointments`)
Là bộ xử lý phức tạp nhất chứa tất cả các Business Logic (nằm tại hàm `validate()`):
- Chặn đặt lịch ngày quá khứ.
- **Kiểm tra giờ làm việc:** Chặn mọi cố gắng đặt lịch ngoài khung **08:00 - 20:00**.
- **Tính toán tự động:** Tự móc nối `service.duration` vào `start_time` để tính ra `end_time` cho lịch hẹn.
- **Kiểm tra Overlap (Trùng Slot):** Quét QuerySet `Appointment.objects.filter(stylist=...)` để chặn đứng bất kỳ người dùng nào định đặt đè lên giờ của một thợ (stylist) đã có lịch `pending/confirmed`.

---

## 4. Chi Tiết Các Views / ViewSets (Luồng Xử Lý API)

Các Views nhận URL và nối với phần Serializers.

### View xác thực (`accounts`)
- `RegisterView` (POST): Công khai, dùng `RegisterSerializer`.
- `MeView` (GET, PUT, PATCH, DELETE): Yêu cầu có gắn token (`IsAuthenticated`), trả về / cập nhật thông tin user hiện hành bằng `request.user`.

### Dịch vụ công cộng lẫn quản lý (`services` & `promotions`)
Sử dụng chuẩn `ModelViewSet` cho phép hỗ trợ toàn bộ các luồng list/retrieve/create/update/delete.
- **Điểm nhấn:** Hàm `get_permissions()` được ghi đè:
  - Nếu là `GET`, trả về `AllowAny` (ai xem web cũng được).
  - Nếu là `POST, PUT, DELETE`, đòi hỏi quyền đặc chế `IsStaffOrAdmin` (chỉ nhân viên Admin mới được thêm sứa xoá menu/khuyến mãi).
- **Bộ lọc (DjangoFilterBackend):** Cung cấp API có khả năng lọc ?name=... hay ?price=... trên URL. Đối với `promotions`, sẽ chỉ `get_queryset` các mảng đã gán `is_active=True` cho Public xem.

### Lõi Booking (`appointments`)
Cũng sử dụng `ModelViewSet`:
- Xử lý quyền hạn mạnh bằng `get_queryset()`:
  - Khi Admin xem, nó trả về toàn bộ danh sách `Appointment.objects.all()`.
  - Nhưng khi Customer xem, nó chỉ trả về lịch cá nhân `Appointment.objects.filter(customer=user)`.
- Gắn Decorator `@action`:
  - `PUT /cancel/`: Dành cho khách hàng. Kèm điều kiện không được ở trạng thái dưới 24 giờ.
  - `PUT /confirm/`, `PUT /complete/`, `PUT /reject/`: Dành riêng cho `IsStaffOrAdmin` thao tác duyệt trạng thái đơn hẹn.
  - Sử dụng giao dịch `.atomic()` tại `perform_create()` để dập tắt nỗi ám ảnh "race condition" nếu có hai thao tác đặt lịch xảy ra cùng một mili-giây.
