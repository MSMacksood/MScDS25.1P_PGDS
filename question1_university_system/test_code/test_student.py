"""
Unit Tests for Student Module

Tests all student-related classes including enrollment logic, GPA calculation,
academic status determination, and secure record management.
"""

import unittest
from unittest.mock import MagicMock
import sys
import os

# Add the parent directory to the path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from student import Student, UndergraduateStudent, GraduateStudent, SecureStudentRecord
from department import Course


class TestStudent(unittest.TestCase):
    """Test cases for the base Student class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.student = Student("S001", "Alan Turing", "1912-06-23", "Computer Science")

        # Create mock courses for testing
        self.course1 = Course("CS101", "Intro to Programming", 3)
        self.course2 = Course("CS201", "Data Structures", 3, prerequisites={"CS101"})

    def test_student_initialization(self):
        """Test that Student objects are initialized correctly."""
        self.assertEqual(self.student.person_id, "S001")
        self.assertEqual(self.student.name, "Alan Turing")
        self.assertEqual(self.student.major, "Computer Science")
        self.assertEqual(self.student.gpa, 0.0)
        self.assertEqual(len(self.student.enrolled_courses), 0)

    def test_enroll_course_success(self):
        """Test successful course enrollment without prerequisites."""
        # Mock the course's add_student method to return True (successful enrollment)
        self.course1.add_student = MagicMock(return_value=True)

        self.student.enroll_course(self.course1, None)

        # Verify student was added to course
        self.course1.add_student.assert_called_once_with(self.student)

        # Verify course was added to student's enrolled courses
        self.assertIn("CS101", self.student.enrolled_courses)
        self.assertIsNone(self.student.enrolled_courses["CS101"])  # No grade yet

    def test_enroll_course_prerequisite_failure(self):
        """Test enrollment failure due to missing prerequisites."""
        # Mock the course's add_student method (shouldn't be called)
        self.course2.add_student = MagicMock(return_value=True)

        self.student.enroll_course(self.course2, None)

        # Verify add_student was not called due to prerequisite failure
        self.course2.add_student.assert_not_called()

        # Verify course was not added to student's enrolled courses
        self.assertNotIn("CS201", self.student.enrolled_courses)

    def test_enroll_course_capacity_failure(self):
        """Test enrollment failure due to course being full."""
        # Mock the course's add_student method to return False (course full)
        self.course1.add_student = MagicMock(return_value=False)

        self.student.enroll_course(self.course1, None)

        # Verify course was not added to student's enrolled courses
        self.assertNotIn("CS101", self.student.enrolled_courses)

    def test_drop_course(self):
        """Test dropping an enrolled course."""
        # First enroll in course
        self.student.enrolled_courses["CS101"] = "A"
        self.course1.remove_student = MagicMock()

        self.student.drop_course(self.course1)

        # Verify student was removed from course
        self.course1.remove_student.assert_called_once_with(self.student)

        # Verify course was removed from student's enrolled courses
        self.assertNotIn("CS101", self.student.enrolled_courses)

    def test_calculate_gpa(self):
        """Test GPA calculation with various grades."""
        # Add courses with grades
        self.student.enrolled_courses = {
            "CS101": "A",  # 4.0 * 3 = 12 points
            "CS201": "B",  # 3.0 * 3 = 9 points
            "CS301": "C"   # 2.0 * 3 = 6 points
        }
        # Total: 27 points, 9 credits, GPA = 3.0

        gpa = self.student.calculate_gpa()
        self.assertEqual(gpa, 3.0)
        self.assertEqual(self.student.gpa, 3.0)

    def test_calculate_gpa_no_grades(self):
        """Test GPA calculation with no graded courses."""
        self.student.enrolled_courses = {"CS101": None}  # No grade assigned

        gpa = self.student.calculate_gpa()
        self.assertEqual(gpa, 0.0)

    def test_get_academic_status(self):
        """Test academic status determination based on GPA."""
        # Test Dean's List (GPA >= 3.5)
        self.student.enrolled_courses = {"CS101": "A"}  # GPA = 4.0
        status = self.student.get_academic_status()
        self.assertEqual(status, "Dean's List")

        # Test Good Standing (2.0 <= GPA < 3.5)
        self.student.enrolled_courses = {"CS101": "C"}  # GPA = 2.0
        status = self.student.get_academic_status()
        self.assertEqual(status, "Good Standing")

        # Test Probation (GPA < 2.0)
        self.student.enrolled_courses = {"CS101": "F"}  # GPA = 0.0
        status = self.student.get_academic_status()
        self.assertEqual(status, "Probation")

    def test_get_responsibilities(self):
        """Test that student responsibilities include base and academic duties."""
        responsibilities = self.student.get_responsibilities()

        self.assertIn("Adhere to university policies.", responsibilities)
        self.assertIn("Attend classes and complete coursework.", responsibilities)


class TestUndergraduateStudent(unittest.TestCase):
    """Test cases for the UndergraduateStudent class."""

    def test_undergraduate_initialization(self):
        """Test undergraduate student initialization with year level."""
        undergrad = UndergraduateStudent("U001", "Jane Doe", "2000-01-01", "Physics", 2)

        self.assertEqual(undergrad.major, "Physics")
        self.assertEqual(undergrad.year_level, 2)
        self.assertIsInstance(undergrad, Student)  # Should inherit from Student


class TestGraduateStudent(unittest.TestCase):
    """Test cases for the GraduateStudent class."""

    def test_graduate_initialization(self):
        """Test graduate student initialization with advisor."""
        grad = GraduateStudent("G001", "Bob Smith", "1995-05-15", "Mathematics", "Dr. Johnson")

        self.assertEqual(grad.major, "Mathematics")
        self.assertEqual(grad.advisor, "Dr. Johnson")
        self.assertIsInstance(grad, Student)  # Should inherit from Student


class TestSecureStudentRecord(unittest.TestCase):
    """Test cases for the SecureStudentRecord class (encapsulation example)."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.student = Student("S001", "Test Student", "2000-01-01", "CS")
        self.secure_record = SecureStudentRecord(self.student, 3.5)

    def test_secure_record_initialization(self):
        """Test secure record initialization with valid GPA."""
        self.assertEqual(self.secure_record.get_gpa(), 3.5)
        self.assertEqual(self.secure_record.get_student_name(), "Test Student")

    def test_gpa_setter_valid_values(self):
        """Test GPA setter with valid values."""
        valid_gpas = [0.0, 2.5, 4.0]

        for gpa in valid_gpas:
            self.secure_record.set_gpa(gpa)
            self.assertEqual(self.secure_record.get_gpa(), gpa)

    def test_gpa_setter_invalid_values(self):
        """Test GPA setter with invalid values raises ValueError."""
        invalid_gpas = [-1.0, 4.1, 5.0, 10.0]

        for gpa in invalid_gpas:
            with self.assertRaises(ValueError):
                self.secure_record.set_gpa(gpa)

    def test_can_enroll_more(self):
        """Test enrollment limit checking."""
        # Initially should be able to enroll more (0 < 5)
        self.assertTrue(self.secure_record.can_enroll_more())

        # Add courses to reach limit
        for i in range(5):
            self.student.enrolled_courses[f"CS{100+i}"] = None

        # Should not be able to enroll more (5 >= 5)
        self.assertFalse(self.secure_record.can_enroll_more())


if __name__ == '__main__':
    unittest.main()
