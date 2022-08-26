from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from users.views import (
    FacebookLogin, 
    KnoxRegisterView, 
    KnoxLoginView, 
    SearchUserView, 
    UserPostView, 
    UserInfoUpdateView, 
    UserDetailsView, 
    WishlistViews, 
    ChangeUsernameView, 
    UserComponentView, 
    LoginAsUser, 
    UserAPIView,
    UserViewset,
    InstagramLogin
)
from dj_rest_auth.views import PasswordResetConfirmView


router = DefaultRouter()
router.register(r'', UserViewset)


urlpatterns = [
    path('auth/login/', KnoxLoginView.as_view(), name='knox_login'),
    path('auth/knox/', include('knox.urls')),  #for logout
    path(
        'auth/registration/',
        KnoxRegisterView.as_view(),
        name='knox_register'
    ),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
    path('auth/instagram/', InstagramLogin.as_view(), name='insta_login'),
    path(
        'password/reset/confirm/<uidb64>/<token>',
        PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    re_path(
        r'^social/accounts/',
        include('allauth.urls'),
        name='socialaccount_signup'
    ),
    path('mainposts/paginated/<pk>/', UserPostView.as_view()),
    path('userinfo/<pk>/', UserInfoUpdateView.as_view()),
    path('userdetails/<pk>/', UserDetailsView.as_view()),
    path('wishlist/<pk>/', WishlistViews.as_view()),
    path('mycomponents/<pk>/', UserComponentView.as_view()),
    path('changeusername/<pk>/', ChangeUsernameView.as_view()),
    path('admin/loginwithusername/<pk>/', LoginAsUser.as_view()),
    path('getusers/', UserAPIView.as_view()),
    path('search/', SearchUserView.as_view()),
    path('', include(router.urls)),
]
