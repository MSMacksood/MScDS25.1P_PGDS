
# main.py
from person import Staff
from student import UndergraduateStudent, SecureStudentRecord
from faculty import Professor, Lecturer
from department import Department, Course

def main():
    print("--- University Management System ---")

    # Create Departments and Courses
    cs_dept = Department("Computer Science")
    cs101 = Course("CS101", "Intro to Programming", 3, prerequisites=None)
    cs201 = Course("CS201", "Data Structures", 3, prerequisites={"CS101"})
    cs_dept.add_course(cs101)
    cs_dept.add_course(cs201)

    # Create People
    prof_ada = Professor("F101", "Ada Lovelace", "1815-12-10", "Computer Science")
    lect_grace = Lecturer("F102", "Grace Hopper", "1906-12-09", "Computer Science")
    student_alan = UndergraduateStudent("S201", "Alan Turing", "1912-06-23", "CS", 3)
    staff_bob = Staff("ST301", "Bob Admin", "1980-05-15", "Admissions", "Administrator")
    
    # Enroll student
    student_alan.enroll_course(cs101, cs_dept)
    student_alan.enroll_course(cs201, cs_dept) # Fails due to prereq
    student_alan.enrolled_courses["CS101"] = 'A' # Manually assign grade for demo
    student_alan.enroll_course(cs201, cs_dept) # Succeeds now
    
    print(f"\nAlan's GPA: {student_alan.calculate_gpa()}")
    print(f"Alan's Status: {student_alan.get_academic_status()}")

    # Polymorphism in action
    university_people = [prof_ada, lect_grace, student_alan, staff_bob]

    print("\n--- Demonstrating Polymorphism ---")
    for person in university_people:
        print(f"\nName: {person.name} ({person.__class__.__name__})")
        print("Responsibilities:")
        for resp in person.get_responsibilities():
            print(f"- {resp}")
        
        # Using hasattr to check for faculty-specific methods
        if hasattr(person, 'calculate_workload'):
            print(f"Workload: {person.calculate_workload()}")
            
    # Encapsulation example
    secure_record = SecureStudentRecord(student_alan, 3.8)
    print(f"\nSecure record for {secure_record.get_student_name()} has GPA: {secure_record.get_gpa()}")
    try:
        secure_record.set_gpa(5.0)
    except ValueError as e:
        print(f"Error setting GPA: {e}")


if __name__ == "__main__":
    main()
