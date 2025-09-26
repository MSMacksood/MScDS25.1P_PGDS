"""
Unit Tests for Faculty Module

Tests all faculty-related classes including workload calculations,
responsibility management, and inheritance hierarchy.
"""

import unittest
import sys
import os

# Add the parent directory to the path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from faculty import Faculty, Professor, Lecturer, TA
from department import Course


class TestFaculty(unittest.TestCase):
    """Test cases for the base Faculty class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.faculty = Faculty("F001", "Dr. Smith", "1970-03-15", "Computer Science", "Associate Professor")

    def test_faculty_initialization(self):
        """Test that Faculty objects are initialized correctly."""
        self.assertEqual(self.faculty.person_id, "F001")
        self.assertEqual(self.faculty.name, "Dr. Smith")
        self.assertEqual(self.faculty.birth_date, "1970-03-15")
        self.assertEqual(self.faculty.department, "Computer Science")
        self.assertEqual(self.faculty.rank, "Associate Professor")

    def test_calculate_workload_base(self):
        """Test base workload calculation method."""
        workload = self.faculty.calculate_workload()
        self.assertEqual(workload, "Base workload calculation.")

    def test_faculty_responsibilities(self):
        """Test that faculty responsibilities include research duties."""
        responsibilities = self.faculty.get_responsibilities()

        # Should include base responsibility
        self.assertIn("Adhere to university policies.", responsibilities)

        # Should include faculty-specific research responsibility
        self.assertIn("Conduct research and publish findings.", responsibilities)

        # Should have at least 2 responsibilities
        self.assertGreaterEqual(len(responsibilities), 2)


class TestProfessor(unittest.TestCase):
    """Test cases for the Professor class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.professor = Professor("P001", "Ada Lovelace", "1815-12-10", "Computer Science")

    def test_professor_initialization(self):
        """Test professor initialization with correct rank and tenure status."""
        self.assertEqual(self.professor.rank, "Professor")
        self.assertEqual(self.professor.department, "Computer Science")
        self.assertFalse(self.professor.tenured)  # Default to non-tenured

        # Should inherit from Faculty
        self.assertIsInstance(self.professor, Faculty)

    def test_professor_workload(self):
        """Test professor-specific workload calculation."""
        workload = self.professor.calculate_workload()
        expected = "Teaches 2 courses, advises 5 graduate students, serves on 1 committee."
        self.assertEqual(workload, expected)

    def test_professor_tenure_status(self):
        """Test that tenure status can be modified."""
        self.assertFalse(self.professor.tenured)

        # Grant tenure
        self.professor.tenured = True
        self.assertTrue(self.professor.tenured)


class TestLecturer(unittest.TestCase):
    """Test cases for the Lecturer class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.lecturer = Lecturer("L001", "Grace Hopper", "1906-12-09", "Computer Science")

    def test_lecturer_initialization(self):
        """Test lecturer initialization with correct rank."""
        self.assertEqual(self.lecturer.rank, "Lecturer")
        self.assertEqual(self.lecturer.department, "Computer Science")

        # Should inherit from Faculty
        self.assertIsInstance(self.lecturer, Faculty)

    def test_lecturer_workload(self):
        """Test lecturer-specific workload calculation (higher teaching load)."""
        workload = self.lecturer.calculate_workload()
        self.assertEqual(workload, "Teaches 4 courses.")

    def test_lecturer_responsibilities(self):
        """Test that lecturer responsibilities focus on teaching, not research."""
        responsibilities = self.lecturer.get_responsibilities()

        # Should include base responsibility
        self.assertIn("Adhere to university policies.", responsibilities)

        # Should include teaching-focused responsibility
        self.assertIn("Focus on teaching and student instruction.", responsibilities)

        # Should NOT include research responsibility (overridden)
        self.assertNotIn("Conduct research and publish findings.", responsibilities)


class TestTA(unittest.TestCase):
    """Test cases for the Teaching Assistant class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.course = Course("CS101", "Intro to Programming", 3)
        self.ta = TA("TA001", "John Student", "1995-09-20", "Computer Science", self.course)

    def test_ta_initialization(self):
        """Test TA initialization with assisting course."""
        self.assertEqual(self.ta.rank, "Teaching Assistant")
        self.assertEqual(self.ta.department, "Computer Science")
        self.assertEqual(self.ta.assisting_course, self.course)

        # Should inherit from Faculty
        self.assertIsInstance(self.ta, Faculty)

    def test_ta_workload(self):
        """Test TA-specific workload calculation with course reference."""
        workload = self.ta.calculate_workload()
        expected = f"Assists with {self.course.name}, holds office hours."
        self.assertEqual(workload, expected)

    def test_ta_workload_different_courses(self):
        """Test TA workload with different courses."""
        math_course = Course("MATH201", "Calculus II", 4)
        math_ta = TA("TA002", "Jane Helper", "1996-03-10", "Mathematics", math_course)

        workload = math_ta.calculate_workload()
        expected = "Assists with Calculus II, holds office hours."
        self.assertEqual(workload, expected)


class TestFacultyInheritance(unittest.TestCase):
    """Test cases for faculty inheritance hierarchy."""

    def test_all_faculty_inherit_from_faculty(self):
        """Test that all faculty types properly inherit from Faculty base class."""
        course = Course("TEST101", "Test Course", 3)

        professor = Professor("P001", "Prof Test", "1970-01-01", "Test Dept")
        lecturer = Lecturer("L001", "Lect Test", "1975-01-01", "Test Dept")
        ta = TA("TA001", "TA Test", "1990-01-01", "Test Dept", course)

        faculty_members = [professor, lecturer, ta]

        for faculty_member in faculty_members:
            self.assertIsInstance(faculty_member, Faculty)
            self.assertTrue(hasattr(faculty_member, 'calculate_workload'))
            self.assertTrue(hasattr(faculty_member, 'get_responsibilities'))

    def test_faculty_polymorphism(self):
        """Test polymorphic behavior across different faculty types."""
        course = Course("TEST101", "Test Course", 3)

        faculty_members = [
            Professor("P001", "Prof Test", "1970-01-01", "Test Dept"),
            Lecturer("L001", "Lect Test", "1975-01-01", "Test Dept"),
            TA("TA001", "TA Test", "1990-01-01", "Test Dept", course)
        ]

        # All should respond to calculate_workload() but with different results
        workloads = [faculty.calculate_workload() for faculty in faculty_members]

        # Each workload should be different and non-empty
        self.assertEqual(len(set(workloads)), 3)  # All unique
        for workload in workloads:
            self.assertIsInstance(workload, str)
            self.assertGreater(len(workload), 0)


if __name__ == '__main__':
    unittest.main()
