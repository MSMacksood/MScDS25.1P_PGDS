"""
Unit Tests for Person Module

Tests the base Person class and Staff class functionality including
age calculation, responsibility management, and inheritance behavior.
"""

import unittest
from unittest.mock import patch
import datetime
import sys
import os

# Add the parent directory to the path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from person import Person, Staff


class TestPerson(unittest.TestCase):
    """Test cases for the base Person class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.person = Person("P001", "John Doe", "1990-05-15")

    def test_person_initialization(self):
        """Test that Person objects are initialized correctly."""
        self.assertEqual(self.person.person_id, "P001")
        self.assertEqual(self.person.name, "John Doe")
        self.assertEqual(self.person.birth_date, "1990-05-15")

    def test_get_age_calculation(self):
        """Test age calculation with different birth dates."""
        # Mock today's date to ensure consistent testing
        with patch('datetime.date.today') as mock_today:
            mock_today.return_value = datetime.date(2024, 1, 1)

            # Test person born before birthday this year
            person_before = Person("P002", "Jane Smith", "1990-03-15")
            self.assertEqual(person_before.get_age(), 34)  # Had birthday already

            # Test person born after birthday this year
            person_after = Person("P003", "Bob Johnson", "1990-06-15")
            self.assertEqual(person_after.get_age(), 33)  # Birthday not yet reached

    def test_get_responsibilities(self):
        """Test that base responsibilities are returned correctly."""
        responsibilities = self.person.get_responsibilities()
        self.assertIsInstance(responsibilities, list)
        self.assertIn("Adhere to university policies.", responsibilities)

    def test_string_representation(self):
        """Test the __str__ method returns correct format."""
        expected = "John Doe (ID: P001)"
        self.assertEqual(str(self.person), expected)


class TestStaff(unittest.TestCase):
    """Test cases for the Staff class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.staff = Staff("ST001", "Alice Brown", "1985-08-20", "IT", "Administrator")

    def test_staff_initialization(self):
        """Test that Staff objects inherit from Person and add staff-specific attributes."""
        # Test inherited attributes
        self.assertEqual(self.staff.person_id, "ST001")
        self.assertEqual(self.staff.name, "Alice Brown")
        self.assertEqual(self.staff.birth_date, "1985-08-20")

        # Test staff-specific attributes
        self.assertEqual(self.staff.department, "IT")
        self.assertEqual(self.staff.role, "Administrator")

    def test_staff_inheritance(self):
        """Test that Staff is properly inheriting from Person."""
        self.assertIsInstance(self.staff, Person)
        self.assertTrue(hasattr(self.staff, 'get_age'))
        self.assertTrue(hasattr(self.staff, 'person_id'))

    def test_staff_responsibilities(self):
        """Test that staff responsibilities include both base and role-specific duties."""
        responsibilities = self.staff.get_responsibilities()

        # Should include base responsibility
        self.assertIn("Adhere to university policies.", responsibilities)

        # Should include role-specific responsibility
        expected_role_resp = "Perform Administrator duties for the IT department."
        self.assertIn(expected_role_resp, responsibilities)

        # Should have at least 2 responsibilities
        self.assertGreaterEqual(len(responsibilities), 2)


if __name__ == '__main__':
    unittest.main()
