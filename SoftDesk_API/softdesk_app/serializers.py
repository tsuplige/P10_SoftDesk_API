from rest_framework.serializers import ModelSerializer, ValidationError

from .models import Project, Contributor, Issue, Comment


class ProjectListSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'name',
                  'time_created', 'author']

    def validate_name(self, value):
        if Project.objects.filter(name=value).exists():
            raise ValidationError('Project already exit')
        return value


class ProjectDetailSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'name', 'type',
                  'description',
                  'time_created', 'author']

    def validate_name(self, value):
        if Project.objects.filter(name=value).exists():
            raise ValidationError('Project already exit')
        return value


class ContributorSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project', 'role']


class IssueListSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'name', 'project',
                  'time_created', 'time_created', 'author']

    def validate_name(self, value):
        if Issue.objects.filter(name=value).exists():
            raise ValidationError('Project already exit')
        return value


class IssueDetailSerializer(ModelSerializer):

    project = ProjectDetailSerializer()

    class Meta:
        model = Issue
        fields = ['id', 'name', 'project',
                  'time_created', 'time_created', 'author', 'description',
                  'status', 'balise', 'priority', 'contributor']


class CommentListSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'issue', 'time_created', 'author']


class CommentDetailSerializer(ModelSerializer):

    issue = IssueDetailSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'issue', 'description',
                  'time_created', 'author']
