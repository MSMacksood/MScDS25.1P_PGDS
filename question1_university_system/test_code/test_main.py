"""
Integration Tests for Main Application

Tests the complete university management system workflow including
department setup, personnel creation, enrollment processes, and
polymorphic behavior demonstrations.
"""

import unittest
from unittest.mock import patch
import io
import sys
import os

# Add the parent directory to the path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import main
from person import Staff
from student import UndergraduateStudent, SecureStudentRecord
from faculty import Professor, Lecturer
from department import Department, Course


class TestMainIntegration(unittest.TestCase):
    """Integration tests for the main application workflow."""

    def setUp(self):
        """Set up test fixtures for integration testing."""
        # Capture stdout to test print statements
        self.held, sys.stdout = sys.stdout, io.StringIO()

    def tearDown(self):
        """Clean up after each test."""
        sys.stdout = self.held

    def test_main_execution_completes(self):
        """Test that main() executes without errors."""
        try:
            main()
            execution_successful = True
        except Exception:
            execution_successful = False

        self.assertTrue(execution_successful)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_output_content(self, mock_stdout):
        """Test that main() produces expected output content."""
        main()
        output = mock_stdout.getvalue()

        # Check for key sections in output
        self.assertIn("University Management System", output)
        self.assertIn("enrolled in", output)  # Enrollment messages
        self.assertIn("GPA:", output)  # GPA calculation
        self.assertIn("Demonstrating Polymorphism", output)
        self.assertIn("Responsibilities:", output)
        self.assertIn("Workload:", output)


class TestSystemIntegration(unittest.TestCase):
    """Test complete system integration with realistic scenarios."""

    def test_complete_enrollment_workflow(self):
        """Test a complete student enrollment workflow."""
        # Set up department and courses
        cs_dept = Department("Computer Science")
        cs101 = Course("CS101", "Intro to Programming", 3)
        cs201 = Course("CS201", "Data Structures", 3, prerequisites={"CS101"})

        cs_dept.add_course(cs101)
        cs_dept.add_course(cs201)

        # Create student
        student = UndergraduateStudent("S001", "Test Student", "2000-01-01", "CS", 2)

        # Test prerequisite enforcement
        student.enroll_course(cs201, cs_dept)  # Should fail
        self.assertNotIn("CS201", student.enrolled_courses)

        # Enroll in prerequisite course
        student.enroll_course(cs101, cs_dept)  # Should succeed
        self.assertIn("CS101", student.enrolled_courses)

        # Complete prerequisite with grade
        student.enrolled_courses["CS101"] = "A"

        # Now advanced course should work
        student.enroll_course(cs201, cs_dept)  # Should succeed
        self.assertIn("CS201", student.enrolled_courses)

    def test_gpa_and_academic_status_workflow(self):
        """Test GPA calculation and academic status determination."""
        student = UndergraduateStudent("S001", "Test Student", "2000-01-01", "CS", 3)

        # Test with high GPA (Dean's List)
        student.enrolled_courses = {
            "CS101": "A",
            "CS201": "A",
            "MATH101": "B"
        }

        gpa = student.calculate_gpa()
        status = student.get_academic_status()

        self.assertAlmostEqual(gpa, 3.67, places=2)  # (4+4+3)/3
        self.assertEqual(status, "Dean's List")

        # Test with low GPA (Probation)
        student.enrolled_courses = {
            "CS101": "D",
            "CS201": "F"
        }

        gpa = student.calculate_gpa()
        status = student.get_academic_status()

        self.assertEqual(gpa, 0.5)  # (1+0)/2
        self.assertEqual(status, "Probation")

    def test_faculty_polymorphism(self):
        """Test polymorphic behavior across different faculty types."""
        course = Course("CS101", "Test Course", 3)

        # Create different faculty types
        faculty_members = [
            Professor("P001", "Dr. Professor", "1970-01-01", "CS"),
            Lecturer("L001", "Ms. Lecturer", "1975-01-01", "CS"),
        ]

        # Test that all respond to common interface
        for faculty in faculty_members:
            workload = faculty.calculate_workload()
            responsibilities = faculty.get_responsibilities()

            self.assertIsInstance(workload, str)
            self.assertGreater(len(workload), 0)
            self.assertIsInstance(responsibilities, list)
            self.assertGreater(len(responsibilities), 0)

    def test_secure_record_encapsulation(self):
        """Test encapsulation principles with SecureStudentRecord."""
        student = UndergraduateStudent("S001", "Test Student", "2000-01-01", "CS", 2)
        secure_record = SecureStudentRecord(student, 3.0)

        # Test valid operations
        self.assertEqual(secure_record.get_gpa(), 3.0)
        secure_record.set_gpa(3.5)
        self.assertEqual(secure_record.get_gpa(), 3.5)

        # Test validation
        with self.assertRaises(ValueError):
            secure_record.set_gpa(5.0)  # Invalid GPA

        # Test enrollment limit checking
        self.assertTrue(secure_record.can_enroll_more())

        # Fill up courses
        for i in range(5):
            student.enrolled_courses[f"CS{100+i}"] = None

        self.assertFalse(secure_record.can_enroll_more())

    def test_department_faculty_management(self):
        """Test department's ability to manage courses and faculty."""
        dept = Department("Computer Science")

        # Add courses
        courses = [
            Course("CS101", "Intro Programming", 3),
            Course("CS201", "Data Structures", 3),
            Course("CS301", "Algorithms", 3)
        ]

        for course in courses:
            dept.add_course(course)

        self.assertEqual(len(dept.courses), 3)

        # Add faculty
        faculty = [
            Professor("P001", "Dr. Ada", "1815-12-10", "CS"),
            Lecturer("L001", "Ms. Grace", "1906-12-09", "CS")
        ]

        for f in faculty:
            dept.add_faculty(f)

        self.assertEqual(len(dept.faculty), 2)

        # Test course lookup
        self.assertEqual(dept.courses["CS201"].name, "Data Structures")

    def test_cross_module_interactions(self):
        """Test interactions between different modules work correctly."""
        # Create objects from all modules
        dept = Department("Computer Science")
        course = Course("CS101", "Programming", 3)
        student = UndergraduateStudent("S001", "Alice", "2000-01-01", "CS", 1)
        professor = Professor("P001", "Dr. Smith", "1970-01-01", "CS")
        staff = Staff("ST001", "Bob Admin", "1980-01-01", "Registrar", "Administrator")

        # Test that they can interact
        dept.add_course(course)
        dept.add_faculty(professor)

        # Test enrollment process
        course.add_student(student)
        student.enrolled_courses[course.course_id] = "A"

        # Verify interactions worked
        self.assertIn(course.course_id, dept.courses)
        self.assertIn(professor, dept.faculty)
        self.assertIn(student, course.students_enrolled)
        self.assertEqual(student.enrolled_courses["CS101"], "A")


class TestErrorHandling(unittest.TestCase):
    """Test error handling and edge cases."""

    def test_invalid_gpa_handling(self):
        """Test that invalid GPA values are handled properly."""
        student = UndergraduateStudent("S001", "Test", "2000-01-01", "CS", 1)
        secure_record = SecureStudentRecord(student)

        # Test boundary conditions
        valid_gpas = [0.0, 4.0, 2.5]
        invalid_gpas = [-0.1, 4.1, -1.0, 10.0]

        # Valid GPAs should work
        for gpa in valid_gpas:
            secure_record.set_gpa(gpa)
            self.assertEqual(secure_record.get_gpa(), gpa)

        # Invalid GPAs should raise ValueError
        for gpa in invalid_gpas:
            with self.assertRaises(ValueError):
                secure_record.set_gpa(gpa)

    def test_enrollment_edge_cases(self):
        """Test edge cases in course enrollment."""
        course = Course("CS101", "Test", 3, limit=1)  # Very small limit
        students = [
            UndergraduateStudent("S001", "Student1", "2000-01-01", "CS", 1),
            UndergraduateStudent("S002", "Student2", "2000-01-02", "CS", 1)
        ]

        # First enrollment should succeed
        result1 = course.add_student(students[0])
        self.assertTrue(result1)

        # Second enrollment should fail (over capacity)
        result2 = course.add_student(students[1])
        self.assertFalse(result2)

        # Remove first student
        course.remove_student(students[0])

        # Now second student should be able to enroll
        result3 = course.add_student(students[1])
        self.assertTrue(result3)


if __name__ == '__main__':
    # Run all tests with verbose output
    unittest.main(verbosity=2)
