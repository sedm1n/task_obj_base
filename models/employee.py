import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class Employee:

    def __init__(self, full_name, birth_date, gender):
        self.full_name = full_name
        self.birth_date = birth_date
        self.gender = gender

    def calculate_age(self):
        """
        Calculate the age of the employee based on their birth date
        """
        birth_date = datetime.strptime(str(self.birth_date), "%Y-%m-%d")
        today = datetime.now()
        age = today.year - birth_date.year
        if today.month < birth_date.month or (
            today.month == birth_date.month and today.day < birth_date.day
        ):
            age -= 1
        return age

    def add_to_db(self, conn):
        """ "
        Add employee to database
        """
        with conn.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    INSERT INTO employees (full_name, birth_date, gender)
                    VALUES (%s, %s, %s)
                """,
                    (self.full_name, self.birth_date, self.gender),
                ))

            except Exception as e:
                logger.exception(f"Error adding employee: {str(e)}")
                raise ValueError(f"Error adding employee: {str(e)}")

        conn.commit()
