import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from controller.student_controller import StudentController

app = Flask(__name__)

# Cấu hình thư mục upload ảnh
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Khởi tạo database
StudentController.init_db()

# Tạo thư mục lưu ảnh nếu chưa có
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# ======== ROUTE ========= #

@app.route('/')
def home():
    """Trang Home."""
    return render_template('home.html')

@app.route('/students')
def students():
    """Hiển thị danh sách sinh viên, có thể tìm kiếm."""
    q = request.args.get('q', '')  # Lấy từ khoá tìm kiếm nếu có
    list_students = StudentController.get_students(q)
    return render_template('index.html', students=list_students)

@app.route('/add', methods=['GET', 'POST'])
def add():
    """Thêm sinh viên mới."""
    if request.method == 'POST':
        StudentController.add_student(request, app.config['UPLOAD_FOLDER'])
        return redirect(url_for('students'))
    return render_template('add.html')

@app.route('/edit/<int:student_id>', methods=['GET', 'POST'])
def edit(student_id):
    """Sửa thông tin sinh viên."""
    if request.method == 'POST':
        StudentController.update_student(student_id, request, app.config['UPLOAD_FOLDER'])
        return redirect(url_for('students'))
    student = StudentController.get_student_by_id(student_id)
    return render_template('edit.html', student=student)

@app.route('/delete/<int:student_id>')
def delete(student_id):
    """Xoá sinh viên."""
    StudentController.delete_student(student_id)
    return redirect(url_for('students'))

if __name__ == '__main__':
    app.run(debug=True)
