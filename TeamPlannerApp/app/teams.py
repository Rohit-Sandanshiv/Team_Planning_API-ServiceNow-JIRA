import json
import os
import uuid
from lib.team_base import TeamBase
from datetime import datetime


class Team(TeamBase):
    def __init__(self):

        self.db_teams_path = "lib/db/teams.json"
        self.db_users_path = "lib/db/users.json"

        if not os.path.exists(self.db_teams_path):
            with open(self.db_teams_path, 'w') as f:
                json.dump([], f)

        if not os.path.exists(self.db_users_path):
            with open(self.db_users_path, 'w') as f:
                json.dump([], f)

    def create_team(self, request: str) -> str:
        data = json.loads(request)
        name = data.get("name", '')
        description = data.get("description", '')
        admin = data.get("admin", '')

        if len(name) > 64 or len(description) > 128:
            raise ValueError("Name or description too Long...")

        with open(self.db_teams_path, 'r+') as f:
            teams = json.load(f)
            if any(u['name'] == name for u in teams):
                raise ValueError("TeamName must be unique")

            team_id = str(uuid.uuid4())
            creation_time = datetime.now().isoformat()
            team = {"team_id": team_id, "name": name, "description": description, "admin": admin,
                    "creation_time": creation_time, "users": [admin]}
            teams.append(team)
            f.seek(0)
            json.dump(teams, f, indent=4)
            f.truncate()
        return json.dumps({"id": team_id})

    def list_teams(self) -> str:
        with open(self.db_teams_path, 'r') as f:
            teams = json.load(f)
            output = [{"name": d.get("name"), "description": d.get("description"), "admin": d.get("admin"),
                       "creation_time": d.get("creation_time")} for d in teams]

            if not output:
                raise ValueError("No Teams yet")

            return json.dumps(output)

    def describe_team(self, request: str) -> str:
        data = json.loads(request)
        team_id = data.get("team_id")
        with open(self.db_teams_path, 'r') as f:
            teams = json.load(f)
        output = dict()
        for team in teams:
            if team.get("team_id") == team_id:
                output["name"] = team.get("name")
                output["description"] = team.get("description")
                output["admin"] = team.get("admin")
                output["creation_time"] = team.get("creation_time")

        if not output:
            raise ValueError("Team Not found")

        return json.dumps(output)

    def update_team(self, request: str) -> str:
        data = json.loads(request)
        update_id = data.get("id", '')
        update_data = data.get("team", {})

        if not update_id or not update_data:
            raise ValueError("Invalid request: Missing required fields.")

        update_flag = False

        with open(self.db_teams_path, 'r+') as f:
            teams = json.load(f)
            team_names = [d.get("name") for d in teams]
            for team in teams:
                if team.get("team_id") == update_id:

                    if len(update_data.get("name")) > 64:
                        raise ValueError("Team_name limit reached. Max permissible, 64")

                    if len(update_data.get("description")) > 128:
                        raise ValueError("description limit reached. Max permissible, 128")

                    if team.get("name") != update_data.get("name"):
                        if update_data.get("name") in team_names:
                            raise ValueError("Team with this name, already exists! Try other name")
                        else:
                            if update_data.get("name"):
                                team["name"] = update_data.get("name")
                    if update_data.get("description"):
                        team["description"] = update_data.get("description")
                    if update_data.get("admin"):
                        team["admin"] = update_data.get("admin")
                    update_flag = True

            f.seek(0)
            json.dump(teams, f, indent=4)
            f.truncate()

        if not update_flag:
            raise ValueError("Team ID not found")

        return json.dumps({"Message": "Updated Successfully"})

    def add_users_to_team(self, request: str):
        data = json.loads(request)
        team_id = data.get("id")
        users = data.get("users")
        if len(users) > 50:
            raise ValueError("max number of users that can be added at a time to the team is 50")

        with open(self.db_users_path, 'r') as f:
            users_data = json.load(f)

        legit_users = []
        for user_id in users:
            users_present = False
            if any(u['user_id'] == user_id for u in users_data):
                users_present = True
                legit_users.append(user_id)
            if not users_present:
                print(f"invalid userid: {user_id}")

        update_flag = False
        users = legit_users

        with open(self.db_teams_path, 'r+') as f:
            teams = json.load(f)
            for team in teams:
                if team.get("team_id") == team_id:
                    team['users'].extend(users)
                    update_flag = True
                    break
            if not update_flag:
                raise ValueError("Team ID not found")
            f.seek(0)
            json.dump(teams, f, indent=4)
            f.truncate()

        return json.dumps({"Message": "Updated Successfully"})

    def remove_users_from_team(self, request: str):
        data = json.loads(request)
        team_id = data.get("id")
        users = data.get("users")
        if len(users) > 50:
            raise ValueError("max number of users that can be removed at a time from the team is 50")
        update_flag = False

        with open(self.db_teams_path, 'r+') as f:
            teams = json.load(f)
            for team in teams:
                if team.get("team_id") == team_id:
                    for user in users:
                        if user in team['users']:
                            team['users'].remove(user)
                    update_flag = True
                    break
            if not update_flag:
                raise ValueError("Team ID not found")
            f.seek(0)
            json.dump(teams, f, indent=4)
            f.truncate()

        return json.dumps({"Message": "Updated Successfully"})

    def list_team_users(self, request: str):
        data = json.loads(request)
        team_id = data.get("team_id")
        users = []

        with open(self.db_teams_path, 'r') as f:
            teams = json.load(f)

        for team in teams:
            if team.get("team_id") == team_id:
                users = team.get('users')
                break

        if not users:
            raise ValueError("TeamId not found")

        with open(self.db_users_path, 'r') as f:
            users_data = json.load(f)

        output = []
        for d in users_data:
            if d.get("user_id") in users:
                output.append({"name": d.get("name"), "display_name": d.get("display_name"),
                               "creation_time": d.get("creation_time")})

        return json.dumps(output)
