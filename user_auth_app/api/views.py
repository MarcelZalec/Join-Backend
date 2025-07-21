from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import serializers
from .serializers import RegistrationSerializer, LoginSerializer

class CustomLoginView(ObtainAuthToken):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data = request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created= Token.objects.get_or_create(user = user)
            data = {
                'token': token.key,
                'username': user.username,
                'email': user.email
            }
        else:
            data = serializer.errors
        
        return Response(data)


class RegistrationView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            try:
                saved_account = serializer.save()
                token, created = Token.objects.get_or_create(user=saved_account)
                return Response({
                    'token': token.key,
                    'username': saved_account.username,
                    'email': saved_account.email
                })
            except serializers.ValidationError as e:
                return Response(e.detail, status=400)
        else:
            return Response(serializer.errors, status=400)


class GuestLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Token aus dem Authorization Header extrahieren
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Token '):
            return Response({'error': 'Authorization header is required and must contain the token'}, status=400)

        # Den eigentlichen Token extrahieren (nach 'Token ')
        token_key = auth_header.split(' ')[1]

        try:
            # Überprüfen, ob der Token existiert
            token = Token.objects.get(key=token_key)
            user = token.user
            data = {
                'message': 'Token valid',
                'token': token.key,
                'username': user.username,
                'email': user.email
            }
            return Response(data, status=200)
        except Token.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=400)