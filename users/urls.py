from django.urls import path 
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('', views.userCRUD, name='search-user'),
    #prueba
    path('create/', views.CreateUserView.as_view(), name='create-user'),
    path('edit/<pk>/', views.EditUserView.as_view(), name='edit-user'),
    path('delete/<pk>/', views.DeleteUserView.as_view(), name='delete-user'),
    #path('searchUser/', views.SearchUsers.as_view()),
    #auth token
    path('get-token/', views.CustomObtainAuthToken.as_view(), name='token_obtain_pair'),
]