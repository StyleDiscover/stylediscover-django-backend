from components.models import ComponentPost, SiteRecord
from components.serializers import ComponentPostSerializer, SiteRecordSerializer
from rest_framework import permissions, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import tempfile
from django.core import files
from django.shortcuts import get_object_or_404, Http404
from django.http import QueryDict
from django.core.files.images import ImageFile
from django.core.files.storage import default_storage


class ComponentListViewset(viewsets.ReadOnlyModelViewSet):
    queryset = ComponentPost.objects.all()
    serializer_class = ComponentPostSerializer

class SiteRecordListView(APIView):
    def getSiteRecord(self, pk):
        try:
            return SiteRecord.objects.get(hostname=pk)
        except SiteRecord.DoesNotExist:
            return SiteRecord.objects.get(hostname='default')

    def get(self, format=None, pk=None, *args, **kwargs):
        site_record = self.getSiteRecord(pk)
    
        serializer = SiteRecordSerializer(site_record)
        return Response(serializer.data)

class AddComponentView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def getSiteRecord(self, pk):
        try:
            return SiteRecord.objects.get(id=pk)
        except:
            raise Http404

    def convertUrlToImage(self, url):
        try:
            response = requests.get(url, stream=True, timeout=5)
            if (response.status_code != requests.codes.ok):
                return Response(status.HTTP_400_BAD_REQUEST)
            filename = url.split('/')[-1]
            temp_filename = tempfile.NamedTemporaryFile()
            for block in response.iter_content(1024*8):
                if not block:
                    break

                temp_filename.write(block)
            f = files.File(temp_filename).open()
            file = ImageFile(f, filename[-100:])

            return file
        except:
            return Response(status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, format=None):
        uploadedByUser = False
        site_records = self.getSiteRecord(request.data['site_records'])

        if (type(request.data['media_url']) == str):
            media_url = self.convertUrlToImage(request.data['media_url'])
        else:
            media_url = request.data['media_url']
            uploadedByUser = True

        componentData = {
            'media_url': media_url,
            'page_url': request.data['page_url'],
        }

        query_dict = QueryDict('', mutable=True)
        query_dict.update(componentData)

        serializer = ComponentPostSerializer(data=query_dict)
        if serializer.is_valid():
            if uploadedByUser:
                serializer.save(site_records = site_records)
                
                # try:
                #     file = media_url
                #     o_file = default_storage.save(f'original/component_pictures/{file}', file)
                # except:
                #     print('an error occured while uploading original image')
                    
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                # page_url = serializer.validated_data['page_url']
                # component_list = ComponentPost.objects.filter(page_url=page_url)
                
                # if not component_list:
                serializer.save(site_records = site_records)
                # else:
                #     component = component_list[0]
                #     serializer = ComponentPostSerializer(component)
                #     return Response(serializer.data, status=status.HTTP_200_OK)

                # try:
                #     file = media_url
                #     o_file = default_storage.save(f'original/component_pictures/{file}', file)
                # except:
                #     print('an error occured while uploading original image')
                    
                media_url.close()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditComponentView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def getSiteRecord(self, pk):
        try:
            return SiteRecord.objects.get(id=pk)
        except:
            raise Http404

    def convertUrlToImage(self, url):
        try:
            response = requests.get(url, stream=True, timeout=5)
            if (response.status_code != requests.codes.ok):
                return Response(status.HTTP_400_BAD_REQUEST)
            filename = url.split('/')[-1]
            temp_filename = tempfile.NamedTemporaryFile()
            for block in response.iter_content(1024*8):
                if not block:
                    break

                temp_filename.write(block)
            f = files.File(temp_filename).open()
            file = ImageFile(f, filename[-100:])

            return file
        except:
            return Response(status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk, format=None):
        uploadedByUser = False
        site_records = self.getSiteRecord(request.data['site_records'])

        if (type(request.data['media_url']) == str):
            media_url = self.convertUrlToImage(request.data['media_url'])
        else:
            media_url = request.data['media_url']
            uploadedByUser = True

        componentData = {
            'media_url': media_url,
            'page_url': request.data['page_url'],
        }

        query_dict = QueryDict('', mutable=True)
        query_dict.update(componentData)

        component_filter = ComponentPost.objects.filter(id=pk)
        component = get_object_or_404(component_filter)

        serializer = ComponentPostSerializer(component, data=query_dict)
        if serializer.is_valid():
            if uploadedByUser:
                serializer.save(site_records = site_records)
                # try:
                #     file = request.data['media_url']
                #     o_file = default_storage.save(f'original/component_pictures/{file}', file)
                # except:
                #     print('error occured while uploading original image/video')
                
                    
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                # page_url = serializer.validated_data['page_url']
                # component_list = ComponentPost.objects.filter(page_url=page_url)
                
                # if not component_list:
                serializer.save(site_records = site_records)
                # else:
                #     component = component_list[0]
                #     serializer = ComponentPostSerializer(component)
                #     return Response(serializer.data, status=status.HTTP_200_OK)

                media_url.close()
                # if(request.data['media_url']):
                #     file = request.data['media_url']
                #     o_file = default_storage.save(f'original/component_pictures/{file}', file)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)