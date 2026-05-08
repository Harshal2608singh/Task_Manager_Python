from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Task
from .serializers import TaskSerializer
from .permissions import IsAdminOrManager

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = ['status']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
