def print_usage():
    print("""
Usage: python myApp.py <mode> [arguments]

Modes:
1 - Create tables
2 - Add employee: python myApp.py 2 "<full_name>" <birth_date> <gender>
    Example: python myApp.py 2 "John Doe Smith" 1990-01-15 male
    Supported date formats: YYYY-MM-DD, DD.MM.YYYY, DD/MM/YYYY, YYYY/MM/DD
3 - List all employees
4 - Generate test data
5 - Search employees
6 - Optimize and compare performance

Notes:
- Full name should contain at least first and last name
- Gender should be 'male' or 'female' (case insensitive)
- Birth date must be between 1900 and current date
    """)