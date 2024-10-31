from models.employee import Employee


class OutputFormatter:
    @staticmethod
    def print_employee(employee: Employee):
        age = employee.calculate_age()
        
        print(f"Name: {employee.full_name}, Birth Date: {employee.birth_date}, "
              f"Gender: {employee.gender}, Age: {age}")
    
    @staticmethod
    def print_search_results(rows, execution_time):
        
        for row in rows:
            employee = Employee(row[0], row[1], row[2])
            OutputFormatter.print_employee(employee)
        
        print(f"\nFound {len(rows)} employees")
        print(f"\nQuery execution time: {execution_time:.4f} seconds")