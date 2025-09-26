from person import Person

class Student(Person):
    """Represents a student, extending Person with academic details."""
    def __init__(self, person_id, name, birth_date, major):
        super().__init__(person_id, name, birth_date)
        self.major = major
        self.enrolled_courses = {}  # {course_id: grade}
        self.gpa = 0.0

    def enroll_course(self, course, department):
        # Prerequisite check
        completed_courses = set(self.enrolled_courses.keys())
        if not course.prerequisites.issubset(completed_courses):
            missing = course.prerequisites - completed_courses
            print(f"Enrollment failed: Missing prerequisites for {course.name}: {', '.join(missing)}")
            return

        if course.add_student(self):
            self.enrolled_courses[course.course_id] = None  # No grade yet
            print(f"{self.name} enrolled in {course.name}.")
        else:
            print(f"Enrollment failed: {course.name} is full.")

    def drop_course(self, course):
        if course.course_id in self.enrolled_courses:
            course.remove_student(self)
            del self.enrolled_courses[course.course_id]
            print(f"{self.name} dropped {course.name}.")

    def calculate_gpa(self):
        # Simplified GPA calculation
        total_points = 0
        total_credits = 0 # This is a placeholder; a real system would need course credits
        grade_points = {'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0}

        for course_id, grade in self.enrolled_courses.items():
            if grade and grade in grade_points:
                total_points += grade_points[grade] * 3 # Assume 3 credits per course
                total_credits += 3

        if total_credits == 0:
            self.gpa = 0.0
            return 0.0

        self.gpa = round(total_points / total_credits, 2)
        return self.gpa

    def get_academic_status(self):
        self.calculate_gpa()
        if self.gpa >= 3.5:
            return "Dean's List"
        elif self.gpa >= 2.0:
            return "Good Standing"
        else:
            return "Probation"

    def get_responsibilities(self):
        base_resp = super().get_responsibilities()
        base_resp.append("Attend classes and complete coursework.")
        return base_resp

class UndergraduateStudent(Student):
    def __init__(self, person_id, name, birth_date, major, year_level):
        super().__init__(person_id, name, birth_date, major)
        self.year_level = year_level

class GraduateStudent(Student):
    def __init__(self, person_id, name, birth_date, major, advisor):
        super().__init__(person_id, name, birth_date, major)
        self.advisor = advisor

class SecureStudentRecord:
    """Demonstrates encapsulation with private attributes and validation."""
    def __init__(self, student, initial_gpa=0.0):
        self.__student = student
        self.__gpa = 0.0
        self.set_gpa(initial_gpa)
        self.__enrollment_limit = 5

    # Getter for GPA
    def get_gpa(self):
        return self.__gpa

    # Setter for GPA with validation
    def set_gpa(self, new_gpa):
        if 0.0 <= new_gpa <= 4.0:
            self.__gpa = new_gpa
        else:
            raise ValueError("GPA must be between 0.0 and 4.0")

    def can_enroll_more(self):
        # Data integrity check
        return len(self.__student.enrolled_courses) < self.__enrollment_limit

    def get_student_name(self):
        return self.__student.name
