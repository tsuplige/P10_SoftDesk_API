# from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import User
from .serializers import UserSerializer


class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        data = request.data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            user = User.objects.create_user(username=data['username'],
                                            password=data['password'],
                                            birthdate=data['birthdate'],
                                            can_data_be_shared=data['can_data_be_shared'],
                                            can_be_contacted=data['can_be_contacted'])
            return Response({"user_id": user.id,
                             "message": "Inscription réussie"},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
