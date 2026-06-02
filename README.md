# Salon Management System Backend

Dịch vụ Backend cho Hệ thống Quản lý Salon (Salon Management System), được xây dựng trên nền tảng **Django** và **Django REST Framework (DRF)**, sử dụng cơ sở dữ liệu **SQLite**. 

Hệ thống hỗ trợ quản lý phân quyền chặt chẽ cho 4 vai trò chính: **Customer** (Khách hàng), **Receptionist** (Lễ tân), **Staff** (Nhân viên kỹ thuật), và **Manager** (Quản lý).

---

## 1. Yêu cầu Hệ thống & Thư viện

- **Python**: Phiên bản 3.11 trở lên.
- **Thư viện chính** (Xem chi tiết tại [requirements.txt](file:///d:/project/salon_project/backend/requirements.txt)):
  - `Django>=5.0,<6.0`
  - `djangorestframework>=3.15,<4.0`
  - `djangorestframework-simplejwt>=5.3,<6.0` (Xử lý xác thực JWT)
  - `django-filter>=24.0,<25.0`
  - `django-cors-headers>=4.3,<5.0`

---

## 2. Hướng dẫn Vận hành (Setup & Run)

Thực hiện các bước sau tại thư mục `backend/` để cài đặt và chạy ứng dụng:

### Bước 1: Tạo và kích hoạt môi trường ảo (Virtual Environment)
```bash
# Tạo môi trường ảo .venv
python -m venv .venv

# Kích hoạt môi trường ảo
# Trên Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Trên macOS/Linux:
source .venv/bin/activate
```

### Bước 2: Cài đặt các thư viện phụ thuộc
```bash
pip install -r requirements.txt
```

### Bước 3: Tạo cơ sở dữ liệu và chạy Migrations
```bash
python manage.py migrate
```

### Bước 4: Nạp dữ liệu mẫu (Seed Demo Data)
Hệ thống đã chuẩn bị sẵn câu lệnh nạp dữ liệu mẫu bao gồm danh sách dịch vụ, tài khoản nhân viên, khách hàng và lịch hẹn để tiện chạy thử nghiệm:
```bash
python manage.py seed_demo_data
```

### Bước 5: Tạo tài khoản quản trị Admin (Tùy chọn)
Nếu muốn đăng nhập trang quản trị Django Admin (`http://127.0.0.1:8000/admin/`):
```bash
python manage.py createsuperuser
```

### Bước 6: Khởi chạy máy chủ phát triển
```bash
python manage.py runserver
```
Server chạy mặc định tại địa chỉ: `http://127.0.0.1:8000/`

### Bước 7: Chạy kiểm thử (Tests)
Để chạy các bộ test tự động (unit test, integration test):
```bash
pytest
```

---

## 3. Danh sách Tài khoản Demo (Seeded)

Sau khi chạy lệnh `seed_demo_data`, các tài khoản sau sẽ được khởi tạo với mật khẩu mặc định là **`ChangeMe123!`**:

| Vai trò (Role) | Tên đăng nhập (Username) | Quyền hạn chính |
|---|---|---|
| **Manager** | `manager` | Quản lý toàn bộ hệ thống, xem báo cáo, cấu hình dịch vụ/nhân sự. |
| **Receptionist** | `receptionist` | Tiếp nhận đặt lịch, xác nhận, check-in khách, xuất hóa đơn, thanh toán. |
| **Staff** | `staff1` | Xem lịch làm việc cá nhân, cập nhật trạng thái làm dịch vụ cho khách. |
| **Customer** | `customer1`, `customer2` | Đặt lịch hẹn, xem lịch sử cá nhân, phản hồi/khiếu nại, ví điểm thưởng. |

---

## 4. Tài liệu API (API Endpoints)

Tất cả các API endpoint bắt đầu bằng tiền tố `/api/`. Dưới đây là danh sách chi tiết các API phân theo module:

### Xác thực & Tài khoản (`/api/auth/` & `/api/accounts/`)
- `POST /api/auth/register/` - Đăng ký tài khoản Khách hàng mới.
- `POST /api/auth/login/` - Đăng nhập, trả về JWT Access Token & Refresh Token.
- `POST /api/auth/logout/` - Đăng xuất (xóa phiên làm việc).
- `GET /api/auth/me/` - Xem thông tin tài khoản hiện tại.
- `PATCH /api/auth/me/` - Cập nhật thông tin cá nhân.
- `GET /api/accounts/` - **[Manager]** Danh sách tất cả tài khoản.
- `POST /api/accounts/` - **[Manager]** Tạo tài khoản nhân sự (Lễ tân, Staff, Manager).
- `PATCH /api/accounts/{id}/` - **[Manager]** Cập nhật tài khoản.
- `POST /api/accounts/{id}/deactivate/` - **[Manager]** Khóa/Hủy kích hoạt tài khoản.

### Hồ sơ Khách hàng (`/api/customers/`)
- `GET /api/customers/` - Danh sách khách hàng (Lễ tân/Quản lý xem hết; Khách hàng chỉ xem chính mình).
- `POST /api/customers/` - Tạo hồ sơ khách hàng trực tiếp.
- `GET /api/customers/{id}/` - Xem chi tiết hồ sơ.
- `PATCH /api/customers/{id}/` - Cập nhật thông tin khách hàng.
- `POST /api/customers/{id}/archive/` - Lưu trữ (xóa mềm) hồ sơ khách hàng.
- `GET /api/customers/{id}/history/` - Xem lịch sử làm đẹp, thanh toán, khiếu nại của khách.

### Hồ sơ Nhân sự & Lịch trống (`/api/employees/`)
- `GET /api/employees/` - Danh sách nhân viên.
- `POST /api/employees/` - **[Manager]** Tạo hồ sơ nhân viên mới.
- `GET /api/employees/{id}/` - Xem chi tiết hồ sơ nhân viên.
- `PATCH /api/employees/{id}/` - **[Manager]** Cập nhật hồ sơ nhân viên.
- `POST /api/employees/{id}/archive/` - **[Manager]** Cho nghỉ việc (xóa mềm).
- `GET /api/employees/{id}/availability/` - Xem lịch biểu rảnh/bận của nhân viên.
- `POST /api/employees/{id}/availability/` - **[Manager]** Thêm khung giờ bận/khoá lịch nhân viên.

### Danh mục Dịch vụ (`/api/services/`)
- `GET /api/services/` - Xem danh sách dịch vụ đang hoạt động.
- `POST /api/services/` - **[Manager]** Tạo dịch vụ mới.
- `PATCH /api/services/{id}/` - **[Manager]** Cập nhật thông tin/giá tiền dịch vụ (lưu lịch sử giá).
- `POST /api/services/{id}/archive/` - **[Manager]** Dừng hoạt động dịch vụ (xóa mềm).
- `GET /api/services/{id}/price-history/` - **[Manager]** Xem lịch sử thay đổi giá của dịch vụ.

### Đặt Lịch hẹn (`/api/appointments/`)
- `GET /api/appointments/` - Lịch hẹn (Phân quyền theo vai trò).
- `POST /api/appointments/` - Tạo yêu cầu đặt lịch hẹn mới (Khách hàng hoặc Lễ tân).
- `GET /api/appointments/{id}/` - Xem chi tiết lịch hẹn.
- `PATCH /api/appointments/{id}/` - Cập nhật thông tin lịch hẹn.
- `POST /api/appointments/{id}/confirm/` - **[Receptionist]** Xác nhận lịch hẹn (sau khi hệ thống check lịch trống trùng lặp).
- `POST /api/appointments/{id}/reschedule/` - Đổi lịch hẹn sang ngày/giờ khác.
- `POST /api/appointments/{id}/cancel/` - Hủy lịch hẹn.
- `POST /api/appointments/{id}/arrive/` - **[Receptionist]** Xác nhận khách đã đến cửa hàng.
- `POST /api/appointments/{id}/no-show/` - **[Receptionist]** Đánh dấu khách không đến.
- `GET /api/appointments/availability/` - Kiểm tra khung giờ và nhân viên còn trống cho một dịch vụ.

### Thực thi Dịch vụ (`/api/service-executions/`)
- `GET /api/service-executions/` - Lịch thực hiện dịch vụ (Staff xem việc được giao, Manager xem toàn bộ).
- `POST /api/service-executions/{appointment_id}/start/` - **[Staff]** Bắt đầu làm dịch vụ cho khách.
- `POST /api/service-executions/{id}/incidentals/` - **[Staff]** Thêm phụ phí/sản phẩm phát sinh trong quá trình làm.
- `POST /api/service-executions/{id}/complete/` - **[Staff]** Hoàn thành làm tóc/spa cho khách (ghi chú kết quả).

### Hóa đơn & Thanh toán (`/api/invoices/` & `/api/payments/`)
- `GET /api/invoices/` - Danh sách hóa đơn.
- `POST /api/invoices/from-appointment/{appointment_id}/` - **[Receptionist]** Tạo hóa đơn tạm tính từ lịch hẹn đã hoàn thành.
- `GET /api/invoices/{id}/` - Xem chi tiết hóa đơn.
- `POST /api/invoices/{id}/apply-voucher/` - Áp dụng mã giảm giá voucher vào hóa đơn.
- `POST /api/invoices/{id}/use-reward-points/` - Sử dụng điểm thưởng tích lũy của khách để giảm trừ hóa đơn.
- `POST /api/invoices/{id}/issue/` - Chốt hóa đơn và gửi cho khách.
- `POST /api/invoices/{id}/adjust/` - **[Manager]** Điều chỉnh hóa đơn đã xuất.
- `GET /api/payments/` - Lịch sử giao dịch thanh toán.
- `POST /api/payments/` - Tạo giao dịch thanh toán cho hóa đơn.
- `POST /api/payments/{id}/mark-success/` - Xác nhận thanh toán thành công (khách chuyển khoản/tiền mặt).
- `POST /api/payments/{id}/mark-failed/` - Đánh dấu giao dịch thanh toán thất bại.
- `POST /api/payments/{id}/refund/` - **[Manager]** Hoàn tiền giao dịch.

### Khuyến mãi & Điểm thưởng (`/api/promotions/`, `/api/vouchers/`, `/api/reward-ledger/`)
- `GET /api/promotions/` - Danh sách chương trình khuyến mãi đang chạy.
- `POST /api/promotions/` - **[Manager]** Tạo chương trình khuyến mãi mới.
- `PATCH /api/promotions/{id}/` - **[Manager]** Sửa đổi khuyến mãi.
- `POST /api/promotions/{id}/archive/` - **[Manager]** Kết thúc khuyến mãi trước hạn.
- `GET /api/vouchers/` - Xem voucher cá nhân (Khách hàng) hoặc danh sách voucher phát hành (Manager).
- `POST /api/vouchers/` - **[Manager]** Phát hành mã voucher tặng khách.
- `POST /api/vouchers/{id}/cancel/` - **[Manager]** Hủy voucher đã phát hành.
- `GET /api/reward-ledger/` - Sổ cái tích điểm thưởng của khách.
- `POST /api/reward-ledger/adjust/` - **[Manager]** Cộng/Trừ điểm thưởng thủ công cho khách.

### Phản hồi & Khiếu nại (`/api/feedback/` & `/api/complaints/`)
- `GET /api/feedback/` - Danh sách đánh giá sao của khách sau khi xong dịch vụ.
- `POST /api/feedback/` - Khách hàng viết đánh giá.
- `POST /api/feedback/{id}/respond/` - Lễ tân/Quản lý phản hồi đánh giá của khách.
- `POST /api/feedback/{id}/close/` - Đóng phản hồi.
- `GET /api/complaints/` - Danh sách đơn khiếu nại (Complaints).
- `POST /api/complaints/` - Khách hàng hoặc Lễ tân tạo đơn khiếu nại.
- `POST /api/complaints/{id}/assign/` - Phân công nhân viên giải quyết khiếu nại.
- `POST /api/complaints/{id}/escalate/` - Leo thang khiếu nại lên cấp Quản lý (Manager).
- `POST /api/complaints/{id}/resolve/` - Ghi nhận phương án giải quyết và xử lý xong khiếu nại.
- `POST /api/complaints/{id}/close/` - **[Manager]** Đóng khiếu nại hoàn toàn.

### Trung tâm Thông báo (`/api/notifications/`)
- `GET /api/notifications/` - Danh sách thông báo in-app cá nhân.
- `POST /api/notifications/{id}/mark-read/` - Đánh dấu một thông báo đã đọc.
- `POST /api/notifications/mark-all-read/` - Đánh dấu tất cả thông báo đã đọc.

### Báo cáo Quản trị (`/api/reports/` - **[Chỉ dành cho Manager]**)
- `GET /api/reports/revenue/?from=&to=` - Báo cáo doanh thu theo thời gian.
- `GET /api/reports/appointments/?from=&to=` - Thống kê tỷ lệ hoàn thành/hủy/no-show của các lịch hẹn.
- `GET /api/reports/services/?from=&to=` - Thống kê tần suất sử dụng và doanh số của từng dịch vụ.
- `GET /api/reports/customers/?from=&to=` - Báo cáo chỉ số hoạt động của khách hàng.
- `GET /api/reports/staff-performance/?from=&to=` - Đánh giá hiệu suất phục vụ và đánh giá trung bình của từng kỹ thuật viên.

---

## 5. Quy chuẩn Định dạng Phản hồi lỗi (Error Response Code)
Khi các API xảy ra lỗi nghiệp vụ, mã phản hồi JSON sẽ có định dạng chuẩn:
```json
{
  "error": {
    "code": "appointment_conflict",
    "message": "Nhân viên đã có lịch hẹn trùng lặp trong khung giờ này.",
    "details": {}
  }
}
```
Các mã lỗi chính cần lưu ý:
- `permission_denied`: Quyền truy cập không hợp lệ.
- `appointment_conflict`: Trùng lịch làm việc của nhân viên.
- `invalid_status_transition`: Chuyển trạng thái quy trình không hợp lệ.
- `inactive_service`: Dịch vụ đã bị lưu trữ hoặc ngừng hoạt động.
- `voucher_not_eligible`: Hóa đơn không đủ điều kiện dùng voucher.
- `insufficient_reward_points`: Điểm thưởng không đủ để quy đổi.
- `payment_state_error`: Trạng thái thanh toán không khớp.
