from django.contrib import admin
from django.urls import path, include

from rest_framework_nested import routers


from api.views import (
    ProjectViewset,
    ContributorViewset,
    IssueViewset,
    CommentViewset,
)

router = routers.SimpleRouter()
router.register("projects", ProjectViewset, basename="projects")

# Nested router for users & issues
project_router = routers.NestedSimpleRouter(
    router, "projects", lookup="project"
)
project_router.register("users", ContributorViewset, basename="contributors")
project_router.register("issues", IssueViewset, basename="issues")

# Nested router for issues
issue_router = routers.NestedSimpleRouter(
    project_router, "issues", lookup="issues"
)
issue_router.register("comments", CommentViewset, basename="comments")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("account.urls")),
    path("", include(router.urls)),
    path("", include(project_router.urls)),
    path("", include(issue_router.urls)),
]
