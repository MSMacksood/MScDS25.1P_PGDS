"""
Department Module - Academic Organization Classes

This module contains classes that represent the organizational structure of
the university's academic departments and courses. It handles course enrollment
management, prerequisite tracking, and departmental faculty organization.

Classes:
    Course: Represents individual courses with enrollment and prerequisite management
    Department: Manages collections of courses and faculty for academic departments
"""


class Course:
    """
    Represents a university course with enrollment limits and prerequisites.

    This class manages course information, student enrollment, and prerequisite
    validation. It provides the core functionality for course registration
    and capacity management within the university system.

    Attributes:
        course_id (str): Unique identifier for the course (e.g., "CS101")
        name (str): Descriptive name of the course
        credits (int): Number of credit hours the course is worth
        enrollment_limit (int): Maximum number of students who can enroll
        prerequisites (set): Set of course_ids required before taking this course
        students_enrolled (list): List of Student objects currently enrolled
    """

    def __init__(self, course_id, name, credits, limit=30, prerequisites=None):
        """
        Initialize a Course with basic information and constraints.

        Args:
            course_id (str): Unique identifier for the course
            name (str): Descriptive name of the course
            credits (int): Number of credit hours
            limit (int, optional): Maximum enrollment capacity. Defaults to 30.
            prerequisites (list, optional): List of prerequisite course_ids. Defaults to None.
        """
        self.course_id = course_id
        self.name = name
        self.credits = credits
        self.enrollment_limit = limit

        # Convert prerequisites list to set for efficient subset operations
        # Use empty set if no prerequisites provided
        self.prerequisites = set(prerequisites) if prerequisites else set()

        # Initialize empty enrollment list
        self.students_enrolled = []

    def add_student(self, student):
        """
        Attempt to add a student to the course enrollment.

        Checks enrollment capacity before adding the student. This method
        is typically called by the Student.enroll_course() method after
        prerequisite validation.

        Args:
            student: Student object to add to enrollment

        Returns:
            bool: True if student was successfully added, False if course is full
        """
        # Check if there's capacity for another student
        if len(self.students_enrolled) < self.enrollment_limit:
            self.students_enrolled.append(student)
            return True  # Successfully enrolled
        return False  # Course is full

    def remove_student(self, student):
        """
        Remove a student from the course enrollment.

        This method is typically called when a student drops the course.
        It safely handles cases where the student might not be enrolled.

        Args:
            student: Student object to remove from enrollment
        """
        # Only remove if student is actually enrolled
        if student in self.students_enrolled:
            self.students_enrolled.remove(student)

    def __str__(self):
        """
        Return a string representation of the course.

        Returns:
            str: Formatted string with course ID, name, and credits
        """
        return f"{self.course_id}: {self.name} ({self.credits} credits)"


class Department:
    """
    Manages a collection of courses and faculty for an academic department.

    This class represents an academic department within the university and
    provides organizational structure for courses and faculty members. It
    serves as a container and management interface for departmental resources.

    Attributes:
        name (str): Name of the academic department
        courses (dict): Dictionary mapping course_id to Course objects
        faculty (list): List of Faculty objects assigned to this department
    """

    def __init__(self, name):
        """
        Initialize a Department with a name and empty collections.

        Args:
            name (str): Name of the academic department
        """
        self.name = name
        # Use dictionary for courses to enable fast lookup by course_id
        self.courses = {}
        # Use list for faculty as order might matter and lookups are less frequent
        self.faculty = []

    def add_course(self, course):
        """
        Add a course to the department's course catalog.

        Courses are stored in a dictionary with course_id as the key for
        efficient lookup during enrollment operations.

        Args:
            course: Course object to add to the department
        """
        self.courses[course.course_id] = course

    def add_faculty(self, faculty_member):
        """
        Add a faculty member to the department.

        Faculty members are maintained in a list to preserve order and
        allow for multiple faculty members with similar roles.

        Args:
            faculty_member: Faculty object to add to the department
        """
        self.faculty.append(faculty_member)
