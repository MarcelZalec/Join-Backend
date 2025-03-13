from django.urls import path, include
from .views import TaskSingleView, TasksViewList, TaskView, ContactsView, SubTaskView
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'tasks', TaskView)
router.register(r'contacts', ContactsView)
# router.register(r'subtasks', SubTaskView)


urlpatterns = [
    path('', include(router.urls)),
    path('tasks/<int:pk>/subtasks', SubTaskView.as_view({'get': 'list'})),
    # path('contacts/', ContactsView.as_view())
    # path('tasks/', TasksViewList.as_view()),
    # path('tasks/<int:pk>', TaskSingleView.as_view()),
]
