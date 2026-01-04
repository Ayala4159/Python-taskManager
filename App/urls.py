from django.urls import path, include
from App import views

urlpatterns = [
    path("", views.wellcome, name="wellcome"),
    path("SignIn/", views.sign_in, name="sign_in"),
    path("SignUp/", views.sign_up, name="sign_up"),
    path("CreateTeam/", views.create_team, name="create_team"),
    path("SelectTeam/", views.select_team, name="select_team"),
    path("AddTask/", views.add_task, name="add_task"),
    path("GetTasks/", views.get_tasks, name="get_tasks"),

]
