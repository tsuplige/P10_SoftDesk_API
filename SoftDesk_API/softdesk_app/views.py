
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from softdesk_app.permissions import IsAuthor, IsContributor
from django.shortcuts import get_object_or_404

from authentication.models import User
from rest_framework.exceptions import PermissionDenied

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

    @action(detail=True, methods=['put'])
    def update_project(self, request, pk=None):
        project = self.get_object()

        if project.author == request.user:
            serializer = ProjectDetailSerializer(project,
                                                 data=request.data,
                                                 partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            raise PermissionDenied("You don't have permission "
                                   "to update this project.")

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
            return Response({'message': 'You do not have '
                             'permission to delete this project'},
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
        user = self.request.user

        is_contributor = Contributor.objects.filter(
            user=user,
            project__id=project_id
        ).exists()

        if is_contributor:
            return Issue.objects.filter(project__id=project_id)
        else:
            raise PermissionDenied("You don't have permission to"
                                   " access issues in this project.")

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()

    @action(detail=False, methods=['post'])
    def create_issue(self, request, project_id):
        project = Project.objects.get(pk=project_id)
        user = self.request.user
        contributor_name = request.data.get('contributor')
        contributor = User.objects.get(username=contributor_name)

        is_contributor = Contributor.objects.filter(
            user=user,
            project=project
        ).exists()

        if not is_contributor:
            raise PermissionDenied("You don't have permission"
                                   " to create an issue in this project.")

        data = request.data.copy()
        print(data)
        data['project'] = project.id
        data['author'] = user.id
        data['contributor'] = contributor.id

        serializer = IssueDetailSerializer(data=data)

        if serializer.is_valid():
            issue = serializer.save()
            print(issue)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    def update_issue(self, request, project_id, pk=None):
        issue = self.get_object()

        if issue.author == request.user:
            serializer = IssueDetailSerializer(issue,
                                               data=request.data,
                                               partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            raise PermissionDenied("You don't have permission"
                                   " to update this issue.")

    @action(detail=True, methods=['delete'],
            permission_classes=[IsAuthenticated])
    def delete_issue(self, request, project_id, pk=None):

        project = Project.objects.get(pk=project_id)
        user = self.request.user

        is_contributor = Contributor.objects.filter(
            user=user,
            project=project
        ).exists()

        if not is_contributor:
            raise PermissionDenied("You don't have permission"
                                   " to delete an issue in this project.")
        try:
            issue = get_object_or_404(Issue, pk=pk)

            if issue.project.id != project_id:
                return Response({'message': 'Issue does not'
                                 ' belong to this project'},
                                status=status.HTTP_400_BAD_REQUEST)

            if issue.author == request.user:
                issue.delete()
                return Response({'message': 'Issue deleted successfully.'},
                                status=status.HTTP_204_NO_CONTENT)
            else:
                raise PermissionDenied("You don't have permission"
                                       " to delete this issue.")
        except Issue.DoesNotExist:
            return Response({'message': 'Issue not found'},
                            status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def in_progress(self, request, project_id, pk):
        self.get_object().in_progress()
        return Response({"message": "L'issue est maintenant en cours."})

    @action(detail=True, methods=['post'])
    def finished(self, request, project_id, pk):
        self.get_object().finished()
        return Response({"message": "L'issue est maintenant terminée."})


class CommentViewset(ReadOnlyModelViewSet):

    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        issue_id = self.kwargs.get('issue_id')
        user = self.request.user
        issue = Issue.objects.get(id=issue_id)
        project_id = issue.project_id
        is_contributor = Contributor.objects.filter(
            user=user,
            project__id=project_id
        ).exists()

        if is_contributor:
            return Comment.objects.filter(issue__id=issue_id)
        else:
            raise PermissionDenied("You don't have permission "
                                   "to access Comments in this project.")

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()

    @action(detail=False, methods=['post'])
    def add_comment(self, request, issue_id):
        issue = Issue.objects.get(pk=issue_id)
        user = self.request.user

        is_contributor = Contributor.objects.filter(
            user=user,
            project=issue.project
        ).exists()

        if not is_contributor:
            raise PermissionDenied("You don't have"
                                   " permission to create"
                                   " a comment in this project.")

        data = request.data.copy()
        data['issue'] = issue.id
        data['author'] = user.id

        serializer = CommentListSerializer(data=data)

        if serializer.is_valid():
            comment = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    def update_comment(self, request, issue_id, pk=None):
        comment = self.get_object()

        if comment.author == request.user:
            serializer = CommentDetailSerializer(comment,
                                                 data=request.data,
                                                 partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            raise PermissionDenied("You don't have permission "
                                   "to update this comment.")

    @action(detail=True, methods=['delete'])
    def delete_comment(self, request, issue_id, pk=None):

        try:
            comment = get_object_or_404(Comment, pk=pk)

            if request.user == comment.author:
                comment.delete()
                return Response({'message': 'comment deleted successfully.'},
                                status=status.HTTP_204_NO_CONTENT)
            else:
                raise PermissionDenied("You don't have permission"
                                       " to delete this comment.")
        except Comment.DoesNotExist:
            return Response({'message': 'Comment not found'},
                            status=status.HTTP_404_NOT_FOUND)
