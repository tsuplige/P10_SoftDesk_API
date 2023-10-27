# from django.shortcuts import render
# from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from softdesk_app.permissions import IsAuthor, IsContributor

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


class ContributorViewset(ModelViewSet):

    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_id = self.request.query_params.get('project_id')
        print(project_id)
        return Contributor.objects.all()

    def delete(self, request):
        return super().delete(request, *args, **kwargs)

    @action(detail=True, permission_classes=[IsAuthor])
    def add(self, request):

        data = request.data
        serializer = ContributorSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class IssueViewset(ModelViewSet):

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
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
