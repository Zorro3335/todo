
from django.urls import path, include
from . import views
from .views import ToDoAPIView



urlpatterns = [
    path('', views.home, name='home'),
    #LOGIN
    path('signup', views.singupuser, name='singupuser'),
    path('login', views.login_user, name='login_user'),
    path('logout', views.logout_user, name='logout_user'),

    # TODO
    path('current', views.current_todos, name='current_todos'),
    path('create', views.create_todo, name='create_todo'),
    path('completed_todo', views.view_completed_todo, name='completed_todo'),
    path('<int:id_todo>', views.detail_todo, name='detail_todo'),
    path('<int:id_todo>/completed', views.completed_todo, name='completed_todo_to'),
    path('<int:id_todo>/delete', views.delete_todo, name='delete_todo'),
    path('<int:id_todo>/save', views.save_todo, name='save_todo'),

    # API
    path('api/todos/', ToDoAPIView.as_view(), name='todos')

]