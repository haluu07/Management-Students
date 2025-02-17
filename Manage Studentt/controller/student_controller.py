import os
from werkzeug.utils import secure_filename
from model.student_model import StudentModel

class StudentController:
    
    @staticmethod
    def init_db():
        """Khởi tạo database."""
        StudentModel.init_db()

    @staticmethod
    def get_students(search_query=""):
        """Lấy danh sách sinh viên, có thể tìm kiếm theo tên."""
        if search_query:
            return StudentModel.search_students(search_query)
        return StudentModel.get_students()

    @staticmethod
    def get_student_by_id(student_id):
        """Lấy thông tin một sinh viên theo ID."""
        return StudentModel.get_student_by_id(student_id)

    @staticmethod
    def add_student(request, upload_folder):
        """Thêm sinh viên mới."""
        name = request.form['name']
        birthdate = request.form['birthdate']
        gender = request.form['gender']
        department = request.form['department']
        gpa = float(request.form['gpa']) if request.form['gpa'] else 0.0

        # Xử lý file ảnh
        file = request.files.get('image')
        image_filename = None
        if file and StudentController.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(upload_folder, filename))
            image_filename = filename

        StudentModel.add_student(name, birthdate, gender, department, gpa, image_filename)

    @staticmethod
    def update_student(student_id, request, upload_folder):
        """Cập nhật thông tin sinh viên."""
        name = request.form['name']
        birthdate = request.form['birthdate']
        gender = request.form['gender']
        department = request.form['department']
        gpa = float(request.form['gpa']) if request.form['gpa'] else 0.0

        # Xử lý file ảnh
        file = request.files.get('image')
        image_filename = None
        if file and StudentController.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(upload_folder, filename))
            image_filename = filename

        StudentModel.update_student(student_id, name, birthdate, gender, department, gpa, image_filename)

    @staticmethod
    def delete_student(student_id):
        """Xóa sinh viên."""
        StudentModel.delete_student(student_id)

    @staticmethod
    def allowed_file(filename):
        """Kiểm tra file ảnh có hợp lệ không."""
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
