from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import Organization, MemberShip
from .serializers import OrganizationHyperlinkedSerializer, MemberShipSerializer
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from .permission import MembershipPermission

class OrganizationViewSet(ModelViewSet):
    lookup_field = 'slug'
    queryset = Organization.objects.all()
    serializer_class = OrganizationHyperlinkedSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Organization.objects.filter(owner=self.request.user)

    @action(detail=True,methods=['get'])
    def projects(self,request,slug):
        organization=Organization.objects.get(slug=slug)
        serializer = OrganizationHyperlinkedSerializer(organization.projects,many=True)
        return Response(serializer.data)

    @action(detail=True,methods=['get'])
    def members(self,request, slug):
        organization=Organization.objects.get(slug=slug)
        serializer = MemberShipSerializer(organization.memberships,many=True)
        return Response(serializer.data)

class MemberViewSet(ModelViewSet):
    lookup_field = 'id'
    queryset = MemberShip.objects.all()
    serializer_class = MemberShipSerializer
    permission_classes = [MembershipPermission,IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['role']
    

    def get_queryset(self):
        return MemberShip.objects.filter(organization__memberships__user=self.request.user)

