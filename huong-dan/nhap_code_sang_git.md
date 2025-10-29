
Hướng dẫn đẩy code lên Git từ PC

1. Chuẩn bị

Giải nén file dự án (deepfake_demo.zip) ra một thư mục trên PC.

Cài Git nếu chưa có:

Windows: tải Git for Windows và cài.

Mac/Linux: sudo apt install git (Linux) hoặc brew install git (Mac).




2. Khởi tạo repository và commit code

cd đường_dẫn_đến_thư_mục_deepfake_demo  # ví dụ: cd C:\Users\Khach\deepfake_demo
git init                                 # tạo repo local
git add .                                 # thêm tất cả file vào stage
git commit -m "Initial commit"           # commit lần đầu


3. Tạo repository trên GitHub

Vào GitHub → New repository → đặt tên (ví dụ: deepfake_demo) → tạo.

Sao chép URL HTTPS của repo mới (ví dụ: https://github.com/khach/deepfake_demo.git).



4. Kết nối repo local với GitHub và push code

git remote add origin https://github.com/khach/deepfake_demo.git
git branch -M main
git push -u origin main


5. Xác nhận

Vào GitHub → repo → thấy tất cả file đã được đẩy lên.
