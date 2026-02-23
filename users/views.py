from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response

from users.constants import USER_LIST
from users.models import User
from users.serializers import UseListSerializer


# Create your views here.
class ListOfUserAPIView(generics.ListAPIView):
    serializer_class = UseListSerializer
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        self.queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(self.queryset, many=True)
        data = serializer.data
        new_data = {}
        if not data:
            new_data['count'] = 0
            new_data['next'] = None
            new_data['previous'] = None
            new_data['results'] = data
        else:
            new_data['count'] = 0
            new_data['next'] = None
            new_data['previous'] = None
            new_data['results'] = data
        return Response({"data": new_data, "message": USER_LIST}, status=status.HTTP_200_OK)