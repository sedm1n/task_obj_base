import re
from datetime import datetime


class ValidationError(Exception):
    pass


class EmployeeValidator:

    DATE_FORMATS = [
        "%d.%m.%Y",  # 24.07.1952
        "%Y-%m-%d",  # 1952-07-24
        "%d/%m/%Y",  # 24/07/1952
        "%Y/%m/%d",  # 1952/07/24
    ]

    @staticmethod
    def validate_full_name(full_name):
        """
             Validates a full name to ensure it is properly formatted.

        :param full_name: The full name to validate.
        :type full_name: str
        :raises ValidationError: If the full name is less than 2 characters long,
                                contains characters other than letters, spaces, or hyphens,
                                or does not have at least a first name and a last name.
        :return: The capitalized full name if valid.
        :rtype: str
        """
        if not full_name or len(full_name.strip()) < 2:
            raise ValidationError("Full name must be at least 2 characters long")

        if not re.match(r"^[A-Za-z\s-]+$", full_name):
            raise ValidationError(
                "Full name must contain only letters, spaces, and hyphens"
            )

        parts = full_name.split()
        if len(parts) < 2:
            raise ValidationError(
                "Full name must contain at least first name and last name"
            )

        return " ".join(part.capitalize() for part in parts)

    @staticmethod
    def validate_date(date_str):
        """
            Validates a date string to ensure it is properly formatted and within the valid range.

        :param date_str: The date string to validate.
        :type date_str: str
        :raises ValidationError: If the date string is empty, in the future, or before 1900,
                                or if it does not match any of the supported date formats.
        :return: The validated date string in the format 'YYYY-MM-DD'.
        :rtype: str
        """
        if not date_str:
            raise ValidationError("Birth date cannot be empty")

        for date_format in EmployeeValidator.DATE_FORMATS:
            try:
                date_obj = datetime.strptime(date_str, date_format)

                if date_obj.date() > datetime.now().date():
                    raise ValidationError("Birth date cannot be in the future")
                if date_obj.year < 1900:
                    raise ValidationError("Birth date cannot be earlier than 1900")

                return date_obj.strftime("%Y-%m-%d")
            except ValueError:
                continue

        raise ValidationError(
            "Invalid date format. Supported formats are: DD.MM.YYYY, YYYY-MM-DD, DD/MM/YYYY, YYYY/MM/DD"
        )

    @staticmethod
    def validate_gender(gender):
        """
            Validates a gender string to ensure it is properly formatted.

        :param gender: The gender string to validate.
        :type gender: str
        :raises ValidationError: If the gender string is empty or not 'male' or 'female'.
        :return: The validated gender string in the format 'Male' or 'Female'.
        :rtype: str
        """
        
        if not gender:
            raise ValidationError("Gender cannot be empty")

        gender_normalized = gender.lower()
        if gender_normalized not in ["male", "female"]:
            raise ValidationError("Gender must be 'male' or 'female'")

        return gender.capitalize()
