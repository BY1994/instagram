from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('logout/', views.logout, name="logout"),
    path('login/', views.login, name="login"),
    path('delete/', views.delete, name="delete"),
    path('<int:user_id>/follow/', views.follow, name="follow"),
]