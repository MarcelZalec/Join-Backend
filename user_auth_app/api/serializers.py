from rest_framework import serializers
from user_auth_app.models import CustomUser
# from django.contrib.auth.models import User

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        em = attrs.get('email')
        pw = attrs.get('password')
        print(attrs)
        user = CustomUser.objects.filter(email=em).first()
        if user and user.is_active and user.check_password(pw):
            attrs['user'] = user  # Hier wird der validierte Benutzer gespeichert
            return attrs
        raise serializers.ValidationError({'error': "Wrong credentials"})
            
        

class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only = True)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'repeated_password']
        extra_kwargs = {
            'password' : {
                'write_only': True
            }
        }
    
    def validate(self, attrs):
        pw = attrs.get('password')
        repeated_pw = attrs.get('repeated_password')
        em = attrs.get('email')
        
        if pw != repeated_pw:
            raise serializers.ValidationError({'error': "Passwords don't match"})
        
        if CustomUser.objects.filter(email = em).exists():
            raise serializers.ValidationError({'error': "Email allready exists"})
        return attrs
    
    def save(self, **kwargs):
        pw = self.validated_data['password']
        em = self.validated_data['email']
        account = CustomUser(email = em, username = self.validated_data['username'])
        account.set_password(pw)
        account.save()
        return account