# Task_Tracker-Flask_App

This is a pet project created with the goal of gaining practical skills to consolidate knowledge about the Flask framework.
A significant functional part of the application goes far beyond the scope of standard applications from tutorials.
You can create and edit projects, task lists and configure access levels for users. You can also sort lists, search by keywords, and customize the amount objects displayed on the page. If you forget your account password, you can recover it using the password recovery function.

**List of used technologies:**
- Flask
- SQL Alchemy
- PostgreSQL
- Alembic
- Bootstrap

**Requirements:**
  - Python 3.9.13

**Installation:**
  1. Download project
  2. Install modules from requirements.txt
  3. Setup config file
  4. Setup FLASK_APP environment variable: $env:FLASK_APP="[run.py](http://run.py/)"
  5. Setup a database in command window:
     - Init datda base: flask db init
     - Create initial migration: flask db migrate -m 'Initial migration’
     - Upgrade database: flask db upgrade
  6. Run the app: run 'run.py' file
  7. Open [/home](http://127.0.0.1:5000/) page
  8. Push ‘Add Dummy Data’ button to add some dummy data to your database
  9. Open the templates/home.html file and delete code from line 32:
      ```
      <p><a href="{{ url_for('dummy_data.add_dummy_data') }}"><button type="button" class="btn btn-sm btn-danger">Add Dummy Data</button></a></p>
      ```
  10. Register your account to get full access to features
