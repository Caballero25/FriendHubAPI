from django.urls import path 
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    #SearchOneUser
    path('search/', views.userCRUD, name='search-user'),
    #CrudUser
    path('create/', views.CreateUserView.as_view(), name='create-user'),
    path('update/<pk>/', views.UpdateUserView.as_view(), name='edit-user'),
    path('delete/<pk>/', views.DeleteUserView.as_view(), name='delete-user'),
    #auth token
    path('get-token/', views.CustomObtainAuthToken.as_view(), name='token_obtain_pair'),
]