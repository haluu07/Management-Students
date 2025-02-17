import sqlite3
from datetime import datetime

DB_NAME = 'students.db'

class StudentModel:

    @staticmethod
    def init_db():
        """Khởi tạo database."""
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    birthdate TEXT,
                    gender TEXT,
                    department TEXT,
                    gpa REAL,
                    image TEXT
                )
            ''')
            conn.commit()

    @staticmethod
    def get_students():
        """Lấy danh sách sinh viên và định dạng ngày tháng + sắp xếp theo tên chính xác."""
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students")
            students = cursor.fetchall()

        # Chuyển đổi ngày sinh về DD-MM-YYYY và sắp xếp theo tên chính xác (tách tên)
        formatted_students = []
        for student in students:
            student_id, name, birthdate, gender, department, gpa, image = student

            # Chuyển ngày sinh thành định dạng DD-MM-YYYY
            try:
                birthdate = datetime.strptime(birthdate, "%Y-%m-%d").strftime("%d-%m-%Y")
            except ValueError:
                pass  # Giữ nguyên nếu không thể chuyển đổi

            formatted_students.append((student_id, name, birthdate, gender, department, gpa, image))

        # Sắp xếp theo tên thay vì họ
        formatted_students.sort(key=lambda x: x[1].split()[-1])  # Lấy phần cuối cùng của tên

        return formatted_students

    @staticmethod
    def search_students(keyword):
        """Tìm sinh viên theo tên (tìm theo tất cả từ khóa trong tên)."""
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students WHERE name LIKE ?", ('%' + keyword + '%',))
            students = cursor.fetchall()

        # Định dạng ngày tháng và sắp xếp trước khi trả về
        formatted_students = []
        for student in students:
            student_id, name, birthdate, gender, department, gpa, image = student
            try:
                birthdate = datetime.strptime(birthdate, "%Y-%m-%d").strftime("%d-%m-%Y")
            except ValueError:
                pass

            formatted_students.append((student_id, name, birthdate, gender, department, gpa, image))

        formatted_students.sort(key=lambda x: x[1].split()[-1])  # Sắp xếp theo tên thật sự
        return formatted_students

    @staticmethod
    def get_student_by_id(student_id):
        """Lấy thông tin sinh viên theo ID."""
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students WHERE id=?", (student_id,))
            student = cursor.fetchone()
        return student

    @staticmethod
    def add_student(name, birthdate, gender, department, gpa, image=None):
        """Thêm sinh viên vào database."""
        # Chuyển đổi ngày về chuẩn CSDL (YYYY-MM-DD)
        try:
            birthdate = datetime.strptime(birthdate, "%d-%m-%Y").strftime("%Y-%m-%d")
        except ValueError:
            pass  # Nếu sai định dạng, giữ nguyên

        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO students (name, birthdate, gender, department, gpa, image)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, birthdate, gender, department, gpa, image))
            conn.commit()

    @staticmethod
    def update_student(student_id, name, birthdate, gender, department, gpa, image=None):
        """Cập nhật thông tin sinh viên."""
        try:
            birthdate = datetime.strptime(birthdate, "%d-%m-%Y").strftime("%Y-%m-%d")
        except ValueError:
            pass  # Nếu sai định dạng, giữ nguyên

        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            if image:
                cursor.execute("""
                    UPDATE students
                    SET name=?, birthdate=?, gender=?, department=?, gpa=?, image=?
                    WHERE id=?
                """, (name, birthdate, gender, department, gpa, image, student_id))
            else:
                cursor.execute("""
                    UPDATE students
                    SET name=?, birthdate=?, gender=?, department=?, gpa=?
                    WHERE id=?
                """, (name, birthdate, gender, department, gpa, student_id))
            conn.commit()

    @staticmethod
    def delete_student(student_id):
        """Xóa sinh viên khỏi database."""
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
            conn.commit()
