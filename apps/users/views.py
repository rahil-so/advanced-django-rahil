from rest_framework import viewsets, authentication, filters
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from .models import User
from apps.users.serializers import LoginSerializer,UserBriefSerializer
from rest_framework.permissions import  IsAuthenticated

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserBriefSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']

class LoginView(APIView):
    permission_classes = []
    serializer_class = LoginSerializer


    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token, _ = Token.objects.get_or_create(user=serializer.validated_data['user'])
        return Response({'token': token.key, 'user_id': serializer.validated_data['user'].id})

    

