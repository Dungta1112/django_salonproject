### Hướng Dẫn Cài Đặt & Vận Hành (Setup & Deployment)

**Yêu cầu môi trường:** Python 3.10+

### Thiết lập biến môi trường (Environment Variables)
Dự án sử dụng thư viện `python-decouple` giúp ứng dụng quản lý tham số cấu hình linh hoạt. Đặt file có tên `.env` tại thư mục chứa file `manage.py` với nội dung cốt lõi sau:

```env
SECRET_KEY=your_django_secret_key_here
DEBUG=True
# DATABASE_URL=postgres://user:password@localhost:5432/salon_db (Ví dụ Cấu hình PostgreSQL nếu chuyển sang Production)
```

### Cài đặt các phụ thuộc (Dependencies)
Bật Terminal (ưu tiên sử dụng môi trường ảo `venv`), di chuyển vào ổ đĩa và chạy lệnh kết nối tự động:
```bash
pip install -r requirements.txt
```

###  Triển khai Database & Khởi tạo dữ liệu (Migrations & Seed)
Khởi tạo cấu trúc các Schema hệ thống xuống Database (Mặc định dùng SQLite):
```bash
python manage.py makemigrations
python manage.py migrate
```
Nạp dữ liệu chạy thử (Fake data cho services, promotions, appointments):
```bash
python seed.py
```

###  Khởi chạy Server
Bật máy chủ bằng lệnh cơ bản của hệ thống Django:
```bash
python manage.py runserver
```
Server sẽ theo dõi trên cổng gốc: `http://127.0.0.1:8000/`.

---

##  Lược Đồ Cơ Sở Dữ Liệu (Database ER Diagram)
Sơ đồ Entity-Relationship (ERD) minh họa cho mạng lưới dữ liệu Backend dùng kiến trúc lõi dưới đây:

```mermaid
erDiagram
    USER {
        int id PK
        string username
        string email
        string password
        string role "customer | staff | admin"
        string full_name
        string phone
    }

    STYLIST {
        int id PK
        int user_id FK "OneToOne Liên kết xác thực qua bảng USER"
        string nickname
        string specialty
        string avatar
    }

    SERVICE {
        int id PK
        string name
        decimal price
        int duration "Thời lượng tính bằng Phút"
        boolean is_active
    }

    PROMOTION {
        int id PK
        string title
        text content
        date start_date
        date end_date
        decimal discount_percent
        decimal discount_amount
        boolean is_active
    }

    APPOINTMENT {
        int id PK
        int customer_id FK "FK Tới bảng USER định danh khách hàng"
        int service_id FK "FK Tới bảng Dịch Vụ"
        int stylist_id FK "Thợ Cắt Tóc (Null Allowed)"
        int promotion_id FK "Khuyến mãi ép vào (Null Allowed)"
        datetime start_time
        datetime end_time "Được Trigger từ Service.duration"
        string status "pending | confirmed | cancelled | completed | rejected"
        text note
    }

    USER ||--o| STYLIST : "1-1 Mở rộng hồ sơ Thợ cho User.role=staff"
    USER ||--o{ APPOINTMENT : "1 User có thể Book nhiều Lịch"
    SERVICE ||--o{ APPOINTMENT : "Bao gồm"
    STYLIST ||--o{ APPOINTMENT : "Assigned (Được phân lịch)"
    PROMOTION |o--o{ APPOINTMENT : "Áp dụng vào Lịch"
```
