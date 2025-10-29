1️⃣ Chạy bản demo trên PC
 file đã tải (deepfake_demo.zip)

Hướng dẫn:


# 1. Giải nén file
unzip deepfake_demo.zip

# 2. Vào thư mục dự án
cd deepfake_demo

# 3. Tạo virtual environment
python -m venv venv
source venv/bin/activate      # Linux / Mac
venv\Scripts\activate         # Windows

# 4. Cài dependencies
pip install -r requirements.txt

# 5. Khởi tạo database SQLite cho demo
python
>>> from app import db
>>> db.create_all()
>>> exit()

# 6. Chạy ứng dụng
python app.py

Mở trình duyệt vào http://127.0.0.1:5000 để xem demo.
