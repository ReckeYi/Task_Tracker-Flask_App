# Task_Tracker-Flask_App

**Live project can be found [here](http://flask-task.tw1.su:5000/)**

The project was created to demonstrate practical skills related to the Flask framework.

A significant functional part of the application goes far beyond the scope of standard applications from tutorials.

You can create and edit projects, task lists and configure access levels for users. You can also sort lists, search by keywords, and customize the amount objects displayed on the page.
In case you forgot your account password, you can recover it using the password recovery option.

**List of used technologies:**
- Flask
- SQL Alchemy
- PostgreSQL
- Alembic
- Bootstrap
- Nginx
- Docker
- Docker Compose
- Ubuntu Server: live version

**Requirements:**
  - Python 3.9.13

**Installation:**
  1. **Download project**
  2. **Install modules** from requirements.txt ([how to install](https://note.nkmk.me/en/python-pip-install-requirements/))
  3. **[Download PostgreSQL](https://www.postgresql.org/)** and [install your database](https://www.youtube.com/watch?v=KuQUNHCeKCk)
  4. **Create and configure your mail client** for [Google](https://support.google.com/a/answer/176600?hl=en) or [Yandex](https://yandex.com/support/mail/mail-clients/others.html)
  5. **Set up _config.py_** file:
     ```python
     SQLALCHEMY_DATABASE_URI = 'postgresql://your_db_user:your_db_password@localhost:5432/db_name'
     MAIL_SERVER = 'smtp.yandex.ru'
     MAIL_PORT = 465
     MAIL_USE_TLS = False
     MAIL_USE_SSL = True
     MAIL_USERNAME = 'your_email_user (copy only your username that comes before @yandex.ru)'
     MAIL_PASSWORD = 'your_app_password'
     ```
  6. **Configure the environment variable**. Open terminal, run the command:
     ```
     $env:FLASK_APP="run.py"
     ```
  7. **Set up a database** in command window:
     - open terminal
     - to init datda base run command:
        ```
        flask db init
        ```
     - Create initial migration:
       ```
        flask db migrate -m 'Initial migration’
       ```
     - Upgrade database:
       ```
        flask db upgrade
       ```
  8. **Run the app**: run the _'run.py'_ file
  9. **Open** [/home](http://127.0.0.1:5000/) page
  10. **Push ‘_Add Dummy Data_’ button** to add some dummy data to your database
  11. Optional: **Open the templates/home.html file and delete** code from line 32:
       ```html
       <p><a href="{{ url_for('dummy_data.add_dummy_data') }}"><button type="button" class="btn btn-sm btn-danger">Add Dummy Data</button></a></p>
       ```
  12. **[Register](http://127.0.0.1:5000/register) your account** to get full access to all features.
