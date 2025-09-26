"""
Faculty Module - Academic Personnel Classes

This module contains all faculty-related classes representing different types of
academic personnel in the university system. It demonstrates inheritance hierarchy,
method overriding, and different faculty role specializations.

Classes:
    Faculty: Base class for all academic faculty members
    Professor: Full-time professors with research and teaching duties
    Lecturer: Teaching-focused faculty without research requirements
    TA: Teaching Assistants who support course instruction
"""

from person import Person


class Faculty(Person):
    """
    Base class for academic faculty members.

    This class represents the common attributes and behaviors shared by all
    faculty members in the university, including professors, lecturers, and
    teaching assistants. It extends Person with faculty-specific functionality.

    Attributes:
        department (str): Academic department where faculty member works
        rank (str): Academic rank or title (Professor, Lecturer, TA, etc.)
    """

    def __init__(self, person_id, name, birth_date, department, rank):
        """
        Initialize a Faculty member with academic information.

        Args:
            person_id (str): Unique identifier for the faculty member
            name (str): Full name of the faculty member
            birth_date (str): Birth date in YYYY-MM-DD format
            department (str): Academic department
            rank (str): Academic rank or title
        """
        # Initialize base Person attributes
        super().__init__(person_id, name, birth_date)
        self.department = department
        self.rank = rank

    def calculate_workload(self):
        """
        Calculate the workload for this faculty member.

        This is a base implementation that should be overridden by subclasses
        to provide specific workload calculations based on faculty type.

        Returns:
            str: Description of the faculty member's workload
        """
        return "Base workload calculation."

    def get_responsibilities(self):
        """
        Get the list of responsibilities for faculty members.

        Extends base Person responsibilities with research duties that are
        common to most faculty positions.

        Returns:
            list: List of responsibility strings including research duties
        """
        # Get base responsibilities from Person class
        base_resp = super().get_responsibilities()
        # Add faculty-specific responsibility
        base_resp.append("Conduct research and publish findings.")
        return base_resp


class Professor(Faculty):
    """
    Represents a full-time professor with teaching and research duties.

    Professors typically have the highest academic rank and are expected to
    balance teaching, research, and service responsibilities. They may be
    eligible for tenure based on performance.

    Attributes:
        tenured (bool): Whether the professor has received tenure
    """

    def __init__(self, person_id, name, birth_date, department):
        """
        Initialize a Professor.

        Args:
            person_id (str): Unique identifier for the professor
            name (str): Full name of the professor
            birth_date (str): Birth date in YYYY-MM-DD format
            department (str): Academic department
        """
        # Initialize with "Professor" rank
        super().__init__(person_id, name, birth_date, department, "Professor")
        self.tenured = False  # Default to non-tenured status

    def calculate_workload(self):
        """
        Calculate the workload specific to professors.

        Professors typically have balanced responsibilities across teaching,
        research supervision, and administrative service.

        Returns:
            str: Detailed description of professor workload
        """
        return "Teaches 2 courses, advises 5 graduate students, serves on 1 committee."


class Lecturer(Faculty):
    """
    Represents a teaching-focused faculty member without research requirements.

    Lecturers primarily focus on instruction and typically have higher teaching
    loads compared to professors. They may not be required to conduct research
    or publish scholarly work.
    """

    def __init__(self, person_id, name, birth_date, department):
        """
        Initialize a Lecturer.

        Args:
            person_id (str): Unique identifier for the lecturer
            name (str): Full name of the lecturer
            birth_date (str): Birth date in YYYY-MM-DD format
            department (str): Academic department
        """
        # Initialize with "Lecturer" rank
        super().__init__(person_id, name, birth_date, department, "Lecturer")

    def calculate_workload(self):
        """
        Calculate the workload specific to lecturers.

        Lecturers typically have higher teaching loads since they don't
        have research responsibilities.

        Returns:
            str: Description of lecturer's teaching-focused workload
        """
        return "Teaches 4 courses."

    def get_responsibilities(self):
        """
        Get the list of responsibilities specific to lecturers.

        Overrides the base Faculty responsibilities to remove research
        requirements and focus solely on teaching duties.

        Returns:
            list: List of teaching-focused responsibilities
        """
        # Override completely to remove research responsibility
        return ["Adhere to university policies.", "Focus on teaching and student instruction."]


class TA(Faculty):
    """
    Represents a Teaching Assistant who supports course instruction.

    TAs are typically graduate students who assist professors with course
    delivery, grading, and student support. They have limited teaching
    responsibilities focused on a specific course.

    Attributes:
        assisting_course: Course object that the TA is assigned to assist
    """

    def __init__(self, person_id, name, birth_date, department, assisting_course):
        """
        Initialize a Teaching Assistant.

        Args:
            person_id (str): Unique identifier for the TA
            name (str): Full name of the TA
            birth_date (str): Birth date in YYYY-MM-DD format
            department (str): Academic department
            assisting_course: Course object that the TA will assist with
        """
        # Initialize with "Teaching Assistant" rank
        super().__init__(person_id, name, birth_date, department, "Teaching Assistant")
        self.assisting_course = assisting_course

    def calculate_workload(self):
        """
        Calculate the workload specific to teaching assistants.

        TAs typically assist with one specific course, including grading,
        office hours, and student support activities.

        Returns:
            str: Description of TA workload for their assigned course
        """
        return f"Assists with {self.assisting_course.name}, holds office hours."
