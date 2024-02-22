# ExpensEase
Multi-purpose budgeting tool, 2023-2024 coursework at UoP.

## Names, Student IDs & GitHub IDs - In that order
- Erdit, up2115603, 19395781<br>
- Toby, up2120860, 128059876<br>
- George, up2117604, 146346646<br>
- Paul, up2203365, 64145882<br>
- Ben, up2058403, 147066158<br>
- Andreas, up2151158, 128136527<br>
- Elsayed, up968829, 115377482<br>
---
## How to Use
The project runs through cross-origin resource sharing for development and testing.

### Backend
Backend is developed using Python version 3.11.7. Any other version of Python has not been tested. This guide assumes you also have pip installed.

#### Creating a virtual environment
It's good practise to create a virtual environment to keep everything seperate. Here is how you do this.

Use the `venv` module to create a virtual environment.
```
python -m venv myenv
```

Activate the virtual environment.

On **Windows**:
```
myenv\Scripts\activate
```
On **macOS and Linux**:
```
source myenv/bin/activate
```

To then have all the necessary python dependencies installed on your new virtual environment, use the `requirements.txt` file. This file can be found in `/backend`

You can do this by running in your terminal or command prompt, whilst in the activated virtual environment:
```
pip install -r requirements.txt
```

---

### Setup PostgreSQL database
You must have a locally running postgres database to use the backend and run the project.

**Windows**
* Download and install PostgreSQL from the official website.
* During installation, set up a username and password for the database.
* Once installed, open pgAdmin (included with PostgreSQL) and create a new database named 'expensease'.
* Open SQL Query tool in pgAdmin and execute the SQL script (located in `/database/DBCreationSQL.sql`) to create tables and relationships.

**Mac**
* Install PostgreSQL using Homebrew: `brew install postgresql`.
* Start the PostgreSQL service: `brew services start postgresql`.
* Access the PostgreSQL command line: `psql postgres`.
* Create a new user and database:
```sql
CREATE USER username WITH PASSWORD 'password';
CREATE DATABASE expensease;
GRANT ALL PRIVILEGES ON DATABASE expensease TO username;
```
* Exit the PostgreSQL command line and run the SQL script using `psql -U username -d expensease -a -f DBCreationSQL.sql`.

**Linux**
Install PostgreSQL using your package manager (`apt`, `yum`, etc.).
Start the PostgreSQL service: `sudo service postgresql start`.
Access the PostgreSQL command line: `sudo -u postgres psql`.
Create a new user and database:
```sql
CREATE USER username WITH PASSWORD 'password';
CREATE DATABASE expensease;
GRANT ALL PRIVILEGES ON DATABASE expensease TO username;
```
* Exit the PostgreSQL command line and run the SQL script using `psql -U username -d expensease -a -f DBCreationSQL.sql`.

#### Adjust the .env file
In the `/backend` folder, there is a `.env-example` file. Create a new file just called `.env` with the same data as the `.env-example` file.
```
FLASK_APP=run.py
FLASK_ENV=development
DATABASE_URL=postgresql://username:password@localhost/expensease
SECRET_SESSION_KEY=SKGNaJDK1d034cma!l1
```

Replace `username` and `password` in the DATABASE_URL with the credentials you set up during PostgreSQL installation.

---

After this is done, the backend is ran by running the `run.py` file. This file would then create the Flask backend in development mode. Your IDE can handle the running of the python file, or you can simply just run `python run.py` to run it in a terminal or command line.