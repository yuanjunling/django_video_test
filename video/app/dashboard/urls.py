# conding:utf-8

from django.urls import path
from .views.base import Index
from .views.auth import Login,AdminManger,Logout,UpdateAdminStatus
from .views.video import ExternalVideo,VideoSubView,VideoStarView


urlpatterns = [
    path('',Index.as_view(),name='dashboard_index'),
    path('login/',Login.as_view(),name='login'),
    path('admin/manger',AdminManger.as_view(),name='admin_manger'),
    path('logout',Logout.as_view(),name='logout'),
    path('admin/manger/update/status/<int:user_id>',UpdateAdminStatus.as_view(),name='admin_update_status'),
    path('video/externa',ExternalVideo.as_view(),name='externa_video'),
    path('video/videosub/<int:video_id>',VideoSubView.as_view(),name='video_sub'),
    path('video/Star',VideoStarView.as_view(),name='video_star')
]
