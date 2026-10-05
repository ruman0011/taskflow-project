```markdown
# TaskFlow

A Django task management dashboard for organizing projects and tracking tasks.

**Built by Md Ruman Mia**

## Features

- Create and manage projects
- Create, edit, and delete tasks
- Set task status, priority, and due date
- Search tasks and filter by status
- See overdue tasks at a glance
- Sign up, log in, and log out
- Keep each user's projects and tasks separate

## Built With

- Python
- Django
- SQLite
- HTML and CSS

## Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/ruman0011/taskflow-project.git
   cd taskflow-project
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:

   ```bash
   python manage.py migrate
   ```

5. Start the development server:

   ```bash
   python manage.py runserver
   ```

6. Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## Notes

- SQLite is used for local development.
- Keep secret keys and other private settings out of the repository.
- Before deploying publicly, configure Django's production security settings and use a production-ready database and hosting setup.

## Author

**Md Ruman Mia**
```
