from rest_framework import serializers
from join.models import Task, Contacts, Subtask


class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = '__all__'


class SubtaskSerializer(serializers.Serializer):
    task_description = serializers.CharField()
    is_tasked_checked = serializers.BooleanField()
    
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        # Überprüfung und Umbenennen der Schlüssel
        print("Empfangene Daten:", data)
        if 'task-description' in data:
            data['task_description'] = data.pop('task-description')
        if 'is-tasked-checked' in data:
            data['is_tasked_checked'] = data.pop('is-tasked-checked')
        return data


## class TaskSerializer(serializers.ModelSerializer):
##     subtasks = SubtaskSerializer(many=True, required=False)
##     class Meta:
##         model = Task
##         fields = '__all__'
##         
##     def create(self, validated_data):
##         subtasks_data = validated_data.pop('subtasks', [])
##         print(f"das ist das Objekt {validated_data}")
##         task = Task.objects.create(**validated_data)
##         
##         # Erstelle die Subtasks und verknüpfe sie mit der Aufgabe
##         subtasks = [Subtask.objects.create(**subtask_data) for subtask_data in subtasks_data]
##         task.subtasks.set(subtasks)  # Nutze `.set()` für Many-to-Many
##         
##         return task

class TaskSerializer(serializers.ModelSerializer):
    subtasks = SubtaskSerializer(many=True, required=False)

    class Meta:
        model = Task
        fields = '__all__'

    def create(self, validated_data):
        subtasks_data = validated_data.pop('subtasks', [])
        task = Task.objects.create(**validated_data)
        subtasks = [Subtask.objects.create(**subtask_data) for subtask_data in subtasks_data]
        task.subtasks.set(subtasks)  # Nutze `.set()` für Many-to-Many
        return task

    def update(self, instance, validated_data):
        subtasks_data = validated_data.pop('subtasks', [])
        instance = super().update(instance, validated_data)

        # Subtasks aktualisieren
        instance.subtasks.clear()  # Entferne alte Subtasks
        subtasks = [Subtask.objects.create(**subtask_data) for subtask_data in subtasks_data]  # Neue erstellen
        instance.subtasks.set(subtasks)  # Setze die neuen Subtasks als Many-to-Many-Beziehung

        return instance


class TaskSerializerV2(serializers.ModelSerializer):
    subtasks = SubtaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
        
    def update(self, instance, validated_data):
        subtasks_data = validated_data.pop('subtasks', [])
        assigned_to_data = validated_data.pop(
            'assigned_to', None)  # kann auch leer

        # Update task fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update assigned users correctly (ManyToMany)
        if assigned_to_data is not None:
            # Expecting a list of IDs
            instance.assigned_to.set(assigned_to_data)

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


class TaskSerializerOriginal(serializers.ModelSerializer):
    subtasks = SubtaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
        
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    
    def create(self, validated_data):
        return super().create(validated_data)