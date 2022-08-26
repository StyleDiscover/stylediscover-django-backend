from mainposts.models import MainPost
from mainposts.serializers import MainPostSerializer, EmailSerializer, MainPostCategorySerializer, MainPostChoiceSerializer
from mainposts.permissions import IsUserOrReadOnly
from rest_framework import permissions, viewsets, status
from rest_framework.views import APIView

from django.core import files
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

# sending emails
from django.core.mail import send_mail, mail_admins
from clarendon.settings import EMAIL_HOST_USER
from django.http import QueryDict
from users.models import UserAccount
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from mainposts.models import Categories
from rest_framework.pagination import PageNumberPagination


class MainPostViewset(viewsets.ModelViewSet):
    queryset = MainPost.objects.all()
    serializer_class = MainPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsUserOrReadOnly]

    def perform_create(self, serializer):
        user = self.request.user
        if(user.account_type == 'HI' and not ('category' in self.request.data)):
            serializer.save(user=self.request.user, photo_of=self.request.user, category=Categories.HOM)
        else:
            serializer.save(user=self.request.user, photo_of=self.request.user)
        # try:
        #     if(self.request.data['media_type'] != 'VD'):
        #         file = self.request.data['media_url']
        #         o_file = default_storage.save(f'original/main_post_media/{self.request.user}/{file}', file)
        # except:
        #     print('error occured while uploading original image/video')

class SendEmailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, format=None):
        subject = request.data['subject']
        message = request.data['message']
        username = request.data['username']

        user_filter = UserAccount.objects.filter(username=username)
        user = get_object_or_404(user_filter)

        emailData = {
            'subject': subject,
            'message': message,
            'usename': username
        }

        query_dict = QueryDict('', mutable=True)
        query_dict.update(emailData)


        if username:
            mail_admins(subject=subject, message=message,)
            user_filter.update(sent_insta_email=True)

            return Response(data={'message': 'sent!'})

        return Response(data={'error': 'Failed to deliver email.'},status=status.HTTP_400_BAD_REQUEST)

class MainPostCategoryView(APIView):
    def get(self, request, pk=None, format=None):
        category_list = MainPost.objects.values_list('category', flat=True).distinct()
        g_by_c = {}
        for category in category_list:
            queryset = MainPost.objects.filter(category=category, user=pk)
            serializer = MainPostCategorySerializer(queryset, many=True)
            cat = str(Categories[category].label)
            g_by_c[cat] = serializer.data
        return Response(g_by_c)



class MainPostCategoryDetailsView(APIView, PageNumberPagination):
    def get(self, request, pk=None, category=None, format=None):
        queryset = MainPost.objects.filter(category=category, user=pk)
        paginated_queryset = self.paginate_queryset(queryset, request, view=self)
        serializer = MainPostCategorySerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    page_size = 3

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

class MainPostPhotoOfDetailsView(APIView, PageNumberPagination):
    def get(self, request, pk=None, category=None, format=None):
        queryset = MainPost.objects.filter(category=category, photo_of=pk)
        paginated_queryset = self.paginate_queryset(queryset, request, view=self)
        serializer = MainPostCategorySerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    page_size = 3

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

class MainPostChoicesView(APIView):
    def get(self, request, format=None):
        serializer = MainPost._meta.get_field('category').choices
        return Response({'choices': serializer})