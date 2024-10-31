import logging
import random
import string
import time

from psycopg2.extras import execute_batch

from models.employee import Employee
from utils.decorators import measure_time
from utils.validators import EmployeeValidator, ValidationError

logger = logging.getLogger(__name__)


class EmployeeService:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def add_employee(self, full_name, birth_date, gender):
        """
        Add an employee to the database.

        :param full_name: The full name of the employee
        :param birth_date: The birth date of the employee
        :param gender: The gender of the employee
        :return: The added employee
        :raises ValidationError: If the input data is invalid
        :raises Exception: If there was an unexpected error
        """
        try:

            validated_name = EmployeeValidator.validate_full_name(full_name)
            validated_date = EmployeeValidator.validate_date(birth_date)
            validated_gender = EmployeeValidator.validate_gender(gender)

            conn = self.db_manager.get_connection()
            employee = Employee(validated_name, validated_date, validated_gender)

            employee.add_to_db(conn)

            conn.close()

            logger.info(f"Employee {full_name} added successfully")
            return employee

        except ValidationError as e:
            logger.exception(f"Validatin error adding employee: {str(e)}")
            raise ValidationError(f"Validation error: {str(e)}")

        except Exception as e:
            logger.exception(f"Error adding employee: {str(e)}")
            raise Exception(f"Error adding employee: {str(e)}")

    @measure_time
    def list_employees(self):
        """
        List all employees in the database.

        :return: A list of Employee objects representing all employees in the database
        :raises Exception: If there was an unexpected error
        """
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT DISTINCT full_name, birth_date, gender
                FROM employees
                ORDER BY full_name
            """
            )

            rows = cursor.fetchall()
            conn.close()
        except Exception as e:
            logger.exception(f"Error listing employees: {str(e)}")

        return [Employee(row[0], row[1], row[2]) for row in rows]

    @measure_time
    def search_employees(self):
        """
        Search employees in the database based on criteria.

        :return: A tuple containing a list of Employee objects representing the search results
            and the time taken to execute the query
        :raises ValueError: If there was an unexpected error
        """
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        start_time = time.time()

        try:
            cursor.execute(
                """                       
            SELECT DISTINCT full_name, birth_date, gender
            FROM employees
            WHERE gender = 'Male' AND full_name LIKE 'F%'
            ORDER BY full_name
        """
            )

        except Exception as e:
            logger.exception(f"Error listing employees: {str(e)}")
            raise ValueError(f"Error searching employees: {str(e)}")

        rows = cursor.fetchall()
        end_time = time.time()

        conn.close()
        return rows, end_time - start_time

    def generate_random_name(self, start_letter=None):
        """
        Generates a random name for an employee, with the given start letter.

        :param start_letter: The first letter of the last name, if any
        :return: A string representing a random name
        """

        first_names = [
            "John",
            "James",
            "Robert",
            "Michael",
            "William",
            "David",
            "Richard",
            "Charles",
            "Joseph",
            "Thomas",
        ]
        middle_names = [
            "Alexander",
            "Benjamin",
            "Christopher",
            "Daniel",
            "Edward",
            "Frederick",
            "George",
            "Henry",
            "Isaac",
        ]

        if start_letter:
            last_names = [
                f"{start_letter}{surname}"
                for surname in ["oster", "ranks", "ord", "isher", "owler"]
            ]
        else:
            last_names = [
                f"{letter}{surname}"
                for letter in string.ascii_uppercase
                for surname in ["oster", "ranks", "ord", "isher", "owler"]
            ]

        return f"{random.choice(last_names)} {random.choice(first_names)} {random.choice(middle_names)}"

    def generate_random_date(self):
        """
        Generates a random date between the years 1950 and 2005.

        :return: A string representing a random date in the format 'YYYY-MM-DD'
        """
        year = random.randint(1950, 2005)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        return f"{year}-{month:02d}-{day:02d}"

    def bulk_insert(self, employees):
        """
        Inserts a list of Employee objects into the database in bulk.

        :param employees: A list of Employee objects to be inserted into the database.
        :raises ValueError: If there was an error during the database insertion.
        """
        conn = self.db_manager.get_connection()
        with conn.cursor() as cursor:
            try:
                execute_batch(
                    cursor,
                    """
                    INSERT INTO employees (full_name, birth_date, gender)
                    VALUES (%s, %s, %s)
                """,
                    [(emp.full_name, emp.birth_date, emp.gender) for emp in employees],
                    page_size=1000,
                )
                conn.commit()
                conn.close()

            except Exception as e:
                logger.exception(f"Error inserting employees: {str(e)}")
                raise ValueError(f"Error bulk inserting employees: {str(e)}")

    @measure_time
    def generate_test_data(self):
        """
        Generates test data for the application.

        Generates 1,000,000 random employee records with an even distribution of gender and last name.
        Also generates 100 male employee records with the last name starting with 'F'.

        :return: A tuple containing the time taken to execute the query
        :raises ValueError: If there was an error during the database insertion.
        """
        batch_size = 10000
        employees = []

        # Generate 1,000,000 random employees
        for _ in range(1000000):
            name = self.generate_random_name()
            date = self.generate_random_date()
            gender = random.choice(["Male", "Female"])
            employees.append(Employee(name, date, gender))

            if len(employees) == batch_size:
                self.bulk_insert(employees)
                employees = []

        # Generate 100 male employees with 'F' surnames
        for _ in range(100):
            name = self.generate_random_name("F")
            date = self.generate_random_date()
            employees.append(Employee(name, date, "Male"))

        if employees:
            self.bulk_insert(employees)
