# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from softdesk_app.models import Project, Contributor, Issue, Comment
from softdesk_app.serializers import (ProjectSerializer, ContributorSerializer,
                                      IssueSerializer, CommentSerializer)


class ProjectViewset(ModelViewSet):

    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.all()


class ContributorViewset(ModelViewSet):

    serializer_class = ContributorSerializer

    def get_queryset(self):
        return Contributor.objects.all()


class IssueViewset(ModelViewSet):

    serializer_class = IssueSerializer

    def get_queryset(self):
        return Issue.objects.all()


class CommentViewset(ModelViewSet):

    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.all()
