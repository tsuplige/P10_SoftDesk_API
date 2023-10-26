# from django.shortcuts import render
# from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from softdesk_app.permissions import IsAuthor

from softdesk_app.models import Project, Contributor, Issue, Comment
from softdesk_app.serializers import (ProjectListSerializer,
                                      ProjectDetailSerializer,
                                      ContributorSerializer,
                                      IssueListSerializer,
                                      IssueDetailSerializer,
                                      CommentListSerializer,
                                      CommentDetailSerializer)


class ProjectViewset(ModelViewSet):

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
        
    if action == 'destroy':
        permission_classes = [IsAuthor]
    else:
        permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(work_on__user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        # elif self.action == 'destroy':
            
        return super().get_serializer_class()

    @action(detail=False, methods=['post'])
    def create_project(self, request):
        data = request.data.copy()

        data['work_on'] = [{'user': request.user.id}]

        serializer = ProjectListSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class ContributorViewset(ModelViewSet):

    serializer_class = ContributorSerializer

    def get_queryset(self):
        return Contributor.objects.all()


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
