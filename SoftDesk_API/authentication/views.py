# from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from .models import User
from .serializers import (UserSerializer,
                          UserListSerializer,
                          UserDetailSerializer,
                          UserAnonymeDetailSerializer)


class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        data = request.data
        serializer = self.get_serializer(data=data)
        birthdate = data.get('birthdate')
        if birthdate:
            from datetime import date
            today = date.today()
            age = today.year - birthdate.year - (
                (today.month, today.day) < (birthdate.month, birthdate.day))

            if age < 15:
                data['can_data_be_shared'] = False

        if serializer.is_valid():
            user = User.objects.create_user(username=data['username'],
                                            password=data['password'],
                                            birthdate=data['birthdate'],
                                            can_data_be_shared=data['can_data_be_shared'],
                                            can_be_contacted=data['can_be_contacted'],
                                            first_name=data['first_name'],
                                            last_name=data['last_name'])
            return Response({"user_id": user.id,
                             "message": "Inscription réussie"},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request):
        pass


class UserViewSet(ReadOnlyModelViewSet):

    serializer_class = UserListSerializer
    detail_serializer_class = UserDetailSerializer
    anonyme_detail_serializer_class = UserAnonymeDetailSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(can_data_be_shared=True)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            user = self.get_object()
            if user.can_data_be_shared is None:
                return self.anonyme_detail_serializer_class
            elif user.can_data_be_shared:
                return self.detail_serializer_class
            else:
                return self.anonyme_detail_serializer_class
        return super().get_serializer_class()

    @action(detail=False, methods=['put'])
    def update_user(self, request):
        user_to_update = self.request.user
        try:
            user = User.objects.get(id=user_to_update.id)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Données uti'
                                 'lisateur mises à jour'},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'message': 'User not found'},
                            status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return Response({'message': 'Permission denied'},
                            status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['delete'])
    def delete_user(self, request):
        user_to_delete = self.request.user
        print(user_to_delete)
        try:
            user = User.objects.get(id=user_to_delete.id)
            user.delete()
            return Response({'message': 'Compte et information'
                             'utilisateur supprimés'},
                            status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'message': 'User not found'},
                            status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return Response({'message': 'Permission denied'},
                            status=status.HTTP_403_FORBIDDEN)
