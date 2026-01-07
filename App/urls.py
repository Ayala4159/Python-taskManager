from django.urls import path, include
from App import views

urlpatterns = [
    path("", views.welcome, name="welcome"),
    path("SignIn/", views.sign_in, name="sign_in"),
    path("SignUp/", views.sign_up, name="sign_up"),
    path("CreateTeam/", views.create_team, name="create_team"),
    path("SelectTeam/", views.select_team, name="select_team"),
    path("AddTask/", views.add_task, name="add_task"),
    path("GetTasks/", views.get_tasks, name="get_tasks"),
    path("deleteTask/<int:task_id>/", views.delete_task, name="delete_task"),
    path("editTask/<int:task_id>/", views.edit_task, name="edit_task"),
    path("updateOwner/<int:task_id>/", views.update_owner, name="update_owner"),

]
