from rest_framework.permissions import BasePermission
from softdesk_app.models import Contributor


class IsContributor(BasePermission):

    def has_permission(self, request, view):
        project = view.get_object()
        return project.work_on.filter(user=request.user).exists()


class IsAuthor(BasePermission):

    def has_permission(self, request, view):
        project = view.get_object()
        contributor = Contributor.objects.filter(project=project.id,
                                                 user=request.user).first()

        if contributor and contributor.is_author():
            print('est auteur')
            return True

        print('n\'est pas auteur')
        return False
