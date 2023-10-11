from django.urls import path 
from rest_framework.authtoken.views import obtain_auth_token
from views import *

urlpatterns = [
    #SearchOneUser
    path('', userCRUD, name='search-user'),
    #CrudUser
    path('create/', CreateUserView.as_view(), name='create-user'),
    path('update/<pk>/', UpdateUserView.as_view(), name='edit-user'),
    path('delete/<pk>/', DeleteUserView.as_view(), name='delete-user'),
    #auth token
    path('get-token/', CustomObtainAuthToken.as_view(), name='token_obtain_pair'),
]