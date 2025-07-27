import traceback

from django.shortcuts import render
import json
from TeamPlannerApp.app.users import User
from TeamPlannerApp.app.teams import Team
from TeamPlannerApp.app.project_board import ProjectBoard
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

user_obj = User()
team_obj = Team()
project_board_obj = ProjectBoard()

#  User Methods ----------------------------------------------------------------------------


@csrf_exempt
def create_user_view(request):
    if request.method == 'POST':
        try:
            data = request.body.decode('utf-8')
            response = user_obj.create_user(data)
            return JsonResponse(json.loads(response))
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Only POST methods allowed"}, status=405)


def list_users_view(request):
    if request.method == 'GET':
        try:
            response = User().list_users()
            return JsonResponse(json.loads(response), safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Only GET methods allowed"}, status=405)


def get_user_view(request, id):
    if request.method == 'GET':
        try:
            data = json.dumps({"user_id": id})
            response = User().describe_user(data)
            return JsonResponse(json.loads(response))
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Only GET methods allowed"}, status=405)


@csrf_exempt
def update_user_view(request):
    if request.method == 'POST':
        try:
            data = request.body.decode('utf-8')
            response = user_obj.update_user(data)
            return JsonResponse(json.loads(response))
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Only POST methods allowed"}, status=405)

# #  Team Methods ----------------------------------------------------------------------------


@csrf_exempt
def create_team_view(request):
    if request.method == 'POST':
        try:
            data = request.body.decode('utf-8')
            response = team_obj.create_team(data)
            return JsonResponse(json.loads(response))
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Only POST methods allowed"}, status=405)


def list_teams_view(request):
    if request.method == 'GET':
        try:
            response = Team().list_teams()
            return JsonResponse(json.loads(response), safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Only GET methods allowed"}, status=405)


def get_team_view(request, id):
    if request.method == 'GET':
        try:
            data = json.dumps({"team_id": id})
            response = Team().describe_team(data)
            return JsonResponse(json.loads(response))
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Only GET methods allowed"}, status=405)


@csrf_exempt
def update_team_view(request):
    if request.method == 'POST':
        try:
            data = request.body.decode('utf-8')
            response = team_obj.update_team(data)
            return JsonResponse(json.loads(response))
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Only POST methods allowed"}, status=405)


def get_user_teams_view(request, id):
    if request.method == 'GET':
        try:
            data = json.dumps({"user_id": id})
            response = user_obj.get_user_teams(data)
            return JsonResponse(json.loads(response))
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Only GET methods allowed"}, status=405)


@csrf_exempt
def add_users_to_team_view(request):
    if request.method == 'POST':
        try:
            data = request.body.decode('utf-8')
            response = team_obj.add_users_to_team(data)
            return JsonResponse(json.loads(response))
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Only POST methods allowed"}, status=405)


@csrf_exempt
def remove_users_from_team_view(request):
    if request.method == 'POST':
        try:
            data = request.body.decode('utf-8')
            response = team_obj.remove_users_from_team(data)
            return JsonResponse(json.loads(response))
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Only POST methods allowed"}, status=405)


def list_team_users_view(request, id):
    if request.method == 'GET':
        try:
            data = json.dumps({"team_id": id})
            response = Team().list_team_users(data)
            return JsonResponse(json.loads(response), safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Only GET methods allowed"}, status=405)


#  ProjectBoard Methods ----------------------------------------------------------------------------


@csrf_exempt
def create_board_view(request):
    if request.method == 'POST':
        try:
            data = request.body.decode('utf-8')
            response = project_board_obj.create_board(data)
            return JsonResponse(json.loads(response))
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Only POST methods allowed"}, status=405)


@csrf_exempt
def close_board_view(request):
    if request.method == 'POST':
        try:
            data = request.body.decode('utf-8')
            response = project_board_obj.close_board(data)
            return JsonResponse(json.loads(response))
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Only POST methods allowed"}, status=405)


@csrf_exempt
def add_task_view(request):
    if request.method == 'POST':
        try:
            data = request.body.decode('utf-8')
            response = project_board_obj.add_task(data)
            return JsonResponse(json.loads(response))
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Only POST methods allowed"}, status=405)


@csrf_exempt
def update_task_status_view(request):
    if request.method == 'POST':
        try:
            data = request.body.decode('utf-8')
            response = project_board_obj.update_task_status(data)
            return JsonResponse(json.loads(response))
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Only POST methods allowed"}, status=405)


def list_boards_view(request, id):
    if request.method == 'GET':
        try:
            data = json.dumps({"team_id": id})
            response = project_board_obj.list_boards(data)
            return JsonResponse(json.loads(response), safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Only GET methods allowed"}, status=405)


@csrf_exempt
def export_board_view(request):
    if request.method == 'POST':
        try:
            data = request.body.decode('utf-8')
            response = project_board_obj.export_board(data)
            return JsonResponse(json.loads(response))
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Only POST methods allowed"}, status=405)


# Extra --------------------------------------------------------------

# def get_user_view_post(request):
#     if request.method == 'POST':
#         try:
#             data = request.body.decode('utf-8')
#             response = User().describe_user(data)
#             return JsonResponse(json.loads(response))
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=400)
#     return JsonResponse({"error": "Only POST methods allowed"}, status=405)
