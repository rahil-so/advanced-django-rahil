from rest_framework.routers import DefaultRouter
from apps.projects.views import ProjectViewSet
from apps.comments.views import CommentViewSet
from apps.organizations.views import OrganizationViewSet
from apps.tasks.views import TaskViewSet
from apps.users.views import UserViewSet

router = DefaultRouter()
router.register('projects', ProjectViewSet, basename='project')
router.register('comments',CommentViewSet, basename='comment')
router.register('tasks', TaskViewSet, basename='task')
router.register('users', UserViewSet, basename='user')
router.register('organizations', OrganizationViewSet,basename='organization')

