from django.db import models
from django.contrib.auth.models import User
from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated
from django.urls import path, include
from django.contrib import admin
from django.urls import path

# Models
class Client(models.Model):
    client_name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Project(models.Model):
    project_name = models.CharField(max_length=255)
    client = models.ForeignKey(Client, related_name='projects', on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='projects')
    created_by = models.ForeignKey(User, related_name='created_projects', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

# Serializers
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

# Views
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

# URL routing
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'projects', ProjectViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]

# To run the application
if __name__ == "__main__":
    import os
    import django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_management.settings")
    django.setup()
