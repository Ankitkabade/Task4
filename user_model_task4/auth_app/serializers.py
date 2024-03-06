from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .models import User
from task4app.serializers import TaskSerializer


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    user_task = TaskSerializer(read_only=True,many=True)
    tasks = TaskSerializer(read_only=True,many=True)
    class Meta:
        model = User
        fields = ('id','username','password','email','first_name','last_name','gender','address','pincode','city','contact','role','company','user_task','tasks')
        
        
    def create(self, validated_data):
        obj = User.objects.create_user(**validated_data)
        obj.is_active=False
        obj.save()
        return obj