from rest_framework import generics,status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Snippet, Tag
from .serializers import SnippetSerializer, TagSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.urls import reverse


class SnippetListCreateView(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SnippetDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        tag = instance.tag
        self.perform_destroy(instance)
        if tag:
            tag.delete()
        return Response({"detail": "Snippet and associated tag deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class TagListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class TagDetailView(generics.RetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    

class SnippetOverview(APIView):
    def get(self, request, *args, **kwargs):
        snippet_count = Snippet.objects.count()
        snippets = Snippet.objects.all()
        snippet_serializer = SnippetSerializer(snippets, many=True)

        overview_data = {
            "total_snippets": snippet_count,
            "snippet_list": snippet_serializer.data
        }

        for snippet_data in overview_data["snippet_list"]:
            snippet_id = snippet_data["id"]
            snippet_data["detail_url"] = reverse("snippet-detail", kwargs={"pk": snippet_id})

        return Response(overview_data, status=status.HTTP_200_OK)
