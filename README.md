# DjangoBankingSystem

## Description
This repository hosts a Django-based backend for a banking application, organized into modular apps for different functionalities, such as `accounts` and `banks`. It is designed to handle user authentication, account management, and banking operations.

## Project Structure
- `accounts/`: Contains user-related functionalities like registration, login, and profile management.
- `banks/`: Manages bank-related operations and models.
- `general/`: General components used across the application.
- `mysite/`: The main Django project directory with global settings.
- `.gitignore`: Specifies untracked files to ignore.
- `LICENSE`: The license file for the project.
- `Makefile`: A script for automating common administrative tasks.
- `README.md`: Documentation of the project (this file).
- `db.sqlite3`: The SQLite database file.
- `manage.py`: A command-line utility for administrative tasks.

## How to Run
1. Ensure that you have Python and Django installed on your system.
2. Navigate to the project's root directory.
3. Run the following commands to set up the application:
   ```python manage.py makemigrations
   python manage.py migrate```
5. To start the development server, execute:
6. Access the application through `localhost:8000` in your web browser.

## Technologies Used
- Django
- Python

## Learning Outcomes
This project provided hands-on experience with Django's MVC framework for building a feature-rich banking system backend. It involved implementing models, views, and controllers for user and bank management, as well as integrating user authentication and session handling.

## Acknowledgments
This project was developed as part of CSC309-Programming on Web. Special thanks to Instructor Jack Sun for guidance and support.
