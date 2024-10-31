import logging
import sys

from database.db_manager import DatabaseManager
from services.employee_service import EmployeeService
from utils.menu import print_usage
from utils.output_formatter import OutputFormatter
from utils.validators import ValidationError

logger = logging.getLogger(__name__)


def main():

    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
        
    logger.info("Starting program")    
    db_manager = DatabaseManager()
    employee_service = EmployeeService(db_manager)
    formatter = OutputFormatter()
    mode = sys.argv[1]
    
    try:
        if mode == '1':
            db_manager.create_tables()
            print("Table created successfully")
            
        elif mode == '2':
            if len(sys.argv) != 5:
                print("Usage: python main.py 2 \"<full_name>\" <birth_date> <gender>")
                sys.exit(1)

            employee = employee_service.add_employee(sys.argv[2], sys.argv[3], sys.argv[4])
            print(f"Employee {employee.full_name} added successfully")
            
        elif mode == '3':
            employees = employee_service.list_employees()
            
            for employee in employees:
                formatter.print_employee(employee)
                
        elif mode == '4':
            employee_service.generate_test_data()
            print("Test data generated successfully")
            
        elif mode == '5':
            rows, execution_time = employee_service.search_employees()
            formatter.print_search_results(rows, execution_time)
            
        elif mode == '6':
            print("Before optimization:")
            rows, time_before = employee_service.search_employees()
            formatter.print_search_results(rows, time_before)
            
            db_manager.create_indexes()
            print("\nAfter optimization:")
            rows, time_after = employee_service.search_employees()
            formatter.print_search_results(rows, time_after)
            
            print(f"\nTime after optimization: {time_after:.4f} seconds")
            print(f"\nTime before optimization: {time_before:.4f} seconds")
            print(f"\nOptimization improvement: {((time_before - time_after) / time_before * 100):.4f}%")
            
        else:
            print("Invalid mode")
            sys.exit(1)
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()