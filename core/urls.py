from django.urls import path 
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('book/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
    path('register', views.register_view, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
]