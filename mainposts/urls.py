from django.urls import path, include
from rest_framework.routers import DefaultRouter
from mainposts.views import MainPostViewset, SendEmailView, MainPostCategoryView, MainPostChoicesView, MainPostCategoryDetailsView, MainPostPhotoOfDetailsView

router = DefaultRouter()
router.register(r'', MainPostViewset)

urlpatterns = [
    path('categorychoice/', MainPostChoicesView.as_view()),
    path('sendemail/', SendEmailView.as_view()),
    path('category/<pk>/', MainPostCategoryView.as_view()),
    path('category/<category>/<pk>/', MainPostCategoryDetailsView.as_view()),
    path('photoof/<category>/<pk>/', MainPostPhotoOfDetailsView.as_view()),
    path('', include(router.urls)),
]
