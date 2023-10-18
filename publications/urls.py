from django.urls import path 
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('info/<pk>/', views.PublicationRetrieveView.as_view(), name='info-publication'),
    path('create/', views.CreatePublicationView.as_view(), name='create-publication'),
    path('update/<pk>/',views.UpdatePublicationView.as_view(), name='update-publication'),
    path('delete/<pk>/', views.DeletePublicationView.as_view(), name='delete-publication'),

    path('entertainment/', views.EntertainmentPublicationListView.as_view(), name='entertainment-publications'),
    path('innovation/', views.DevelopmentPublicationListView.as_view(), name='innovation-publications'),
] 