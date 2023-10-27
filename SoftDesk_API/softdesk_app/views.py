# from django.shortcuts import render
# from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from softdesk_app.permissions import IsAuthor, IsContributor
from django.conf import settings
from authentication.models import User

from softdesk_app.models import Project, Contributor, Issue, Comment
from softdesk_app.serializers import (ProjectListSerializer,
                                      ProjectDetailSerializer,
                                      ContributorSerializer,
                                      IssueListSerializer,
                                      IssueDetailSerializer,
                                      CommentListSerializer,
                                      CommentDetailSerializer)


class ProjectViewset(ReadOnlyModelViewSet):

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(work_on__user=self.request.user)

    @action(detail=True, permission_classes=[IsContributor])
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class

        return super().get_serializer_class()

    @action(detail=False, methods=['post'])
    def create_project(self, request):

        data = request.data.copy()
        data['author'] = request.user.id
        serializer = ProjectDetailSerializer(data=data)

        if serializer.is_valid():

            project = serializer.save()
            contributor_data = {'user': request.user.id,
                                'project': project.id,
                                'role': "Auteur"}
            contributor_serializer = ContributorSerializer(
                data=contributor_data)

            if contributor_serializer.is_valid():
                contributor_serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            else:
                project.delete()
                return Response(contributor_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'],
            permission_classes=[IsAuthor])
    def delete_project(self, request, pk=None):

        if Project.objects.get(pk=pk):
            project = Project.objects.get(pk=pk)
        else:
            return Response({'message': 'Project not found'},
                            status=status.HTTP_404_NOT_FOUND)

        if project.author == request.user:
            project.delete()
            return Response({'message': 'Project deleted successfully'},
                            status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': 'You do not have permission to delete this project'},
                            status=status.HTTP_403_FORBIDDEN)


class ContributorViewset(ReadOnlyModelViewSet):

    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        return Contributor.objects.filter(project_id=project_id)

    @action(detail=False, methods=['post', 'delete'])
    def add_or_delete(self, request, project_id):
        project = Project.objects.get(pk=project_id)
        username = request.data.get('username')

        user = User.objects.get(username=username)

        contributor_data = {
            'user': user.id,
            'project': project.id
        }

        serializer = ContributorSerializer(data=contributor_data)
        if request.method == 'POST':
            if project.author == request.user:
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data,
                                    status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors,
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'You do not have'
                                 'permission to delete this project'},
                                status=status.HTTP_403_FORBIDDEN)
        elif request.method == 'DELETE':
            if project.author == request.user:
                contributor = Contributor.objects.get(user=user,
                                                      project=project)
                contributor.delete()
                return Response({'message': 'Project deleted successfully'},
                                status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': 'You do not have'
                                 ' permission to delete this project'},
                                status=status.HTTP_403_FORBIDDEN)


class IssueViewset(ModelViewSet):

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        if Contributor.objects.get(project=project_id,
                                   user=self.request.user).exists():
            return Issue.objects.filter(project_id=project_id)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()

    @action(detail=True, methods=['post'])
    def in_progress(self, request, pk):
        self.get_object().in_progress()
        return Response()

    @action(detail=True, methods=['post'])
    def finished(self, request, pk):
        self.get_object().finished()
        return Response()


class CommentViewset(ModelViewSet):

    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer

    def get_queryset(self):
        return Comment.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()


class AdminProjectViewset(ModelViewSet):
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    def get_queryset(self):
        return Project.objects.all()
