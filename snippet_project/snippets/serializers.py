from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Snippet, Tag

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class TagSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ['id', 'title', 'content']

    def get_content(self, obj):
        snippets = Snippet.objects.filter(tag=obj)
        content_list = [snippet.content for snippet in snippets]
        return content_list

    def to_internal_value(self, data):
        title = data.get('title', None)

        if title:
            existing_tag = Tag.objects.filter(title=title).first()

            if existing_tag:
                return {'id': existing_tag.id, 'title': existing_tag.title, 'content': self.get_content(existing_tag)}

        return super(TagSerializer, self).to_internal_value(data)

    def create(self, validated_data):
        # Avoid setting ID when creating a new tag
        return Tag.objects.create(title=validated_data['title'])

class SnippetSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  
    tag = TagSerializer(required=False)

    class Meta:
        model = Snippet
        fields = ['id', 'title', 'content', 'timestamp', 'user', 'tag']

    def create(self, validated_data):
        user = self.context['request'].user
        snippet_data = {**validated_data, 'user': user}
        tag_data = snippet_data.pop('tag', None)

        snippet = Snippet.objects.create(**snippet_data)

        if tag_data:
            tag, _ = Tag.objects.get_or_create(title=tag_data['title'])
            snippet.tag = tag
            snippet.save()

        return snippet
