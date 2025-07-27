import json
import uuid
import os
from datetime import datetime
from lib.project_board_base import ProjectBoardBase


class ProjectBoard(ProjectBoardBase):
    def __init__(self):
        self.db_users_path = "lib/db/users.json"
        self.db_team_path = "lib/db/teams.json"
        self.db_board_path = "lib/db/projectboard.json"
        self.out_folder = "lib/out"

        if not os.path.exists(self.db_users_path):
            with open(self.db_users_path, 'w') as f:
                json.dump([], f)

        if not os.path.exists(self.db_team_path):
            with open(self.db_team_path, 'w') as f:
                json.dump([], f)

        if not os.path.exists(self.db_board_path):
            with open(self.db_board_path, 'w') as f:
                json.dump([], f)

    def create_board(self, request: str):
        data = json.loads(request)
        name = data.get("name", '')
        description = data.get("description", '')
        team_id = data.get("team_id", '')

        if len(name) > 64 or len(description) > 128:
            raise ValueError("Name or description too Long...")

        with open(self.db_team_path, 'r') as f:
            teams = json.load(f)

        if not any(u['team_id'] == team_id for u in teams):
            raise ValueError("Team doesn't exist!. Try different team_id")

        with open(self.db_board_path, 'r+') as f:
            boards = json.load(f)
            if any(u['name'] == name for u in boards):
                raise ValueError("Project Board Name must be unique")

            board_id = str(uuid.uuid4())
            creation_time = datetime.now().isoformat()

            board = {"board_id": board_id, "name": name, "description": description, "team_id": team_id,
                     "creation_time": creation_time, "status": "OPEN", "end_time": None, "task": []}

            boards.append(board)
            f.seek(0)
            json.dump(boards, f, indent=4)
            f.truncate()
        return json.dumps({"id": board_id})

    def close_board(self, request: str) -> str:
        data = json.loads(request)
        board_id = data.get("id")
        board_present = False
        with open(self.db_board_path, 'r+') as f:
            boards = json.load(f)

            for board in boards:
                if board.get('board_id') == board_id:
                    board_present = True
                    if not board.get("task"):
                        board['status'] = 'CLOSE'
                        board['end_time'] = datetime.now().isoformat()
                        break
                    else:
                        flag = True
                        for task in board.get('task'):
                            if task.get('status') != 'COMPLETE':
                                flag = False
                                break
                        if flag:
                            board['status'] = 'CLOSE'
                            board['end_time'] = datetime.now().isoformat()
                            break
                        else:
                            raise ValueError("some tasks are incomplete, can't close the board")
            if not board_present:
                raise ValueError("No Board with this id is present")
            f.seek(0)
            json.dump(boards, f, indent=4)
            f.truncate()
        return json.dumps({"message": "Success"})

    def add_task(self, request: str) -> str:
        data = json.loads(request)
        title = data.get("title", '')
        description = data.get("description", '')
        user_id = data.get("user_id", '')
        board_id = data.get('board_id', '')
        task_id = str(uuid.uuid4())
        creation_time = datetime.now().isoformat()
        board_present = False

        if len(title) > 64 or len(description) > 128:
            raise ValueError("Title or description too Long...")

        with open(self.db_users_path, 'r') as f:
            users = json.load(f)

        if not any(u['user_id'] == user_id for u in users):
            raise ValueError("User doesn't exist!. Try correct user")

        with open(self.db_board_path, 'r+') as f:
            boards = json.load(f)

            for board in boards:
                if board.get('board_id') == board_id:
                    board_present = True
                    if board.get('status') == 'CLOSE':
                        raise ValueError("Board is already closed, can't add tasks")

                    tasks = board.get("task")
                    tasks_titles = [task.get('title') for task in tasks]
                    if title in tasks_titles:
                        raise ValueError("Task title must be unique for a board")

                    task = {"task_id": task_id, "title": title, "description": description, "user_id": user_id,
                            "board_id": board_id, "creation_time": creation_time, "status": "OPEN"}
                    board['task'].append(task)

            if not board_present:
                raise ValueError("No Board with this id is present")
            f.seek(0)
            json.dump(boards, f, indent=4)
            f.truncate()
            return json.dumps({"message": "Success"})

    def update_task_status(self, request: str):
        data = json.loads(request)
        task_id = data.get("id")
        status = data.get('status')
        task_present = False

        with open(self.db_board_path, 'r+') as f:
            boards = json.load(f)

            for board in boards:
                tasks = board.get("task")
                for task in tasks:
                    if task.get('task_id') == task_id:
                        task_present = True
                        task['status'] = status

            if not task_present:
                raise ValueError("No task with this id is present")
            f.seek(0)
            json.dump(boards, f, indent=4)
            f.truncate()
            return json.dumps({"message": "Success"})

    def list_boards(self, request: str) -> str:
        data = json.loads(request)
        team_id = data.get("team_id")

        with open(self.db_board_path, 'r+') as f:
            boards = json.load(f)

        if not boards:
            raise ValueError("Empty board")
        output = []
        for board in boards:
            if board.get("team_id") == team_id and board.get("status") == 'OPEN':
                output.append({"id": board.get("board_id"), "name": board.get("name")})

        if not output:
            raise ValueError("Empty board")

        return json.dumps(output)

    def export_board(self, request: str) -> str:
        data = json.loads(request)
        board_id = data.get('id')

        with open(self.db_board_path, 'r') as f:
            boards = json.load(f)

        output_board = None
        for board in boards:
            if board.get("board_id") == board_id:
                output_board = board

        if not output_board:
            raise ValueError("Please try correct Board ID")

        team_name = ''
        user_name = ''
        with open(self.db_team_path, 'r') as f:
            teams = json.load(f)

        for team in teams:
            if team.get("team_id") == output_board.get("team_id"):
                team_name = team.get("name")

        # with open(self.db_users_path, 'r') as f:
        #     users = json.load(f)
        #
        # for user in users:
        #     if user.get("user_id") == output_board.get("team_id"):
        #         user_name = team.get("name")

        lines = [
            f"📋 Project Board : {output_board['name']}",
            f"📝 Description   : {output_board['description']}",
            f"👥 Team ID       : {team_name} ({output_board['team_id']})",
            f"📅 Created On    : {output_board['creation_time']}",
            f"📌 Status        : {output_board['status']}"
        ]

        if output_board.get("end_time"):
            lines.append(f"✅ Closed On     : {output_board['end_time']}")
        lines.append("\n📌 Tasks :")
        lines.append("-" * 75)

        for task in output_board.get("task", []):
            lines.extend([
                f"🔹 Task Title   : {task['title']}",
                f"  📄 Description  : {task['description']}",
                f"  👤 Assigned To  : {task['user_id']}",
                f"  🕒 Created On   : {task['creation_time']}",
                f"  📌 Status       : {task['status']}",
                "-" * 75
            ])

        file_name = f"{board_id}_details_{datetime.now().isoformat()}_export.txt"
        file_name = file_name.replace(":", '')
        output_path = os.path.join(self.out_folder, file_name)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

        return json.dumps({"outfile": output_path})
