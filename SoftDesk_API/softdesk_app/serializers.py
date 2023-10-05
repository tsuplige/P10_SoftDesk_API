from rest_framework.serializers import ModelSerializer

from .models import Project, Contributor, Issue, Comment


class ProjectSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'name', 'type',
                  'time_created', 'author']


class ContributorSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project']


class IssueSerializer(ModelSerializer):

    project = ProjectSerializer()

    class Meta:
        model = Issue
        fields = ['id', 'name', 'project',
                  'time_created', 'time_created', 'author']


class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'issue', 'time_created', 'author']
