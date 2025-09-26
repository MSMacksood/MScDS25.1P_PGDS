from person import Person

class Faculty(Person):
    """Base class for academic faculty."""
    def __init__(self, person_id, name, birth_date, department, rank):
        super().__init__(person_id, name, birth_date)
        self.department = department
        self.rank = rank

    def calculate_workload(self):
        return "Base workload calculation."

    def get_responsibilities(self):
        base_resp = super().get_responsibilities()
        base_resp.append("Conduct research and publish findings.")
        return base_resp

class Professor(Faculty):
    def __init__(self, person_id, name, birth_date, department):
        super().__init__(person_id, name, birth_date, department, "Professor")
        self.tenured = False

    def calculate_workload(self):
        return "Teaches 2 courses, advises 5 graduate students, serves on 1 committee."

class Lecturer(Faculty):
    def __init__(self, person_id, name, birth_date, department):
        super().__init__(person_id, name, birth_date, department, "Lecturer")

    def calculate_workload(self):
        return "Teaches 4 courses."

    def get_responsibilities(self):
        # Override to remove research responsibility
        return ["Adhere to university policies.", "Focus on teaching and student instruction."]

class TA(Faculty):
    def __init__(self, person_id, name, birth_date, department, assisting_course):
        super().__init__(person_id, name, birth_date, department, "Teaching Assistant")
        self.assisting_course = assisting_course

    def calculate_workload(self):
        return f"Assists with {self.assisting_course.name}, holds office hours."
