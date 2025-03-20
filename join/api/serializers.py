from rest_framework import serializers
from join.models import Task, Contacts, Subtask


class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = '__all__'


class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = '__all__'
        # fields = ['id', 'task_description', 'is_tasked_checked', 'task']
    
    
    def to_internal_value(self, data):
        # data = super().to_internal_value(data)
        # print(f"Empfangene Daten: {data}")
        if 'task-description' in data:
            data['task_description'] = data.pop('task-description')
        if 'is-tasked-checked' in data:
            data['is_tasked_checked'] = data.pop('is-tasked-checked')
        # print(f"daten Nach der Umwandlung: {data}")
        return super().to_internal_value(data)
    
    
    # def create(self, validated_data):
    #     # Wenn `many=True`, enthält validated_data eine Liste von Dictionaries
    #     print("Validierte Daten:", validated_data) 
    #     subtasks = [Subtask(**item) for item in validated_data]
    #     return Subtask.objects.bulk_create(subtasks)


class TaskSerializer(serializers.ModelSerializer):
    subtasks = SubtaskSerializer(many=True)

    class Meta:
        model = Task
        fields = '__all__'
        
    def update(self, instance, validated_data):
        subtasks_data = validated_data.pop('subtasks', [])
        assigned_to_data = validated_data.pop(
            'assigned', None)  # kann auch leer

        # Update task fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update assigned users correctly (ManyToMany)
        if assigned_to_data is not None:
            # Expecting a list of IDs
            instance.assigned(assigned_to_data)

        # Update subtasks correctly
        instance.subtasks.all().delete()  # Clear old subtasks
        for subtask_data in subtasks_data:
            instance.subtasks.create(**subtask_data)

        return instance
    
    def create(self, validated_data):
        subtasks_data = validated_data.pop('subtasks', [])
        assigned_to_data = validated_data.pop(
            'assigned', [])  # kann auch leer sein

        # Create the task first
        task = Task.objects.create(**validated_data)

        task.assigned.set(assigned_to_data)

        # Create the related subtasks
        for subtask_data in subtasks_data:
            Subtask.objects.create(task=task, **subtask_data)

        return task


class AssignedSerializer(TaskSerializer):
    class Meta:
        model = Task
        fields = ["assigned"]