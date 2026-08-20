from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import Organization
from .serializers import OrganizationHyperlinkedSerializer
from rest_framework.filters import SearchFilter


class OrganizationViewSet(ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationHyperlinkedSerializer
    permission_class = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['name']


    def get_queryset(self):
        return Organization.objects.filter(Owner=self.request.user)



