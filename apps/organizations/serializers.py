from rest_framework import serializers
from apps.organizations.models import Organization, MemberShip


class OrganizationHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True)
    projects_url = serializers.HyperlinkedIdentityField(view_name='project-detail',
                                                        read_only=True, lookup_field='slug')
    members_url = serializers.HyperlinkedIdentityField(view_name='member-detail', read_only=True)
    class Meta:
        model = Organization
        fields = [
            'url','id','members_url',
             'name', 'slug', 'owner',  'plan','projects_url','created_at'
        ]
        #'members_url', add this later and realize why aslani write it like this
        extra_kwargs = {
            'url': {
                'view_name': 'organization-detail',
                'lookup_field': 'slug'
            }
        }
class MemberShipSerializer(serializers.ModelSerializer):
    class Meta:
        Model = MemberShip
        fields=[
            'id','user','organization','role','joined_at']
        read_only_fields=['id','joined_at','organization','role','user']
