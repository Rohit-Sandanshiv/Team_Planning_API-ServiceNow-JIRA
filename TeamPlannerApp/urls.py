from django.urls import path
from .views import create_user_view, list_users_view, get_user_view, update_user_view, create_team_view, \
    list_teams_view, get_team_view, update_team_view, get_user_teams_view, add_users_to_team_view, \
    remove_users_from_team_view, list_team_users_view, create_board_view, close_board_view, add_task_view, \
    update_task_status_view, list_boards_view, export_board_view

urlpatterns = [
    path('create_user/', create_user_view),
    path('list_users/', list_users_view),
    path('get_users/<str:id>/', get_user_view),
    path('update_user/', update_user_view),
    path('create_team/', create_team_view),
    path('list_teams/', list_teams_view),
    path('get_teams/<str:id>/', get_team_view),
    path('update_team/', update_team_view),
    path('get_user_teams/<str:id>/', get_user_teams_view),
    path('add_users_to_teams/', add_users_to_team_view),
    path('remove_users_from_team/', remove_users_from_team_view),
    path('list_team_users/<str:id>/', list_team_users_view),
    path('create_board/', create_board_view),
    path('close_board/', close_board_view),
    path('add_task/', add_task_view),
    path('update_task_status/', update_task_status_view),
    path('list_boards/<str:id>/', list_boards_view),
    path('export_board/', export_board_view),
]