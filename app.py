import os
import subprocess
from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy

# -------------------- CẤU HÌNH ỨNG DỤNG --------------------
app = Flask(__name__)

# SECRET_KEY cho session Flask
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'mysecretkey')

# -------------------- CẤU HÌNH DATABASE --------------------
# Lấy DATABASE_URL từ Render
uri = os.getenv(
    "DATABASE_URL",
    "postgresql://deepfake_demo:yGvdZK7OLfdYmNZALYqYcvgb8EvGtKbY@dpg-d41benmr433s73drgvr0-a.oregon-postgres.render.com/deepfake_demo"
)

# Render thường trả về 'postgres://', cần sửa lại cho SQLAlchemy
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

# Thêm ?sslmode=require để kết nối an toàn
if "?sslmode=" not in uri:
    uri += "?sslmode=require"

app.config["SQLALCHEMY_DATABASE_URI"] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# -------------------- MODELS --------------------
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Video(db.Model):
    __tablename__ = 'videos'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    result = db.Column(db.String(120))

# -------------------- HÀM PHỤ TRỢ --------------------
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_resolutions(save_path):
    """Tạo các phiên bản video 480p, 720p, 1080p"""
    base, ext = os.path.splitext(save_path)
    resolutions = {
        "480p": "854x480",
        "720p": "1280x720",
        "1080p": "1920x1080"
    }
    for label, size in resolutions.items():
        output = f"{base}_{label}{ext}"
        try:
            subprocess.run([
                "ffmpeg", "-i", save_path, "-vf", f"scale={size}", "-c:a", "copy", output
            ], check=True)
        except Exception as e:
            print(f"Lỗi khi tạo {label}: {e}")

# -------------------- ROUTES --------------------
@app.route('/')
def home():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        if not username or not password:
            flash("Vui lòng nhập đầy đủ thông tin!", "warning")
            return redirect('/register')

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Tên người dùng đã tồn tại!", "danger")
            return redirect('/register')

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("Đăng ký thành công! Hãy đăng nhập.", "success")
        return redirect('/login')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        user = User.query.filter_by(username=username).first()

        if not user:
            flash("Tài khoản không tồn tại!", "danger")
            return redirect(url_for('login'))

        if user.password != password:
            flash("Sai mật khẩu!", "danger")
            return redirect(url_for('login'))

        session['user_id'] = user.id
        flash("Đăng nhập thành công!", "success")
        return redirect(url_for('dashboard'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("Đã đăng xuất.", "info")
    return redirect('/login')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')

    user = db.session.get(User, session['user_id'])

    if request.method == 'POST':
        file = request.files['video']
        if file and allowed_file(file.filename):
            filename = file.filename
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)

            new_video = Video(filename=filename, user_id=user.id, result="Đang xử lý...")
            db.session.add(new_video)
            db.session.commit()

            generate_resolutions(save_path)
            new_video.result = "Hoàn tất xử lý"
            db.session.commit()

    videos = Video.query.filter_by(user_id=user.id).all()
    return render_template('dashboard.html', user=user, videos=videos)

@app.route('/delete_video/<int:video_id>', methods=['POST'])
def delete_video(video_id):
    video = Video.query.get(video_id)
    if video:
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], video.filename)
        if os.path.exists(video_path):
            os.remove(video_path)
        db.session.delete(video)
        db.session.commit()
        flash("Đã xóa video thành công!", "success")
    else:
        flash("Không tìm thấy video!", "danger")
    return redirect(url_for('dashboard'))

# -------------------- KHỞI CHẠY ỨNG DỤNG --------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Tạo bảng nếu chưa có
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
