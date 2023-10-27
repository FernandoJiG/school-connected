from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('roomDif/<str:pk>', views.room, name="room"),#utilizamos las flechas para determinar que recibiremos un parametro dinamico como las clases genericas
    path('profile/<str:pk>', views.userProfile, name="user-profile"),

    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>', views.deleteMessage, name="delete-message"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),
]
