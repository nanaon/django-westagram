from django.urls import path
from .views import MainView, SignUpView, LogInView

urlpatterns = [
    path('', MainView.as_view()),
    path('/sign-up', SignUpView.as_view()),
    path('/log-in', LogInView.as_view()),
]
