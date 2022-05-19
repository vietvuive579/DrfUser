from django.urls import path
from knox import views as knox_views
from . import views

urlpatterns = [
    path('user/', views.get_user),
    path('login/', views.login),
    path('register/', views.register),
    path('update/', views.update),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout')
]