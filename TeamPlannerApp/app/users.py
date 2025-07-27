import json
import os
import uuid
from lib.user_base import UserBase
from datetime import datetime


class User(UserBase):
    def __init__(self):
        self.db_users_path = "lib/db/users.json"
        self.db_team_path = "lib/db/teams.json"

        if not os.path.exists(self.db_users_path):
            with open(self.db_users_path, 'w') as f:
                json.dump([], f)

        if not os.path.exists(self.db_team_path):
            with open(self.db_team_path, 'w') as f:
                json.dump([], f)

    def create_user(self, request: str) -> str:
        data = json.loads(request)
        name = data["name"]
        display_name = data["display_name"]

        if len(name) > 64 or len(display_name) > 64:
            raise ValueError("Name or Display Name too Long...")

        with open(self.db_users_path, 'r+') as f:
            users = json.load(f)
            if any(u['name'] == name for u in users):
                raise ValueError("Username must be unique")

            user_id = str(uuid.uuid4())
            creation_time = datetime.now().isoformat()
            user = {"user_id": user_id, "name": name, "display_name": display_name, "creation_time": creation_time}
            users.append(user)
            f.seek(0)
            json.dump(users, f, indent=4)
            f.truncate()
        return json.dumps({"id": user_id})

    def list_users(self) -> str:
        with open(self.db_users_path, 'r') as f:
            users = json.load(f)
            output = [{"name": d.get("name"), "display_name": d.get("display_name"),
                       "creation_time": d.get("creation_time")} for d in users]

            if not output:
                raise ValueError("No users yet")

            return json.dumps(output)

    def describe_user(self, request: str) -> str:
        data = json.loads(request)
        user_id = data.get("user_id")
        with open(self.db_users_path, 'r') as f:
            users = json.load(f)
        output = dict()
        for user in users:
            if user.get("user_id") == user_id:
                output["name"] = user.get("name")
                output["display_name"] = user.get("display_name")
                output["creation_time"] = user.get("creation_time")

        if not output:
            raise ValueError("user Not found")

        return json.dumps(output)

    def update_user(self, request: str) -> str:
        data = json.loads(request)
        update_id = data.get("id")
        update_data = data.get("user", {})

        if not update_id or "display_name" not in update_data or "name" not in update_data:
            raise ValueError("Invalid request: Missing required fields.")

        update_flag = False

        with open(self.db_users_path, 'r+') as f:
            users = json.load(f)
            for user in users:
                if user.get("user_id") == update_id:
                    if user.get("name") != update_data.get("name"):
                        raise ValueError("Warning! user name cannot be updated")
                    if len(update_data.get("display_name")) > 128:
                        raise ValueError("Display Name limit reached. Max permissible, 128")
                    user["display_name"] = update_data.get("display_name")
                    update_flag = True

            f.seek(0)
            json.dump(users, f, indent=4)
            f.truncate()

        if not update_flag:
            raise ValueError("User ID not found.")

        return json.dumps({"Message": "Updated Successfully"})

    def get_user_teams(self, request: str) -> str:
        data = json.loads(request)
        user_id = data.get("user_id")
        with open(self.db_team_path, 'r') as f:
            teams = json.load(f)

        output = dict()
        for team in teams:
            if user_id in team.get('users'):
                output["name"] = team.get("name")
                output["description"] = team.get("description")
                output["creation_time"] = team.get("creation_time")

        if not output:
            raise ValueError("Team Not found")

        return json.dumps(output)









