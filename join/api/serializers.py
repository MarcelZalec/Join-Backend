from rest_framework import serializers
from join.models import Task, Contacts, Subtask


class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = '__all__'


class SubtaskSerializer(serializers.Serializer):
    class Meta:
        model = Subtask
        fields = ['id', 'task_description', 'is_tasked_checked', 'task']


class TaskSerializer(serializers.ModelSerializer):
    subtasks = SubtaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
        
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    
    def create(self, validated_data):
        return super().create(validated_data)


class AssignedSerializer(TaskSerializer):
    class Meta:
        model = Task
        fields = ["assigned"]