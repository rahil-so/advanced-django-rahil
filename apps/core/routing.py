from rest_framework.routers import DefaultRouter
from apps.projects.views import ProjectViewSet
from apps.comments.views import CommentViewSet
from apps.organizations.views import OrganizationViewSet
from apps.tasks.views import TaskViewSet
from apps.users.views import UserViewSet

router = DefaultRouter()
router.register('projects', ProjectViewSet)
router.register('comments',CommentViewSet)
router.register('tasks', TaskViewSet)
router.register('organizations', OrganizationViewSet)
router.register('users',UserViewSet)
