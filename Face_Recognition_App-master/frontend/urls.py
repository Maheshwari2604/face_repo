from django.conf.urls import url, include
from .views import userviewset, register, PollListView, upload , imgviewset
from rest_framework import routers
from rest_framework.routers import DefaultRouter, SimpleRouter
from .api import UserViewSet
from .views import img_check , FileUploadView

router = DefaultRouter()
router.register('api/users', UserViewSet, 'users-list')
router.register('api/upload', imgviewset, 'img')

urlpatterns = [
    #url(r'^api/users/', PollListView.as_view()),
    #url(r'^api/users/(?P<slug>[\w-]+)/$', PollListView.as_view()),
    #url(r'aa/', views.PostList.as_view()),
    #url(r'^<int:pk>/', views.PostDetail.as_view()),
    url(r'^$', register, name='register'),
    url(r'^check$',img_check, name='img_check'),
    url(r'^uploadimg/(?P<filename>[^/]+)$', FileUploadView.as_view()),
    url(r'^upload$', upload, name='upload'),
    #url(r'^user/', userview.as_view()),
]

urlpatterns += router.urls
