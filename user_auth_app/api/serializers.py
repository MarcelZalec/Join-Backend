from rest_framework import serializers
from django.contrib.auth.models import User

class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only = True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password']
        extra_kwargs = {
            'password' : {
                'write_only': True
            }
        }
    
    def save(self, **kwargs):
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['repeated_password']
        em = self.validated_data['email']
        
        if pw != repeated_pw:
            raise serializers.ValidationError({'error': "Passwords don't match"})
        
        if User.objects.filter(email = em).exists():
            raise serializers.ValidationError({'error': "Email allready exists"})
        
        account = User(email = em, username = self.validated_data['username'])
        account.set_password(pw)
        account.save()
        return account