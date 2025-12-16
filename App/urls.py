from django.urls import path, include
from App import views

urlpatterns = [
    path("", views.wellcome),
    path("SignIn/", views.sign_in),
    path("SignUp/", views.sign_up)
]
