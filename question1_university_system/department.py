class Course:
    """Represents a university course with enrollment limits and prerequisites."""
    def __init__(self, course_id, name, credits, limit=30, prerequisites=None):
        self.course_id = course_id
        self.name = name
        self.credits = credits
        self.enrollment_limit = limit
        self.prerequisites = set(prerequisites) if prerequisites else set()
        self.students_enrolled = []

    def add_student(self, student):
        if len(self.students_enrolled) < self.enrollment_limit:
            self.students_enrolled.append(student)
            return True
        return False

    def remove_student(self, student):
        if student in self.students_enrolled:
            self.students_enrolled.remove(student)

    def __str__(self):
        return f"{self.course_id}: {self.name} ({self.credits} credits)"

class Department:
    """Manages a collection of courses and faculty for an academic department."""
    def __init__(self, name):
        self.name = name
        self.courses = {}
        self.faculty = []

    def add_course(self, course):
        self.courses[course.course_id] = course

    def add_faculty(self, faculty_member):
        self.faculty.append(faculty_member)
