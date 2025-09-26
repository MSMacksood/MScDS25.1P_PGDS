
"""
University Management System - Main Application

This is the main application file that demonstrates the university management system
by creating instances of various classes and showing their interactions. It serves
as both an entry point and a comprehensive example of object-oriented programming
principles including inheritance, polymorphism, and encapsulation.

The system demonstrates:
- Class hierarchy and inheritance (Person -> Student/Faculty/Staff)
- Polymorphism through common interfaces
- Encapsulation with private attributes and validation
- Business logic for course enrollment and academic management
"""

# Import specific classes from each module
from person import Staff
from student import UndergraduateStudent, SecureStudentRecord
from faculty import Professor, Lecturer
from department import Department, Course


def main():
    """
    Main function demonstrating the university management system.

    This function creates a sample university environment with departments,
    courses, and various types of personnel, then demonstrates key system
    functionality including enrollment, grading, and polymorphic behavior.
    """
    print("--- University Management System ---")

    # === DEPARTMENT AND COURSE SETUP ===

    # Create Computer Science department
    cs_dept = Department("Computer Science")

    # Create courses with prerequisite relationships
    cs101 = Course("CS101", "Intro to Programming", 3, prerequisites=None)
    cs201 = Course("CS201", "Data Structures", 3, prerequisites={"CS101"})

    # Add courses to department catalog
    cs_dept.add_course(cs101)
    cs_dept.add_course(cs201)

    # === PERSONNEL CREATION ===

    # Create various types of university personnel using historical figures
    prof_ada = Professor("F101", "Ada Lovelace", "1815-12-10", "Computer Science")
    lect_grace = Lecturer("F102", "Grace Hopper", "1906-12-09", "Computer Science")
    student_alan = UndergraduateStudent("S201", "Alan Turing", "1912-06-23", "CS", 3)
    staff_bob = Staff("ST301", "Bob Admin", "1980-05-15", "Admissions", "Administrator")

    # === ENROLLMENT DEMONSTRATION ===

    print("\n--- Course Enrollment Process ---")

    # Attempt to enroll student in courses
    student_alan.enroll_course(cs101, cs_dept)  # Should succeed - no prerequisites
    student_alan.enroll_course(cs201, cs_dept)  # Should fail - missing CS101 prerequisite

    # Simulate completion of CS101 by assigning a grade
    student_alan.enrolled_courses["CS101"] = 'A'  # Manual grade assignment for demo
    print("CS101 completed with grade 'A'")

    # Now CS201 enrollment should succeed
    student_alan.enroll_course(cs201, cs_dept)  # Should succeed now

    # === ACADEMIC PERFORMANCE CALCULATION ===

    print(f"\nAlan's GPA: {student_alan.calculate_gpa()}")
    print(f"Alan's Academic Status: {student_alan.get_academic_status()}")

    # === POLYMORPHISM DEMONSTRATION ===

    # Create a heterogeneous list of different person types
    university_people = [prof_ada, lect_grace, student_alan, staff_bob]

    print("\n--- Demonstrating Polymorphism ---")

    # Iterate through different person types using common interface
    for person in university_people:
        print(f"\nName: {person.name} ({person.__class__.__name__})")
        print("Responsibilities:")

        # All Person objects have get_responsibilities() method (polymorphism)
        for resp in person.get_responsibilities():
            print(f"- {resp}")

        # Check for faculty-specific methods using duck typing
        # This demonstrates how we can handle different object types gracefully
        if hasattr(person, 'calculate_workload'):
            print(f"Workload: {person.calculate_workload()}")

    # === ENCAPSULATION DEMONSTRATION ===

    print("\n--- Demonstrating Encapsulation ---")

    # Create secure student record with encapsulated data
    secure_record = SecureStudentRecord(student_alan, 3.8)
    print(f"Secure record for {secure_record.get_student_name()} has GPA: {secure_record.get_gpa()}")

    # Demonstrate validation in encapsulated setter
    try:
        # This should fail due to validation (GPA > 4.0)
        secure_record.set_gpa(5.0)
    except ValueError as e:
        print(f"Error setting invalid GPA: {e}")

    print("\n--- System Demonstration Complete ---")


# Standard Python idiom for running main function when script is executed directly
if __name__ == "__main__":
    main()
