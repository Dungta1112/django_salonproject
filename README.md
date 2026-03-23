# Hệ Thống Quản Lý Đặt Lịch Salon Tóc (API Backend)

## 1. Giới thiệu Tổng quan
Dự án phát triển hệ thống RESTful API phục vụ nền tảng quản lý Salon Tóc chuyên nghiệp, được thiết kế trên lõi giải pháp **Django** và **Django REST Framework (DRF)**. Hệ thống cung cấp giải pháp Backend số hóa toàn diện giúp kết nối Khách hàng với các dịch vụ chăm sóc sắc đẹp, đồng thời cung cấp công cụ để Ban quản trị (Admin) và Nhân sự (Staff) vận hành salon một cách tối ưu, tập trung vào tính toàn vẹn dữ liệu.

## 2. Kiến trúc Bảo mật & Phân quyền (Authentication & Authorization)
Hệ thống sử dụng cơ chế xác thực **JSON Web Token (JWT)**, đảm bảo hiệu năng bảo mật cao và tính phi trạng thái (stateless) trong quá trình giao tiếp giữa các nền tảng (Web/App) và Server.
Cơ chế Phân quyền (Role-based Access Control) được chia làm 3 cấp độ truy cập rõ rệt:
- **Người dùng Vô danh (Guest):** Chỉ có quyền truy cập Đọc (Read-only) đối với các danh mục Dịch vụ và Khuyến mãi đang ở trạng thái kích hoạt.
- **Khách hàng (Customer):** Được cấp quyền xem thông tin hồ sơ cá nhân, thực hiện thao tác tạo mới lịch hẹn và tra cứu/hủy các lịch hẹn thuộc sở hữu cá nhân.
- **Quản trị viên / Nhân sự (Admin / Staff):** Toàn quyền kiểm soát (Create/Update/Delete) danh mục Dịch vụ, Khuyến mãi và nắm quyền thao tác xét duyệt (Xác nhận, Từ chối, Hoàn thành) các luồng lịch hẹn của toàn hệ thống.

## 3. Các Phân hệ Tính năng Lõi (API Features)

### 3.1. Phân hệ Quản lý Tài khoản (Account Management APIs)
- **Định danh An toàn:** Chịu trách nhiệm cho luồng Đăng ký và Đăng nhập. Hệ thống tự động cấp phát bộ đôi Access/Refresh Token. Toàn bộ mật khẩu của người dùng được băm (Hash Algorithms) tiêu chuẩn thay vì lưu trữ dưới dạng văn bản thuần, chống lại các nguy cơ lộ lọt dữ liệu.
- **Quản lý Hồ sơ:** Cung cấp luồng dữ liệu trích xuất hồ sơ cá nhân độc lập (`/api/auth/me/`) cho người dùng đã xác thực, đi kèm chức năng cập nhật thông tin và cập nhật mật khẩu mã hóa an toàn.

### 3.2. Phân hệ Dịch Vụ và Khuyến Mãi (Catalog APIs)
- **Truy xuất Danh mục:** Cung cấp luồng dữ liệu danh sách Dịch Vụ và Khuyến Mãi cho thiết bị đầu cuối với bộ lọc (Filtering) động dựa theo tên (`name`), giá (`price`). Chỉ phơi bày thông tin của các chương trình đang thực thụ khả dụng (`is_active=True`).
- **Nghiệp vụ Quản trị:** Cơ chế Custom Permissions khước từ mọi truy cập cố gắng tác động làm thay đổi cấu trúc bảng giá hoặc bổ sung/xóa chương trình khuyến mãi nếu phát hiện luồng truy cập không đến từ tài khoản Nhân sự nội bộ.

### 3.3. Phân hệ Xử lý Đặt Lịch Hẹn (Booking Engine APIs)
Đây là Module điều phối cốt lõi với hàng loạt quy tắc nghiệp vụ (Business Rules) khắt khe được tích hợp nhằm đảm bảo tính logic tuyệt đối của một Salon thực tiễn:
- **Thuật toán Ngăn chặn Xung đột (Overlapping Constraint):** Tự động truy vấn và phát hiện nhằm chặn đứng các luồng giao dịch đặt lịch trên cùng một nhân sự (Stylist) nếu quỹ thời gian đó đã có lịch hẹn đang chờ duyệt (`pending`) hoặc đã chốt (`confirmed`).
- **Ràng buộc Giờ Hành Chính (Working Hours Limits):** Từ chối mọi yêu cầu ngoại tuyến. Khách hàng chỉ được phép giao dịch trong quỹ thời gian mở cửa (Từ 08:00 sáng và kết thúc muộn nhất vào 20:00 tối).
- **Đồng bộ Thời lượng (Duration Sync):** Việc xác thực đầu vào luôn tự động móc nối độ dài dịch vụ (`duration` / tính bằng phút) để bù trừ và quy đổi chính xác Giờ kết thúc (`end_time`). Không phụ thuộc vào dữ liệu tính toán từ Client frontend nhằm loại bỏ rủi ro sai lệch.
- **Quản lý Cạnh tranh Dữ liệu (Transaction Integrity):** Lõi ghi chép DB khi Booking được bọc lót bởi cơ chế `transaction.atomic()`, giúp ngăn chặn hoàn toàn "Race Condition" nếu hệ thống đón nhận hàng loạt thao tác tranh giành đặt lịch tập trung trong cùng 1 mili-giây.
- **Chính sách Trạng thái (Status Flow):**
  - Ràng buộc chặn khách hàng tự ý hủy (`cancel`) nếu tính từ thời điểm bấm hủy đến giờ cắt tóc chưa đủ 24 tiếng.
  - Cung cấp các Restful Action riêng biệt (`confirm`, `complete`, `reject`) cho Admin để thao tác duyệt trạng thái đơn hẹn, giúp tách biệt logic kinh doanh với logic cập nhật dữ liệu thông thường.

## 4. Tài Liệu Hóa Tự Động (API Documentation)
Thay vì duy trì tài liệu thủ công, toàn bộ danh sách Endpoint được tài liệu hóa tự động dựa trên cấu trúc mã nguồn theo chuẩn công nghiệp **OpenAPI**. Nền tảng được xuất bản trực tuyến thông qua giao diện `Swagger UI` trực quan hóa và `ReDoc`, mang lại quy trình làm việc phối hợp nhanh gọn nhất đối với các Frontend Developer hay đơn vị kiểm thử (QA/Tester).
