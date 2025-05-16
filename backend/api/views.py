from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics,serializers
from .serializers import UserSerializer, NoteSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Note

# Create your views here.

class NoteListCreate(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(auther=user)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(auther=self.request.user)
        else:
            raise serializer.ValidationError(serializer.errors)
        
class NoteDelete(generics.DestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    queryset = Note.objects.all()


    def get_object(self):
            user = self.request.user
            pk = self.kwargs['pk']
            try:
                return Note.objects.get(pk=pk, auther=user)
            except Note.DoesNotExist:
                raise serializers.ValidationError("Note not found or not authorized to delete.")

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
