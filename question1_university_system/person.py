"""
Person Module - Base Classes for University Personnel

This module contains the base Person class and Staff class that serve as the foundation
for all individuals in the university management system. It demonstrates inheritance
and polymorphism principles in object-oriented programming.

Classes:
    Person: Abstract base class for all university individuals
    Staff: Non-academic personnel with specific departmental roles
"""

import datetime


class Person:
    """
    Base class for all individuals in the university system.

    This class provides common attributes and methods that all university
    personnel (students, faculty, staff) share, including personal information
    and basic responsibilities.

    Attributes:
        person_id (str): Unique identifier for the person
        name (str): Full name of the person
        birth_date (str): Birth date in YYYY-MM-DD format
    """

    def __init__(self, person_id, name, birth_date):
        """
        Initialize a Person with basic information.

        Args:
            person_id (str): Unique identifier for the person
            name (str): Full name of the person
            birth_date (str): Birth date in YYYY-MM-DD format
        """
        self.person_id = person_id
        self.name = name
        self.birth_date = birth_date

    def get_age(self):
        """
        Calculate and return the person's current age.

        Returns:
            int: Current age in years, accounting for whether birthday has
                 occurred this year
        """
        today = datetime.date.today()
        birth_date_obj = datetime.datetime.strptime(self.birth_date, "%Y-%m-%d").date()

        # Calculate age, adjusting for whether birthday has occurred this year
        return today.year - birth_date_obj.year - ((today.month, today.day) < (birth_date_obj.month, birth_date_obj.day))

    def get_responsibilities(self):
        """
        Get the list of responsibilities for this person.

        This method is designed to be overridden by subclasses to provide
        specific responsibilities for different types of university personnel.

        Returns:
            list: List of responsibility strings
        """
        return ["Adhere to university policies."]

    def __str__(self):
        """
        Return a string representation of the person.

        Returns:
            str: Formatted string with name and ID
        """
        return f"{self.name} (ID: {self.person_id})"


class Staff(Person):
    """
    Represents a staff member of the university.

    Staff are non-academic personnel who perform administrative, technical,
    or support functions within various university departments.

    Attributes:
        department (str): Department where the staff member works
        role (str): Specific job title or role description
    """

    def __init__(self, person_id, name, birth_date, department, role):
        """
        Initialize a Staff member with personal and employment information.

        Args:
            person_id (str): Unique identifier for the staff member
            name (str): Full name of the staff member
            birth_date (str): Birth date in YYYY-MM-DD format
            department (str): Department where they work
            role (str): Job title or role description
        """
        # Call parent constructor to initialize common attributes
        super().__init__(person_id, name, birth_date)
        self.department = department
        self.role = role

    def get_responsibilities(self):
        """
        Get the list of responsibilities for this staff member.

        Extends the base responsibilities with department-specific duties.

        Returns:
            list: List of responsibility strings including base and role-specific duties
        """
        # Get base responsibilities from parent class
        base_resp = super().get_responsibilities()
        # Add role-specific responsibility
        base_resp.append(f"Perform {self.role} duties for the {self.department} department.")
        return base_resp
