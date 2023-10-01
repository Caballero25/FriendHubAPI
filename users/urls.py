from django.urls import path 
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('', views.userCRUD, name='user-view'),
    path('get-token/', obtain_auth_token, name='token_obtain_pair'),
]