"""
Unit Tests for Department Module

Tests course enrollment management, prerequisite validation,
and department organization functionality.
"""

import unittest
import sys
import os

# Add the parent directory to the path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from department import Course, Department
from student import Student


class TestCourse(unittest.TestCase):
    """Test cases for the Course class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.course = Course("CS101", "Intro to Programming", 3, limit=2)
        self.student1 = Student("S001", "Alice", "2000-01-01", "CS")
        self.student2 = Student("S002", "Bob", "2000-02-02", "CS")
        self.student3 = Student("S003", "Charlie", "2000-03-03", "CS")

    def test_course_initialization(self):
        """Test course initialization with all parameters."""
        self.assertEqual(self.course.course_id, "CS101")
        self.assertEqual(self.course.name, "Intro to Programming")
        self.assertEqual(self.course.credits, 3)
        self.assertEqual(self.course.enrollment_limit, 2)
        self.assertEqual(len(self.course.prerequisites), 0)
        self.assertEqual(len(self.course.students_enrolled), 0)

    def test_course_with_prerequisites(self):
        """Test course initialization with prerequisites."""
        advanced_course = Course("CS201", "Data Structures", 3, 
                               prerequisites=["CS101", "MATH101"])

        expected_prereqs = {"CS101", "MATH101"}
        self.assertEqual(advanced_course.prerequisites, expected_prereqs)

    def test_add_student_success(self):
        """Test successful student enrollment within capacity."""
        # Add first student
        result1 = self.course.add_student(self.student1)
        self.assertTrue(result1)
        self.assertIn(self.student1, self.course.students_enrolled)
        self.assertEqual(len(self.course.students_enrolled), 1)

        # Add second student (at capacity)
        result2 = self.course.add_student(self.student2)
        self.assertTrue(result2)
        self.assertIn(self.student2, self.course.students_enrolled)
        self.assertEqual(len(self.course.students_enrolled), 2)

    def test_add_student_capacity_exceeded(self):
        """Test student enrollment failure when course is full."""
        # Fill course to capacity
        self.course.add_student(self.student1)
        self.course.add_student(self.student2)

        # Try to add third student (should fail)
        result = self.course.add_student(self.student3)
        self.assertFalse(result)
        self.assertNotIn(self.student3, self.course.students_enrolled)
        self.assertEqual(len(self.course.students_enrolled), 2)

    def test_remove_student_success(self):
        """Test successful student removal from course."""
        # First enroll student
        self.course.add_student(self.student1)
        self.assertIn(self.student1, self.course.students_enrolled)

        # Then remove student
        self.course.remove_student(self.student1)
        self.assertNotIn(self.student1, self.course.students_enrolled)
        self.assertEqual(len(self.course.students_enrolled), 0)

    def test_remove_student_not_enrolled(self):
        """Test removing a student who isn't enrolled (should handle gracefully)."""
        # Try to remove student who was never enrolled
        initial_count = len(self.course.students_enrolled)
        self.course.remove_student(self.student1)

        # Should not change enrollment list
        self.assertEqual(len(self.course.students_enrolled), initial_count)

    def test_course_string_representation(self):
        """Test the __str__ method returns correct format."""
        expected = "CS101: Intro to Programming (3 credits)"
        self.assertEqual(str(self.course), expected)

    def test_default_enrollment_limit(self):
        """Test default enrollment limit when not specified."""
        default_course = Course("CS102", "Test Course", 3)
        self.assertEqual(default_course.enrollment_limit, 30)  # Default value

    def test_prerequisites_immutability(self):
        """Test that prerequisites are stored as a set for efficient operations."""
        prereq_course = Course("CS301", "Advanced Course", 3, 
                             prerequisites=["CS101", "CS201", "CS101"])  # Duplicate

        # Should be a set (no duplicates)
        self.assertIsInstance(prereq_course.prerequisites, set)
        self.assertEqual(len(prereq_course.prerequisites), 2)  # Duplicates removed


class TestDepartment(unittest.TestCase):
    """Test cases for the Department class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.department = Department("Computer Science")
        self.course1 = Course("CS101", "Intro to Programming", 3)
        self.course2 = Course("CS201", "Data Structures", 3)

    def test_department_initialization(self):
        """Test department initialization with empty collections."""
        self.assertEqual(self.department.name, "Computer Science")
        self.assertEqual(len(self.department.courses), 0)
        self.assertEqual(len(self.department.faculty), 0)

    def test_add_course(self):
        """Test adding courses to department catalog."""
        self.department.add_course(self.course1)

        # Course should be in department's catalog
        self.assertIn("CS101", self.department.courses)
        self.assertEqual(self.department.courses["CS101"], self.course1)
        self.assertEqual(len(self.department.courses), 1)

    def test_add_multiple_courses(self):
        """Test adding multiple courses to department."""
        self.department.add_course(self.course1)
        self.department.add_course(self.course2)

        self.assertEqual(len(self.department.courses), 2)
        self.assertIn("CS101", self.department.courses)
        self.assertIn("CS201", self.department.courses)

    def test_add_faculty(self):
        """Test adding faculty members to department."""
        # Create a mock faculty member (we'll import from faculty module)
        from faculty import Professor

        professor = Professor("F001", "Dr. Smith", "1970-01-01", "Computer Science")
        self.department.add_faculty(professor)

        self.assertEqual(len(self.department.faculty), 1)
        self.assertIn(professor, self.department.faculty)

    def test_add_multiple_faculty(self):
        """Test adding multiple faculty members to department."""
        from faculty import Professor, Lecturer

        professor = Professor("F001", "Dr. Smith", "1970-01-01", "Computer Science")
        lecturer = Lecturer("F002", "Ms. Johnson", "1975-01-01", "Computer Science")

        self.department.add_faculty(professor)
        self.department.add_faculty(lecturer)

        self.assertEqual(len(self.department.faculty), 2)
        self.assertIn(professor, self.department.faculty)
        self.assertIn(lecturer, self.department.faculty)

    def test_course_lookup_efficiency(self):
        """Test that courses are stored in a dictionary for efficient lookup."""
        # Add multiple courses
        courses = [
            Course("CS101", "Course 1", 3),
            Course("CS201", "Course 2", 3),
            Course("CS301", "Course 3", 3)
        ]

        for course in courses:
            self.department.add_course(course)

        # Direct lookup should work efficiently
        self.assertEqual(self.department.courses["CS201"].name, "Course 2")
        self.assertEqual(self.department.courses["CS301"].credits, 3)


class TestCourseStudentInteraction(unittest.TestCase):
    """Integration tests for Course-Student interactions."""

    def setUp(self):
        """Set up test fixtures with realistic course-student scenarios."""
        self.intro_course = Course("CS101", "Intro Programming", 3, limit=2)
        self.advanced_course = Course("CS201", "Data Structures", 3, 
                                    limit=2, prerequisites={"CS101"})

        self.student1 = Student("S001", "Alice", "2000-01-01", "CS")
        self.student2 = Student("S002", "Bob", "2000-02-02", "CS")

    def test_prerequisite_enforcement_integration(self):
        """Test that prerequisites are properly enforced in enrollment workflow."""
        # Student tries to enroll in advanced course without prerequisite
        # (This would be checked by Student.enroll_course method)

        # Simulate the prerequisite check logic
        completed_courses = set(self.student1.enrolled_courses.keys())
        has_prereqs = self.advanced_course.prerequisites.issubset(completed_courses)

        self.assertFalse(has_prereqs)  # Should fail prerequisite check

        # Now simulate completing prerequisite
        self.student1.enrolled_courses["CS101"] = "A"
        completed_courses = set(self.student1.enrolled_courses.keys())
        has_prereqs = self.advanced_course.prerequisites.issubset(completed_courses)

        self.assertTrue(has_prereqs)  # Should pass prerequisite check

    def test_enrollment_capacity_management(self):
        """Test enrollment capacity management across multiple students."""
        # Both students try to enroll in intro course (capacity = 2)
        result1 = self.intro_course.add_student(self.student1)
        result2 = self.intro_course.add_student(self.student2)

        self.assertTrue(result1)  # First student succeeds
        self.assertTrue(result2)  # Second student succeeds (at capacity)

        # Third student should fail
        student3 = Student("S003", "Charlie", "2000-03-03", "CS")
        result3 = self.intro_course.add_student(student3)

        self.assertFalse(result3)  # Should fail due to capacity
        self.assertEqual(len(self.intro_course.students_enrolled), 2)


if __name__ == '__main__':
    unittest.main()
