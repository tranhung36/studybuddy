from django.urls import path
from .views import (
    delete_room,
    home,
    room,
    create_room,
    update_room,
    delete_room,
    login_page,
    logout_page,
    register_page,
    delete_message,
    user_profile,
    update_profile,
    white_board
)

urlpatterns = [
    path('', home, name="home"),
    path('room/<str:pk>/', room, name="room"),
    path('create-room/', create_room, name='create-room'),
    path('update-room/<str:pk>/', update_room, name='update-room'),
    path('delete-room/<str:pk>/', delete_room, name='delete-room'),
    path('delete-message/<str:pk>/', delete_message, name='delete-message'),
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('logout/', logout_page, name='logout'),
    path('profile/<str:pk>/', user_profile, name='user-profile'),
    path('update-profile/', update_profile, name='update-profile'),
    path('white-board/<str:pk>/', white_board, name="white-board")
]
