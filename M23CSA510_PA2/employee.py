class Employee:
    def __init__(self, employee_id: int, name: str, department: str, salary: float):
        self.employee_id: int = employee_id
        self.name: str = name
        self.department: str = department
        self.salary: float = salary

    def __repr__(self):
        return f"Employee(ID: {self.employee_id}, Name: {self.name}, Dept: {self.department}, Salary: {self.salary})"
