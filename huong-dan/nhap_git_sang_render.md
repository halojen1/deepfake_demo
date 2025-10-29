Chạy file từ Git trên Render

1. Đăng nhập Render

Truy cập https://render.com → đăng nhập hoặc đăng ký tài khoản mới.



2. Tạo Web Service mới

Nhấn New → Web Service.

Chọn Connect GitHub → chọn repo mà khách đã push code.

Chọn Branch (thường là main).



3. Cấu hình build

Environment: Python 3

Build Command:

pip install -r requirements.txt

Start Command:

python app.py

Environment Variables (nếu có):

Ví dụ: FLASK_ENV=production

Hoặc SECRET_KEY nếu app dùng session.




4. Deploy

Nhấn Create Web Service → Render sẽ tự build và chạy.

Chờ Render hoàn tất → sẽ có URL dạng https://tên-service.onrender.com để xem web trực tiếp.



5. Kiểm tra

Mở URL → kiểm tra đăng nhập, upload video, dashboard…

Mọi tính năng trên web sẽ chạy trực tiếp trên cloud mà không cần PC.
