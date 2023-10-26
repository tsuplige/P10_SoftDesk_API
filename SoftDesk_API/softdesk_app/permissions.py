from rest_framework.permissions import BasePermission


class IsContributor(BasePermission):

    def has_permission(self, request, view):
        project = view.get_object()
        return project.work_on.filter(user=request.user).exists()

class IsAuthor(BasePermission):

    def has_permission(self, request, view):
        project = view.get_object()
        return project.work_on.filter(user=request.user).exists()