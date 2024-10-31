#Test Task: Employee Directory Console Application

A console-based application for managing an employee directory with PostgreSQL integration. The application supports various functionalities, such as creating tables, adding employee records, listing all employees, generating test data, searching by criteria, and optimizing performance.

Installation and Setup
Prerequisites
Python 3.11 or higher
PostgreSQL installed and running


Installation

Install dependencies:

```bash

pip install -r requirements.txt
```
Configure your PostgreSQL database in config.py or by setting appropriate environment variables. Ensure the database is created and ready for use.

Database Configuration
Make sure to have a PostgreSQL user and database created. Example configuration in .env:

```bash
DB_NAME=employee
DB_USER=postgres
DB_PASSWORD=mysecretpassword
DB_HOST=localhost
DB_PORT=5433
```
Running the Application
The application is invoked from the command line with various parameters to select different modes:

Create Tables: Initializes the employees table in the database.

```bash

python myApp.py 1
```
Add Employee: Adds a new employee record. Requires full name, birth date, and gender as arguments.

```bash


python myApp.py 2 "<full_name>" <birth_date> <gender>
```
Example:

```
bash
python myApp.py 2 "John Doe Smith" 1990-01-15 male
```
Supported date formats: YYYY-MM-DD, DD.MM.YYYY, DD/MM/YYYY, YYYY/MM/DD

List All Employees: Displays all employee records, ordered by full name.

```
bash
python myApp.py 3
```
Generate Test Data: Automatically generates 1,000,000 employee records with even distribution of gender and initials, including 100 male records starting with "F".

```bash

python myApp.py 4
```
Search Employees: Finds all male employees whose last names start with "F". Displays time taken to execute.

```bash
python myApp.py 5
```
Optimize Performance: Applies database optimizations for faster query execution on search tasks. Outputs time comparisons before and after optimization.

```bash
python myApp.py 6
```