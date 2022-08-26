#general imports
from django.shortcuts import render
from users.serializers import (
    RegisterSerializer, 
    UserSearchSerializer, 
    KnoxSerializer, 
    UserPostSerializer, 
    UserWishlistSerializer, 
    UserInfoSerializer, 
    UserDetailsSerializer, 
    ChangeUsernameSerializer, 
    UserComponentsSerializer,
    WishlistSerializer,
)
from users.utils import create_knox_token
from users.permissions import IsUserOrReadOnly, IsUser, IsAdmin
from users.models import UserAccount, Wishlist, InstagramToken
from django.shortcuts import get_object_or_404
from django.http import QueryDict
from django.db import connection
from django.core.files.storage import default_storage

#DRF imports
from rest_framework import permissions, viewsets, status, generics, mixins, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

#allauth imports
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.shopify.views import ShopifyOAuth2Adapter
from allauth.socialaccount.providers.instagram.views import InstagramOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.account.utils import complete_signup
from allauth.account import app_settings as allauth_settings

#dj-rest-auth imports
from dj_rest_auth.registration.views import SocialLoginView, RegisterView
from dj_rest_auth.views import LoginView

#wishlist imports
from components.models import ComponentPost
from components.serializers import ComponentPostSerializer

#post imports
from mainposts.models import MainPost
from mainposts.serializers import MainPostComponents, MainPostSerializer

#knox import
from knox.models import AuthToken

#knox integrations
class KnoxLoginView(LoginView):
    def get_response(self):
        serializer_class = self.get_response_serializer()

        data = {'user': self.user, 'token': self.token}
        serializer = serializer_class(instance=data, context={'request': self.request})

        return Response(serializer.data, status=200)


class KnoxRegisterView(RegisterView):
    def get_response_data(self, user):
        return KnoxSerializer({'user': user, 'token': self.token}).data

    def perform_create(self, serializer):
        user = serializer.save()
        self.token = create_knox_token(None, user, None)
        complete_signup(self.request._request, user, None, success_url="localhost:3000")
        return user


#facebook login view
class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter

    def get_response(self):
        serializer_class = self.get_response_serializer()

        data = {'user': self.user, 'token': self.token}
        serializer = serializer_class(instance=data, context={'request': self.request})

        return Response(serializer.data, status=200)

#instagram login view
class InstagramLogin(SocialLoginView):
    adapter_class = InstagramOAuth2Adapter

    def get_response(self):
        serializer_class = self.get_response_serializer()

        data = {'user': self.user, 'token': self.token}
        serializer = serializer_class(instance=data, context={'request': self.request})

        cursor = connection.cursor()
        cursor.execute("SELECT uid FROM socialaccount_socialaccount WHERE user_id = %s", [self.user.id])
        results = cursor.fetchone()
        insta_id = results[0]

        insta_token_field = InstagramToken.objects.get_or_create(user=self.user, insta_id=insta_id)
        insta_token_field[0].access_token = self.request.data['access_token']
        insta_token_field[0].save()

        return Response(serializer.data, status=200)


#wishlist views NEW
class WishlistViews(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None, format=None):
        # paginator = CustomPageNumberPagination()
        # queryset = Wishlist.objects.filter(user=pk)
        # results = paginator.paginate_queryset(queryset, request)
        # serializer = WishlistSerializer(results, many=True)
        # return paginator.get_paginated_response(serializer.data)
        queryset = UserAccount.objects.filter(username=pk)
        user = get_object_or_404(queryset)
        serializer = UserWishlistSerializer(user)
        return Response(serializer.data)
    
    def put(self, request, pk=None, format=None):
        try:
            wishlist_component = request.data['component_id']
        except:
            return Response(status.HTTP_400_BAD_REQUEST)
        user_queryset = UserAccount.objects.filter(username=pk)
        user = get_object_or_404(user_queryset)
        component_queryset = ComponentPost.objects.filter(id=wishlist_component)
        component = get_object_or_404(component_queryset)
        user.wishlist.add(component)
        serializer = UserWishlistSerializer(user)
        return Response(serializer.data)

    def delete(self, request, pk=None, format=None):
        try:
            wishlist_component = request.data['component_id']
        except:
            return Response(status.HTTP_400_BAD_REQUEST)
        user_queryset = UserAccount.objects.filter(username=pk)
        user = get_object_or_404(user_queryset)
        component_queryset = ComponentPost.objects.filter(id=wishlist_component)
        component = get_object_or_404(component_queryset)
        user.wishlist.remove(component)
        serializer = UserWishlistSerializer(user)
        return Response(serializer.data)



#Post view
class UserPostView(APIView, PageNumberPagination):
    def get(self, request, pk=None, format=None):
        queryset = MainPost.objects.filter(user=pk)
        paginated_queryset = self.paginate_queryset(queryset, request, view=self)
        serializer = MainPostSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def get_next_link(self):
        if not self.page.has_next():
            return None
        page_number = self.page.next_page_number()
        return page_number

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        page_number = self.page.previous_page_number()
        return page_number

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'results': data
        })

#User Info Update View
class UserInfoUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def put(self, request, pk=None, format=None):
        queryset = UserAccount.objects.filter(username=pk)
        user = get_object_or_404(queryset)
        serializer = UserInfoSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # if(request.data['profile_picture']):
            #     file = request.data['profile_picture']
            #     o_file = default_storage.save(f'original/profile_pictures/{request.user}/{file}', file)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#User details view
class UserDetailsView(APIView):
    def get(self, request, pk=None, format=None):
        queryset = UserAccount.objects.filter(username=pk)
        user = get_object_or_404(queryset)
        serializer = UserDetailsSerializer(user)
        return Response(serializer.data)

#Change Username view
class ChangeUsernameView(mixins.UpdateModelMixin, generics.GenericAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = ChangeUsernameSerializer
    permission_classes = [permissions.IsAuthenticated, IsUser]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

# get all components user used
class UserComponentView(APIView):
    def get(self, request, pk=None, format=None):
        queryset = UserAccount.objects.filter(username=pk)
        user = get_object_or_404(queryset)
        serializer = UserComponentsSerializer(user)
        return Response(serializer.data)


#admin login as user
class LoginAsUser(APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def get(self, request, pk=None, format=None):
        queryset = UserAccount.objects.filter(username=pk)
        user = get_object_or_404(queryset)
        token = AuthToken.objects.create(user=user)
        serializer = KnoxSerializer({'user': user, 'token': token})
        return Response(serializer.data)

#get user info (using token)
class UserAPIView(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserDetailsSerializer

    def get_object(self):
        return self.request.user

class UserViewset(viewsets.ReadOnlyModelViewSet):
    queryset = UserAccount.objects.all()
    serializer_class = UserDetailsSerializer

#custom pagination class
class CustomPageNumberPagination(PageNumberPagination):
    
    page_size = 10

    def get_next_link(self):
        if not self.page.has_next():
            return None
        page_number = self.page.next_page_number()
        return page_number

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        page_number = self.page.previous_page_number()
        return page_number

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'results': data
        })

#search user
class DynamicSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        return request.GET.getlist('search_fields', [])

class SearchUserView(generics.ListAPIView):
    filter_backends = (DynamicSearchFilter,)
    queryset = UserAccount.objects.all()
    serializer_class = UserSearchSerializer
    pagination_class = CustomPageNumberPagination
