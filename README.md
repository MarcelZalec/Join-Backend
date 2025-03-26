# Task Management API

This project is a Django-based API for managing tasks, subtasks, users, and contacts. It is designed to support features such as user authentication, task assignment, and contact management.

## Table of Contents

- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

These instructions will help you set up and run the project on your local machine for development and testing purposes.

### Prerequisites

- Python 3.12 or higher
- Django 5.1 or higher
- Django Rest Framework
- Postman (optional, for API testing)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/MarcelZalec/Join-Backend.git
   cd your-repo-name
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database:**
   - Run the migrations to create the necessary database tables:
     ```bash
     python manage.py migrate
     ```

5. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

## Contributing

Contributions are welcome! Please create an issue first to discuss what you would like to change. You can also fork the repository, make changes, and submit a pull request.