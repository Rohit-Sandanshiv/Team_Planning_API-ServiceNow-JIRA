# 🎉 Event Management API
A Django-based RESTful API for managing users, teams and project boards.

## ⚙️Features
### 👤 Users:   
Users are the individuals who interact with the system. Each user has:   

A unique ID    
A username and display name   
A creation timestamp   
Users can belong to one or more teams and can be assigned tasks on project boards. The system ensures that usernames are unique and display names are within a character limit.   

### 👥 Teams:   
Teams are groups of users collaborating on projects. Each team includes:   

A unique team ID   
A name and description   
An admin user who manages the team   
A list of users who are members of the team   
Teams are essential for organizing users and associating them with project boards. The system supports adding and removing users from teams and updating team details.   

### 📋 Project Boards:   
Project boards are collaborative spaces where teams manage their tasks. Each board includes:   

A unique board ID   
A name, description, and associated team ID   
A status (OPEN or CLOSE)   
A list of tasks, each with its own metadata   
Timestamps for creation and closure   
Boards can only be closed when all tasks are marked as complete. Tasks are assigned to users and tracked by status, title, and creation time.   

---

## 📁 Project Structure
```
Factwise-Project/
│
├── TeamPlannerProject/
│   ├── lib/
│   │   ├── db/
│   │   │   ├── projectboard.json
│   │   │   ├── teams.json
│   │   │   ├── users.json
│   │   │   └── out/
│   │   │       └── <generated_output_file>
│   │   ├── __init__.py
│   │   ├── ProblemStatement.md
│   │   ├── project_board_base.py
│   │   ├── README.md
│   │   ├── requirements.txt
│   │   ├── team_base.py
│   │   └── user_base.py
│   │
│   ├── TeamPlannerApp/
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── project_board.py
│   │   │   ├── teams.py
│   │   │   └── users.py
│   │   │
│   │   ├── migrations/
│   │   │   └── __init__.py
│   │   │
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── TeamPlannerProject/
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   │ 
│   ├── test/
│   │   ├── __init__.py
│   │   ├── .pytest_cache
│   │   ├── test_file.py
│   │   
│   ├── db.sqlite3
│   ├── manage.py
│   ├── Readme.md
│   └── requirements.txt
│
└── venv/               # Virtual environment
```

---
## 🚀 Getting Started
### Prerequisites
- Python 3.8+
- djangp
- pytest
- json (or your preferred DB)

## Installation & Setup
### Prerequisites
- Python 3.7+
- `pip` (Python package manager)

### Steps
1. Clone the repository:
   ```sh
   git clone `https://github.com/Rohit-Sandanshiv/Factwise_python.git`
   cd Factwise_python
   ```
2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Mac/Linux
   venv\Scripts\activate  # On Windows
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run the Flask app:
   ```sh
   python app.py
   ```
   The API will be available at `http://127.0.0.1:8000/`

---

## API Endpoints
- tested on windows cmd 
```text

---------------------------------------  User Methods  -------------------------------------------------------

curl -v -H "Content-Type: application/json" --request POST --data "{\"name\": \"Rohit\", \"display_name\": \"voldemort\"}" http://127.0.0.1:8000/create_user/

curl -v -H "Content-Type: application/json" --request GET http://127.0.0.1:8000/list_users/

curl -v -H "Content-Type: application/json" --request GET http://127.0.0.1:8000/get_users/f2e022ff-e365-479b-9738-61f5f6a94be1/

curl -v -H "Content-Type: application/json" --request POST --data "{\"id\": \"f2e022ff-e365-479b-9738-61f5f6a94be1\", \"user\":{\"name\": \"Rohit\", \"display_name\": \"Voldemort_updated\"}}" http://127.0.0.1:8000/update_user/

curl -v -H "Content-Type: application/json" --request GET http://127.0.0.1:8000/get_user_teams/12345/

--------------------------------------- Team Methods -------------------------------------------------------

curl -v -H "Content-Type: application/json" --request POST --data "{\"name\": \"Rohit_team\", \"description\": \"Smart Team\", \"admin\": \"f2e022ff-e365-479b-9738-61f5f6a94be1\"}" http://127.0.0.1:8000/create_team/

curl -v -H "Content-Type: application/json" --request GET http://127.0.0.1:8000/list_teams/

curl -v -H "Content-Type: application/json" --request GET http://127.0.0.1:8000/get_teams/e013577e-d731-45ed-a7d2-dd2c9bcefc7e/

curl -v -H "Content-Type: application/json" --request POST --data "{\"id\": \"e013577e-d731-45ed-a7d2-dd2c9bcefc7e\", \"team\":{\"name\": \"Rohit_team_updated\", \"description\": \"smart team updated\", \"admin\": \"e013577e-d731-45ed-a7d2-dd2c9bcefc7e\"}}" http://127.0.0.1:8000/update_team/

curl -v -H "Content-Type: application/json" --request POST --data "{\"users\": [\"user1\", \"user2\"], \"id\": \"e013577e-d731-45ed-a7d2-dd2c9bcefc7e\"}" http://127.0.0.1:8000/add_users_to_teams/

curl -v -H "Content-Type: application/json" --request POST --data "{\"users\": [\"user1\", \"user2\"], \"id\": \"e013577e-d731-45ed-a7d2-dd2c9bcefc7e\"}" http://127.0.0.1:8000/remove_users_from_team/

curl -v -H "Content-Type: application/json" --request GET http://127.0.0.1:8000/list_team_users/e013577e-d731-45ed-a7d2-dd2c9bcefc7e/

-------------------------------------  Project Board Methods ------------------------------------------------

curl -v -H "Content-Type: application/json" --request POST --data "{\"name\": \"Rohit_board\", \"description\": \"Smart board\", \"team_id\": \"e013577e-d731-45ed-a7d2-dd2c9bcefc7e\"}" http://127.0.0.1:8000/create_board/

curl -v -H "Content-Type: application/json" --request POST --data "{\"id\": \"d5fb992b-e97f-4531-a258-11a9d3a56baf\"}" http://127.0.0.1:8000/close_board/

curl -v -H "Content-Type: application/json" --request POST --data "{\"title\": \"Rohit_task\", \"description\": \"contact Type\", \"board_id\": \"d5fb992b-e97f-4531-a258-11a9d3a56baf\", \"user_id\": \"f2e022ff-e365-479b-9738-61f5f6a94be1\"}" http://127.0.0.1:8000/add_task/

curl -v -H "Content-Type: application/json" --request POST --data "{\"status\": \"COMPLETE\", \"id\": \"b9152ce0-e25e-453a-8c0c-365140fb784d\"}" http://127.0.0.1:8000/update_task_status/

curl -v -H "Content-Type: application/json" --request GET http://127.0.0.1:8000/list_boards/e013577e-d731-45ed-a7d2-dd2c9bcefc7e/

curl -v -H "Content-Type: application/json" --request POST --data "{\"id\": \"d5fb992b-e97f-4531-a258-11a9d3a56baf\"}" http://127.0.0.1:8000/export_board/
```
## 🧪 Testing
This project uses `pytest` for testing core functionalities.

To run tests:
```bash
pytest -v
```

---
## Bonus
   - Can be improved with adding security to database or migrating it to some other secure databases like sql, postgresql

## Contribution
Feel free to contribute by submitting issues or pull requests.

---

## Author
**Rohit Sandanshiv**

---

## License
MIT License