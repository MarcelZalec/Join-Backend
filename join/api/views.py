from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, generics, status
from join.models import Task, Contacts, Subtask
from .serializers import TaskSerializer, ContactsSerializer, SubtaskSerializer
from rest_framework.views import APIView

from rest_framework import mixins
from rest_framework import generics
from user_auth_app.api.permissions import IsStaffOrReadOnly

# Create your views here.

class TaskView(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsStaffOrReadOnly]


class TaskSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TasksViewList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ContactsView(viewsets.ModelViewSet):
    queryset = Contacts.objects.all()
    serializer_class = ContactsSerializer
    permission_classes = [IsStaffOrReadOnly]


class ContactsViewOLD(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Contacts.objects.all()
    serializer_class = ContactsSerializer
    permission_classes = [IsStaffOrReadOnly]
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SubTaskView(APIView):
    serializer_class = SubtaskSerializer
    permission_classes = [IsStaffOrReadOnly]
    
    
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Task.objects.filter(pk = pk)
    
    def post(self, request, *args, **kwargs):
        serializer = SubtaskSerializer(data=request.data, many=True)
        if serializer.is_valid():
            print(f"das sind die Daten: {serializer}")
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, *args, **kwargs):
        subtasks = Subtask.objects.all()  # Alle Subtasks abrufen
        serializer = SubtaskSerializer(subtasks, many=True)  # `many=True` für Listen
        return Response(serializer.data)