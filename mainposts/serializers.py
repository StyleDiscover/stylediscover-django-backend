from rest_framework import serializers
from mainposts.models import MainPost, Categories
from components.models import ComponentPost


class MainPostSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    account_type = serializers.ReadOnlyField(source='user.account_type')
    name = serializers.ReadOnlyField(source='user.name')
    profile_picture = serializers.ImageField(source='user.profile_picture', read_only=True)
    # user = UserDetailsSerializer()
    component_posts = serializers.PrimaryKeyRelatedField(queryset=ComponentPost.objects.all(), many=True, allow_null=True)

    class Meta:
        model = MainPost
        fields = ['id', 
            'user_id', 
            'username', 
            'name', 
            'profile_picture', 
            'component_posts', 
            'media_url', 
            'media_type', 
            'caption', 
            'category', 
            'created_at', 
            'last_modified', 
            'is_deleted', 
            'source', 
            'photo_of',
            'account_type'
        ]

class MainPostComponents(serializers.ModelSerializer):
    component_posts = serializers.PrimaryKeyRelatedField(queryset=ComponentPost.objects.all(), many=True, allow_null=True)

    class Meta:
        model = MainPost
        fields = ['component_posts']

class EmailSerializer(serializers.Serializer):
    subject = serializers.CharField(required=True)
    message = serializers.CharField(required=True)
    username = serializers.CharField()

    class Meta:
        fields = ['subject', 'message', 'username']

class MainPostCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MainPost
        fields = ['id', 'media_url', 'media_type']

class MainPostChoiceSerializer(serializers.Serializer):
    choices = serializers.ChoiceField(choices=Categories, allow_blank = True)
    class Meta:
        fields = ['choices']
