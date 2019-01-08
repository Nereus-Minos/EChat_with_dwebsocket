from django.conf.urls import url
from mvc import views

urlpatterns = [
    url(r'^$', views.index),        # 主页
    url(r'^signup/$', views.signup),         # 注册
    url(r'^signin/$', views.signin),         # 登录
    url(r'^signout/$', views.signout),        # 退出登录
    url(r'^friends_list/$', views.friends_list),     # 我的朋友
    url(r'^users/$', views.users_index),        # 网友们
    url(r'^settings/$', views.settings, name='tmitter_mvc_views_settings'),     # 个人中心设置
    url(r'^user/(?P<_username>[a-zA-Z\-_\d\u4E00-\u9FA5]+)/$', views.index_user, name="tmitter-mvc-views-index_user"),         # 用户微说信息首页
    url(r'^friend/add/(?P<_username>[a-zA-Z\-_\d\u4E00-\u9FA5]+)', views.friend_add, name="tmitter-mvc-views-friend_add"),       # 已登录用户信息,添加好友
    url(r'^friend/remove/(?P<_username>[a-zA-Z\-_\d\u4E00-\u9FA5]+)', views.friend_remove, name='tmitter-mvc-views-friend_remove'),       # 已登录信息，删除好友

    url(r'^friend/chat/(?P<_username>[a-zA-Z\-_\d\u4E00-\u9FA5]+)', views.friend_chat, name="tmitter-mvc-views-friend_chat"),   # chat

    url(r'^write_blog/(?P<_username>[a-zA-Z\-_\d\u4E00-\u9FA5]+)/$', views.write_blog, name="tmitter-mvc-views-write_blog"),  # 写微说
    url(r'^write_blog/$', views.write_blog),      # 写微说
    url(r'^handle_write_blog/$', views.handle_write_blog),      # 处理写微说函数
    url(r'^upload_img/$', views.upload_img, name='upload_img'),      # 富文本编辑框

    url(r'^message/(?P<_id>\d+)/$', views.detail, name="tmitter-mvc-views-detail"),     # 发布的空间信息详情
    url(r'^message/(?P<_id>\d+)/delete/$', views.detail_delete, name="tmitter-mvc-views-detail_delete"),        # 删除空间消息

    url(r'^user/(?P<_username>[a-zA-Z\-_\d\u4E00-\u9FA5]+)/(?P<_page_index>\d+)/$', views.index_user_page, name='tmitter.mvc.views.index_user_page'),   # 各用户的blog分页条显示的第几页
    url(r'^home/(?P<_page_index>\d+)/$', views.index_page, name='tmitter.mvc.views.index_page'),   # 首页blog分页条显示的第几页
    url(r'^users/(?P<_page_index>\d+)/$', views.users_list, name='tmitter.mvc.views.users_list'),  # 所有用户分页条显示的第几页
    url(r'^friends_list/(?P<_page_index>\d+)/$', views.friends_list, name='tmitter.mvc.views.friends_list'),  # 我的好友分页

    url(r'searching/$', views.searching, name='tmitter.mvc.views.searching'),    # 搜索函数
    url(r'searching_handle/$', views.searching_handle),    # 处理搜索函数
]
