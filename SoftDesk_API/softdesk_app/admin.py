from django.contrib import admin
from authentication.models import User
from .models import Project, Contributor, Issue, Comment


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'time_created', 'author')


class ContributorAdmin(admin.ModelAdmin):
    list_display = ('user', 'project')


class IssueAdmin(admin.ModelAdmin):
    list_display = ('project', 'name', 'priority', 'balise',
                    'status', 'time_created')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('issue', 'author', 'time_created')


admin.site.register(User)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Comment, CommentAdmin)
