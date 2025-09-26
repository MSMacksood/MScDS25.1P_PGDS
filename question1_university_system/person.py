import datetime

class Person:
    """Base class for all individuals in the university system."""
    def __init__(self, person_id, name, birth_date):
        self.person_id = person_id
        self.name = name
        self.birth_date = birth_date

    def get_age(self):
        today = datetime.date.today()
        birth_date_obj = datetime.datetime.strptime(self.birth_date, "%Y-%m-%d").date()
        return today.year - birth_date_obj.year - ((today.month, today.day) < (birth_date_obj.month, birth_date_obj.day))

    def get_responsibilities(self):
        return ["Adhere to university policies."]

    def __str__(self):
        return f"{self.name} (ID: {self.person_id})"

class Staff(Person):
    """Represents a staff member of the university."""
    def __init__(self, person_id, name, birth_date, department, role):
        super().__init__(person_id, name, birth_date)
        self.department = department
        self.role = role

    def get_responsibilities(self):
        base_resp = super().get_responsibilities()
        base_resp.append(f"Perform {self.role} duties for the {self.department} department.")
        return base_resp
