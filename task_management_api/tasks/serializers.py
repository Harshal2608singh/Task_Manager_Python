from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='assigned_to',
        write_only=True
    )

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'status',
            'assigned_to',
            'assigned_to_id',
            'created_by',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_by']
