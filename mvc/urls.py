from django.conf.urls import url
from mvc import views

urlpatterns = [
    url(r'^$', views.index),        # 主页
    url(r'^signup/$', views.signup),         # 注册
    url(r'^signin/$', views.signin),         # 登录
    url(r'^signout/$', views.signout),        # 退出登录
    url(r'^user/$', views.index_user_self),     # 我的空间，需要改进,最后转到了views.index_user
    url(r'^users/$', views.users_index),        # 网友们
    url(r'^settings/$', views.settings, name='tmitter_mvc_views_settings'),     # 个人中心设置
    url(r'^user/(?P<_username>[a-zA-Z\-_\d\u4E00-\u9FA5]+)/$', views.index_user, name="tmitter-mvc-views-index_user"),         # 已登录用户信息首页
    url(r'^friend/add/(?P<_username>[a-zA-Z\-_\d\u4E00-\u9FA5]+)', views.friend_add, name="tmitter-mvc-views-friend_add"),       # 已登录用户信息,添加好友
    url(r'^friend/remove/(?P<_username>[a-zA-Z\-_\d\u4E00-\u9FA5]+)', views.friend_remove, name='tmitter-mvc-views-friend_remove'),       # 已登录信息，删除好友

    url(r'^friend/chat/(?P<_username>[a-zA-Z\-_\d\u4E00-\u9FA5]+)', views.friend_chat, name="tmitter-mvc-views-friend_chat"),   # chat

    url(r'^message/(?P<_id>\d+)/$', views.detail, name="tmitter-mvc-views-detail"),     # 发布的空间信息详情
    url(r'^message/(?P<_id>\d+)/delete/$', views.detail_delete, name="tmitter-mvc-views-detail_delete"),        # 删除空间消息
    url(r'^user/(?P<_username>[a-zA-Z\-_\d\u4E00-\u9FA5]+)/(?P<_page_index>\d+)/$', views.index_user_page, name='tmitter.mvc.views.index_user_page'),   # 分页条显示的第几页

]
