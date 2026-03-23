from django.core.cache import cache
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
        # redis_key = f"test_users_list"
        # cached_data = cache.get(redis_key)
        # if cached_data:
        #     return Response({"data": cached_data, "message": USER_LIST}, status=status.HTTP_200_OK)
        # self.queryset = self.filter_queryset(self.get_queryset())
        # serializer = self.get_serializer(self.queryset, many=True)
        # data = serializer.data
        # new_data = {}
        queryset = list(User.objects.all().values("id", "username", "email", "first_name", "last_name"))
        users_list = list(queryset)

        # ✅ 3. Build response
        new_data = {
            "count": len(users_list),
            "next": None,
            "previous": None,
            "results": users_list
        }
        # if not data:
        #     new_data['count'] = 0
        #     new_data['next'] = None
        #     new_data['previous'] = None
        #     new_data['results'] = data
        # else:
        #     new_data['count'] = 0
        #     new_data['next'] = None
        #     new_data['previous'] = None
        #     new_data['results'] = data
        # cache.set(redis_key, new_data, timeout=60 * 10)
        return Response({"data": new_data, "message": USER_LIST}, status=status.HTTP_200_OK)