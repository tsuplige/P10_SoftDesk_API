"""
URL configuration for SoftDesk_API project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from softdesk_app.views import (ProjectViewset, CommentViewset, IssueViewset,
                                ContributorViewset
                                )
from authentication.views import UserViewSet, SignupView
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

router = routers.SimpleRouter()

router.register(r'projects', ProjectViewset, basename='project')
router.register(r'projects/(?P<project_id>\d+)/issues',
                IssueViewset,
                basename='issues')
router.register(r'projects/(?P<project_id>\d+)/contributors',
                ContributorViewset,
                basename='contributors')
router.register(r'issues/(?P<issue_id>\d+)/comments',
                CommentViewset,
                basename='comments')
router.register('user', UserViewSet, basename='user')

urlpatterns = [
    path("admin/", admin.site.urls),

    path('api/projects/<int:project_id>/issues/<int:pk>/delete_issue/',
         IssueViewset.as_view({'delete': 'delete_issue'}),
         name='delete-issue'),

    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),

    path("api/signup/", SignupView.as_view(), name='signup'),

    path("api/", include(router.urls)),

]
