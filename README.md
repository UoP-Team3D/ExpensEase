# ExpensEase

Multi-purpose budgeting tool, 2023-2024 coursework at UoP.

## Names, Student IDs & GitHub IDs - In that order

- Erdit, up2115603, 19395781
- Toby, up2120860, 128059876
- George, up2117604, 146346646
- Paul, up2203365, 64145882
- Ben, up2058403, 147066158
- Andreas, up2151158, 128136527
- Elsayed, up968829, 115377482

---

## Contribution Convention

Please follow Conventional Commits (https://www.conventionalcommits.org/en/v1.0.0/#summary) as a guide for writing good commit messages when pushing to the repository, this helps everyone understand exactly what you pushed to the repository by just glancing at the commit messages.

## How to Use

The project runs through cross-origin resource sharing for development and testing.

### Backend

Backend is developed using Python version 3.11.7 (3.11.8 has been tested too). Any other version of Python has not been tested. This guide assumes you also have pip installed.

#### Download Tesseract for OCR Scanning

Tesseract is an open-source OCR engine used by `pytesseract` for optical character recognition (reading receipt images). Follow these steps to set up Tesseract on your system:

On **Windows**

1. Download the Tesseract installer for Windows from the following link: https://github.com/UB-Mannheim/tesseract/wiki
2. Run the installer and follow the installation wizard.
3. During installation, make sure to select the option to install the English language pack.
4. Add the Tesseract installation directory (e.g., C:\Program Files\Tesseract-OCR) to your system's PATH environment variable.

On **macOS**

Install Tesseract using Homebrew by running the following command in the terminal:

```
brew install tesseract
```

Homebrew will automatically install the English language pack along with Tesseract.

On **Linux**:

Install Tesseract using your package manager. For example, on Ubuntu or Debian:

```
sudo apt-get install tesseract-ocr
```

Install the English language pack:

```
sudo apt-get install tesseract-ocr-eng
```

After installing Tesseract, pytesseract should be able to use it without any additional configuration.

#### Creating a virtual environment

It's good practise to create a virtual environment to keep everything seperate. Here is how you do this.

Use the `venv` module to create a virtual environment.

```
python -m venv env
```

Activate the virtual environment.

On **Windows**:

```
env\Scripts\activate
```

On **macOS and Linux**:

```
source env/bin/activate
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

#### Dropping Database (if needed)

Chances are the database is going to change during development to accomodate for features or adaptations in the project. To remove the existing tables and recreate the new schema, psql into the database and then run:

```sql
DROP TABLE IF EXISTS public."Budget";
DROP TABLE IF EXISTS public."Category";
DROP TABLE IF EXISTS public."Expense";
DROP TABLE IF EXISTS public."Income";
DROP TABLE IF EXISTS public."Users";
```

Recreate the database by referring to the above.

#### Create Testing DB

Unit testing relies on a "testing" database, this database is 1:1 with the above one, just an empty clone of it named "expensease_test". Create it in the exact same way you created the above, main database.

#### Adjust the .env file

In the `/backend` folder, there is a `.env-example` file. Create a new file just called `.env` with the same data as the `.env-example` file.

```
FLASK_APP=run.py
FLASK_ENV=development
TESTING=true
DATABASE_URL=postgresql://username:password@localhost/expensease
TEST_DATABASE_URL=postgresql://username:password@localhost/expensease_test
SECRET_SESSION_KEY=SKGNaJDK1d034cma!l1
```

Replace `username` and `password` in the DATABASE_URL with the credentials you set up during PostgreSQL installation.

### Running The Unit Tests

When introducing big changes to the backend, or minor, run `pytest` whilst in the `backend` folder to ensure every unit test passes. It's often a good idea to run `pytest` after every pull too so you can pinpoint any issue that may happen whilst developing the project.

---

After this is done, the backend is ran by running the `run.py` file. This file would then create the Flask backend in development mode. Your IDE can handle the running of the python file, or you can simply just run `python run.py` to run it in a terminal or command line.

### Frontend

# ExpensEase

Multi-purpose budgeting tool, 2023-2024 coursework at UoP.

## Names, Student IDs & GitHub IDs - In that order

- Erdit, up2115603, 19395781
- Toby, up2120860, 128059876
- George, up2117604, 146346646
- Paul, up2203365, 64145882
- Ben, up2058403, 147066158
- Andreas, up2151158, 128136527
- Elsayed, up968829, 115377482

---

## Contribution Convention

Please follow Conventional Commits (https://www.conventionalcommits.org/en/v1.0.0/#summary) as a guide for writing good commit messages when pushing to the repository, this helps everyone understand exactly what you pushed to the repository by just glancing at the commit messages.

## How to Use

The project runs through cross-origin resource sharing for development and testing.

### Backend

Backend is developed using Python version 3.11.7 (3.11.8 has been tested too). Any other version of Python has not been tested. This guide assumes you also have pip installed.

#### Download Tesseract for OCR Scanning

Tesseract is an open-source OCR engine used by `pytesseract` for optical character recognition (reading receipt images). Follow these steps to set up Tesseract on your system:

On **Windows**

1. Download the Tesseract installer for Windows from the following link: https://github.com/UB-Mannheim/tesseract/wiki
2. Run the installer and follow the installation wizard.
3. During installation, make sure to select the option to install the English language pack.
4. Add the Tesseract installation directory (e.g., C:\Program Files\Tesseract-OCR) to your system's PATH environment variable.

On **macOS**

Install Tesseract using Homebrew by running the following command in the terminal:

```
brew install tesseract
```

Homebrew will automatically install the English language pack along with Tesseract.

On **Linux**:

Install Tesseract using your package manager. For example, on Ubuntu or Debian:

```
sudo apt-get install tesseract-ocr
```

Install the English language pack:

```
sudo apt-get install tesseract-ocr-eng
```

After installing Tesseract, pytesseract should be able to use it without any additional configuration.

#### Creating a virtual environment

It's good practise to create a virtual environment to keep everything seperate. Here is how you do this.

Use the `venv` module to create a virtual environment.

```
python -m venv env
```

Activate the virtual environment.

On **Windows**:

```
env\Scripts\activate
```

On **macOS and Linux**:

```
source env/bin/activate
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

#### Dropping Database (if needed)
| :memo:        | Take note of this       |
|---------------|:------------------------|

Chances are the database is going to change during development to accomodate for features or adaptations in the project. To remove the existing tables and recreate the new schema, psql into the database and then run:

```sql
DROP TABLE IF EXISTS public."Budget";
DROP TABLE IF EXISTS public."Category";
DROP TABLE IF EXISTS public."Expense";
DROP TABLE IF EXISTS public."Income";
DROP TABLE IF EXISTS public."Users";
```

Recreate the database by referring to the above. If you're not sure if you need to modify the database, run `pytest` and see if you get any errors, chances are those errors may be due to an outdated database.

#### Create Testing DB

Unit testing relies on a "testing" database, this database is 1:1 with the above one, just an empty clone of it named "expensease_test". Create it in the exact same way you created the above, main database.

#### Adjust the .env file

In the `/backend` folder, there is a `.env-example` file. Create a new file just called `.env` with the same data as the `.env-example` file.

```
FLASK_APP=run.py
FLASK_ENV=development
TESTING=true
DATABASE_URL=postgresql://username:password@localhost/expensease
TEST_DATABASE_URL=postgresql://username:password@localhost/expensease_test
SECRET_SESSION_KEY=SKGNaJDK1d034cma!l1
```

Replace `username` and `password` in the DATABASE_URL with the credentials you set up during PostgreSQL installation.

### Running The Unit Tests

When introducing big changes to the backend, or minor, run `pytest` whilst in the `backend` folder to ensure every unit test passes. It's often a good idea to run `pytest` after every pull too so you can pinpoint any issue that may happen whilst developing the project.

---

After this is done, the backend is ran by running the `run.py` file. This file would then create the Flask backend in development mode. Your IDE can handle the running of the python file, or you can simply just run `python run.py` to run it in a terminal or command line.

### Frontend
| :boom: DANGER              |
|:---------------------------|
| **AS OF *02/05/2024*, EXPENSEASE DOESN'T USE CORS ANYMORE. FRONTEND AND BACKEND RUN TOGETHER** |

To get frontend running with backend, follow these instructions carefully:

Option A (automated):

In the `frontend` folder, after your frontend work, you may run the `run.bat` file and it will automatically build, relocate the folder and run the backend for you. **THIS ASSUMES YOUR VIRTUAL ENVIRONMENT IS NAMED "`env`"! and is located in `backend`**.

| :exclamation:              |
|:---------------------------|
| Note: you may have to manually run `python run.py`, or run the `run.py` file in the Python folder yourself, due to virtual enviroment constrictions. |

Option B (manual):

1. `cd` into `frontend`, run `npm install` to install all dependencies used by the frontend
2. run `npm run build`, once complete, a new folder called `build` will be located in the `frontend` folder.
3. Copy this `build` folder from the `frontend` folder into the `backend` folder. Put it directly into the `backend` folder, not into any subfolders that exist inside `backend`.
4. Run `python run.py` to run both simultaneously.
5. Open the app in a browser using `127.0.0.1:5000/`. Using `localhost:5000/` will **NOT** work.

If you run the frontend using `npm start` via `frontend`, it will ***NOT*** work with the backend. You MUST follow the instructions above to get both running properly and together.