#Test Task: Employee Directory Console Application

This console-based application provides efficient management of an employee directory, integrating seamlessly with PostgreSQL to support core functionalities essential for database-driven environments. Key features include:

Database Management: Set up and manage tables within PostgreSQL, ensuring structured storage for employee data.
Employee Records: Add, update, and list employee records with ease, providing a user-friendly interface for data management.
Data Generation: Generate test data automatically, facilitating testing and demonstration of the application.
Search and Filtering: Search employees based on specific criteria, leveraging optimized queries to ensure quick retrieval.
Performance Optimization: Enhanced filtering speed by creating a composite index on the gender and full_name fields. This improvement reduced filtering times from 0.1604 seconds to 0.1329 seconds, yielding a performance improvement of 20.67%.
This project demonstrates an emphasis on optimization and scalability, making it a robust solution for managing employee information in various organizational contexts.


##Installation and Setup
Prerequisites
Python 3.11 or higher
PostgreSQL installed and running


##Installation

###Install dependencies:

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

python main.py 1
```
Add Employee: Adds a new employee record. Requires full name, birth date, and gender as arguments.

```bash


python main.py 2 "<full_name>" <birth_date> <gender>
```
Example:

```
bash
python main.py 2 "John Doe Smith" 1990-01-15 male
```
Supported date formats: YYYY-MM-DD, DD.MM.YYYY, DD/MM/YYYY, YYYY/MM/DD

List All Employees: Displays all employee records, ordered by full name.

```
bash
python main.py 3
```
Generate Test Data: Automatically generates 1,000,000 employee records with even distribution of gender and initials, including 100 male records starting with "F".

```bash

python main.py 4
```
Search Employees: Finds all male employees whose last names start with "F". Displays time taken to execute.

```bash
python main.py 5
```
Optimize Performance: Applies database optimizations for faster query execution on search tasks. Outputs time comparisons before and after optimization.

```bash
python main.py 6
```