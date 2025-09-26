"""
Student Module - Student Classes and Academic Records

This module contains all student-related classes including the base Student class,
specialized student types (Undergraduate/Graduate), and secure record management.
It demonstrates inheritance hierarchy, academic business logic, and encapsulation principles.

Classes:
    Student: Base class for all students with academic functionality
    UndergraduateStudent: Students pursuing bachelor's degrees
    GraduateStudent: Students pursuing advanced degrees
    SecureStudentRecord: Encapsulated record management with data validation
"""

from person import Person


class Student(Person):
    """
    Represents a student, extending Person with academic details.

    This class handles core academic functionality including course enrollment,
    GPA calculation, and academic status determination. It serves as the base
    class for all student types in the university system.

    Attributes:
        major (str): Student's declared field of study
        enrolled_courses (dict): Maps course_id to grade (None if no grade yet)
        gpa (float): Current Grade Point Average
    """

    def __init__(self, person_id, name, birth_date, major):
        """
        Initialize a Student with personal and academic information.

        Args:
            person_id (str): Unique identifier for the student
            name (str): Full name of the student
            birth_date (str): Birth date in YYYY-MM-DD format
            major (str): Student's declared field of study
        """
        # Initialize base Person attributes
        super().__init__(person_id, name, birth_date)
        self.major = major
        self.enrolled_courses = {}  # Dictionary mapping course_id to grade
        self.gpa = 0.0

    def enroll_course(self, course, department):
        """
        Attempt to enroll the student in a course.

        Performs prerequisite validation and capacity checking before enrollment.
        Updates both the student's enrolled courses and the course's student list.

        Args:
            course: Course object to enroll in
            department: Department object (currently unused but kept for interface consistency)
        """
        # Check if student has completed all prerequisites
        completed_courses = set(self.enrolled_courses.keys())
        if not course.prerequisites.issubset(completed_courses):
            # Calculate which prerequisites are missing
            missing = course.prerequisites - completed_courses
            print(f"Enrollment failed: Missing prerequisites for {course.name}: {', '.join(missing)}")
            return

        # Attempt to add student to course (handles capacity checking)
        if course.add_student(self):
            # Add course to student's enrolled courses with no grade initially
            self.enrolled_courses[course.course_id] = None
            print(f"{self.name} enrolled in {course.name}.")
        else:
            print(f"Enrollment failed: {course.name} is full.")

    def drop_course(self, course):
        """
        Drop a course that the student is currently enrolled in.

        Removes the student from both their enrolled courses list and
        the course's student enrollment list.

        Args:
            course: Course object to drop
        """
        if course.course_id in self.enrolled_courses:
            # Remove student from course enrollment
            course.remove_student(self)
            # Remove course from student's enrolled courses
            del self.enrolled_courses[course.course_id]
            print(f"{self.name} dropped {course.name}.")

    def calculate_gpa(self):
        """
        Calculate and update the student's GPA based on completed courses.

        Uses a simplified 4.0 scale with standard letter grade mappings.
        Only includes courses with assigned grades in the calculation.

        Returns:
            float: Calculated GPA rounded to 2 decimal places
        """
        total_points = 0
        total_credits = 0  # Note: Using fixed 3 credits per course for simplification

        # Standard grade point mapping
        grade_points = {'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0}

        # Calculate total points and credits for graded courses
        for course_id, grade in self.enrolled_courses.items():
            if grade and grade in grade_points:
                total_points += grade_points[grade] * 3  # Assuming 3 credits per course
                total_credits += 3

        # Handle case where no graded courses exist
        if total_credits == 0:
            self.gpa = 0.0
            return 0.0

        # Calculate and store GPA
        self.gpa = round(total_points / total_credits, 2)
        return self.gpa

    def get_academic_status(self):
        """
        Determine the student's academic standing based on current GPA.

        Returns:
            str: Academic status classification
                - "Dean's List": GPA >= 3.5
                - "Good Standing": GPA >= 2.0
                - "Probation": GPA < 2.0
        """
        # Update GPA before determining status
        self.calculate_gpa()

        if self.gpa >= 3.5:
            return "Dean's List"
        elif self.gpa >= 2.0:
            return "Good Standing"
        else:
            return "Probation"

    def get_responsibilities(self):
        """
        Get the list of responsibilities specific to students.

        Returns:
            list: List of responsibility strings including academic duties
        """
        # Get base responsibilities from Person class
        base_resp = super().get_responsibilities()
        # Add student-specific responsibility
        base_resp.append("Attend classes and complete coursework.")
        return base_resp


class UndergraduateStudent(Student):
    """
    Represents an undergraduate student pursuing a bachelor's degree.

    Extends the base Student class with undergraduate-specific attributes
    such as academic year level.

    Attributes:
        year_level (int): Current academic year (1=Freshman, 2=Sophomore, etc.)
    """

    def __init__(self, person_id, name, birth_date, major, year_level):
        """
        Initialize an UndergraduateStudent.

        Args:
            person_id (str): Unique identifier for the student
            name (str): Full name of the student
            birth_date (str): Birth date in YYYY-MM-DD format
            major (str): Student's declared field of study
            year_level (int): Current academic year level
        """
        # Initialize base Student attributes
        super().__init__(person_id, name, birth_date, major)
        self.year_level = year_level


class GraduateStudent(Student):
    """
    Represents a graduate student pursuing an advanced degree.

    Extends the base Student class with graduate-specific attributes
    such as faculty advisor assignment.

    Attributes:
        advisor (str): Name or ID of the faculty advisor
    """

    def __init__(self, person_id, name, birth_date, major, advisor):
        """
        Initialize a GraduateStudent.

        Args:
            person_id (str): Unique identifier for the student
            name (str): Full name of the student
            birth_date (str): Birth date in YYYY-MM-DD format
            major (str): Student's declared field of study
            advisor (str): Name or ID of the faculty advisor
        """
        # Initialize base Student attributes
        super().__init__(person_id, name, birth_date, major)
        self.advisor = advisor


class SecureStudentRecord:
    """
    Demonstrates encapsulation with private attributes and validation.

    This class provides a secure interface for managing student academic records
    with data validation and access control. It shows how to properly implement
    encapsulation using private attributes and getter/setter methods.

    Private Attributes:
        __student: Reference to the Student object
        __gpa: Securely stored GPA value
        __enrollment_limit: Maximum number of courses a student can take
    """

    def __init__(self, student, initial_gpa=0.0):
        """
        Initialize a SecureStudentRecord for the given student.

        Args:
            student: Student object to create secure record for
            initial_gpa (float): Initial GPA value (must be 0.0-4.0)
        """
        self.__student = student
        self.__gpa = 0.0  # Initialize to safe default
        self.set_gpa(initial_gpa)  # Use setter for validation
        self.__enrollment_limit = 5  # Maximum courses per student

    def get_gpa(self):
        """
        Getter method for the student's GPA.

        Returns:
            float: Current GPA value
        """
        return self.__gpa

    def set_gpa(self, new_gpa):
        """
        Setter method for the student's GPA with validation.

        Ensures GPA values are within the valid range (0.0 to 4.0).

        Args:
            new_gpa (float): New GPA value to set

        Raises:
            ValueError: If GPA is not between 0.0 and 4.0
        """
        if 0.0 <= new_gpa <= 4.0:
            self.__gpa = new_gpa
        else:
            raise ValueError("GPA must be between 0.0 and 4.0")

    def can_enroll_more(self):
        """
        Check if the student can enroll in additional courses.

        Performs data integrity check against enrollment limits.

        Returns:
            bool: True if student can enroll in more courses, False otherwise
        """
        return len(self.__student.enrolled_courses) < self.__enrollment_limit

    def get_student_name(self):
        """
        Get the name of the student associated with this secure record.

        Returns:
            str: Student's name
        """
        return self.__student.name
