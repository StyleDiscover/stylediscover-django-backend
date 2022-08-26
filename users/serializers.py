from users.models import UserAccount, Wishlist

#DRF imports
from rest_framework import serializers, pagination
from rest_framework.settings import api_settings

# dj-auth imports
from dj_rest_auth.serializers import UserDetailsSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer

#wishlist, and mainpost serializers
from components.models import ComponentPost
from mainposts.models import MainPost
from mainposts.serializers import MainPostComponents, MainPostSerializer


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['id', 'username', 'name', 'email', 'account_type', 'is_premium', 'password','modified_username']

    def create(self, validated_data):
        """Create and return a new User."""

        email = validated_data['email']
        username = validated_data['username']
        name = validated_data['name']
        modified_username = validated_data['modified_username']
        account_type = validated_data['account_type']
        user = UserAccount(username=username, email=email, name=name, modified_username=modified_username, account_type=account_type)

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = [
            'id',
            'username',
            'name',
            'email',
            'account_type',
            'profile_picture',
            'user_bio',
            'is_premium',
            'provider',
            'modified_username',
            'sent_insta_email',
            'user_website'
        ]


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = [
            'id',
            'name',
            'account_type',
            'profile_picture',
            'user_bio',
            'user_website',
        ]

class ChangeUsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = [
            'id',
            'username',
            'modified_username'
        ]

class KnoxSerializer(serializers.Serializer):
    token = serializers.CharField()
    user = UserDetailsSerializer()

    def get_token(self, obj):
        return obj["token"][1]


class UserPostSerializer(serializers.ModelSerializer):
    main_posts = serializers.PrimaryKeyRelatedField(queryset=MainPost.objects.all(), many=True, allow_null=True)

    class Meta:
        model = UserAccount
        fields = ['id', 'username', 'profile_picture', 'name', 'main_posts', 'user_website', 'user_bio']


class UserWishlistSerializer(serializers.ModelSerializer):
    wishlist = serializers.PrimaryKeyRelatedField(queryset=ComponentPost.objects.all(), many=True, allow_null=True)

    class Meta:
        model = UserAccount
        fields = ['id', 'name', 'wishlist']

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ['wishlist_item']

class UserComponentsSerializer(serializers.ModelSerializer):
    main_posts = MainPostComponents(many=True, read_only=True)

    class Meta:
        model = UserAccount
        fields = ['id', 'main_posts']

class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['id', 'username', 'profile_picture']
