from django.urls import path
from users.views import ListOfUserAPIView

urlpatterns  = [
    path('users-list/', ListOfUserAPIView.as_view(), name='users_list'),
]