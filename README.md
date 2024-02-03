# LunchWars

A django webapp for employees to vote on which restaurant should provide lunch for the office.

## Tech Stack
- Django
- Celery
- Redis
- PostgreSQL
- Tailwind CSS

## Instructions
- Clone the repo using `git clone https://github.com/devyneX/LunchWars.git`
- cd into the project directory using `cd LunchWars`
- Create a virtual environment and install dependencies using the following commands 
```
conda create -n lunchwars python=3.9
conda activate lunchwars
pip install -r requirements.txt
```
- Create a postgres database for the project
- Create a .env in the project root directory and add the following environment variables
```bash
NPM_PATH = <path to npm>
DB_NAME= <name of your database>
DB_USER= <your database username>
DB_PASS= <your database password>
DB_HOST= <your database host>
DB_PORT= <your database port no>
```
- Install redis on your machine and start the redis server
- Run the following commands to migrate the database.
```bash
python manage.py migrate
```
- Install tailwind dependencies and start tailwind using the following commands
```bash
python manage.py tailwind install
python manage.py tailwind start
```
- Open a new terminal. Start the django server using the following commands
```bash
conda activate lunchwars
python manage.py runserver
```
- Open up a new terminal. Start a celery worker using the following commands
```bash
conda activate lunchwars
celery -A LunchWars worker --pool=solo -l INFO
```
- Open another terminal. Start a celery beat using the following commands
```bash
conda activate lunchwars
celery -A LunchWars beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
```
- Open your browser and navigate to `http://localhost:8000/` to view the app


## Features
  - Users can sign up as employees or restaurant respresentative
  - Restaurant representatives can add their restaurants to the app
  - Restaurant representatives can add dishes to their restaurants
  - Restaurant representatives can participate in "Wars" to win the right to provide lunch for the office
  - To participate in a war, a restaurant representative creates a menu and adds their dishes to it
  - A menu must have at least 1 dish
  - Employees can vote for their preferred menu. They can vote for multiple menus but only once per menu
  - The leaderboard shows the current standings for today's at all times
  - Employees can view the menu for the day (winner of the previous day)
  - The same restaurant cannot be the winner of 3 consequetive days' wars
  - The system adds a new war for the next day at 12:00 AM everyday

## ER Diagram
![ER Diagram](/er.png)

