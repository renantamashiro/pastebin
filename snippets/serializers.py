from django.contrib.auth.models import User
from rest_framework import serializers
from snippets.models import Snippet, Travel, LANGUAGE_CHOICES, STYLE_CHOICES


class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())
    
    class Meta:
        model = User
        fields = ['id', 'username', 'snippets']

class UserTravelSerializer(serializers.ModelSerializer):
    travels= serializers.PrimaryKeyRelatedField(many=True, queryset=Travel.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'travels']

class SnippetSerializer0(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')
    

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Snippet.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance


class TravelSerializer0(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    location = serializers.CharField(allow_blank=False, max_length=100, required=True)
    description = serializers.CharField(style={'base-template': 'textarea.html'})
    country = serializers.CharField(required=True, max_length=100)
    date_travel = serializers.DateField()

    def create(self, validated_data):
        """
        Create and return a new Travel instance, given the validated data.
        """
        return Travel.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """
        Update and return an existing Travel instance, given the validated data.
        """
        instace.location = validated_data.get('location', instance.location)
        instace.description = validated_data.get('description', instance.description)
        instace.country = validated_data.get('country', instance.country)
        instace.date_travel = validated_data.get('date_travel', instance.date_travel)
        return instance


class SnippetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Snippet
        fields = ['id', 'title', 'code', 'linenos', 'language', 'style', 'owner']


class TravelSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Travel
        fields = ['id', 'location', 'description', 'country', 'date_travel', 'owner']