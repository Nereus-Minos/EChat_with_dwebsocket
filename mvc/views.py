# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from mvc.models import Note, User, Category, Area

from django.utils.translation import ugettext as _
from django.template import Context, loader

from tmitter.settings import *
from utils import mailer, formatter, function, uploader


from django.shortcuts import get_object_or_404

from django.views.decorators.csrf import csrf_exempt

import itertools


# Create your views here.
# home view
@csrf_exempt
def index(request):
    _user_name = ''
    return index_user(request, _user_name)


# user messages view
def index_user(request, _username):
    return index_user_page(request, _username, 1)


def index_page(request, _page_index):
    return index_user_page(request, '', _page_index)


# user messages view and page
def index_user_page(request, _username, _page_index):
    # get user login status
    _islogin = __is_login(request)
    _page_title = _('Home')

    _userid = -1
    # get message list
    _offset_index = (int(_page_index) - 1) * PAGE_SIZE
    _last_item_index = PAGE_SIZE * int(_page_index)

    _login_user_friend_list = None

    if _islogin:
        # get friend messages if user is logined
        _login_user = User.objects.get(username=__user_name(request))
        _login_user_friend_list = _login_user.friend.all()
    else:
        _login_user = None

    _friends = None
    _self_home = False
    if _username != '':
        # there is get user's messages
        _user = get_object_or_404(User, username=_username)
        _userid = _user.id
        _notes = Note.objects.filter(user=_user).order_by('-addtime')
        _page_title = u'%s' % _user.realname
        # get friend list
        # _friends = _user.friend.get_query_set().order_by("id")[0:FRIEND_LIST_MAX]
        _friends = _user.friend.order_by("id")[0:FRIEND_LIST_MAX]
        print("................" % _friends)
        if (_userid == __user_id(request)):
            _self_home = True

    else:
        # get all messages
        _user = None
        #
        # if _islogin:
        #     _query_users = [_login_user]
        #     _query_users.extend(_login_user.friend.all())
        #     _notes = Note.objects.filter(user__in=_query_users).order_by('-addtime')
        #
        # else:
        _notes = Note.objects.all().order_by('-addtime')

    # page bar
    _page_bar = formatter.pagebar(_notes, _page_index, _username)

    # get current page
    _notes = _notes[_offset_index:_last_item_index]

    # body content
    _template = loader.get_template('index.html')


    _one_page_num = len(_notes)
    if _one_page_num < 4:
        _one_page_num_list = [i for i in range(4 - _one_page_num)]
    else:
        _one_page_num_list = ''

    _context = {
        'page_title': _page_title,
        'notes': _notes,
        'islogin': _islogin,
        'userid': __user_id(request),
        'self_home': _self_home,
        'user': _user,
        'userself': _login_user,
        'page_bar': _page_bar,
        'friends': _friends,
        'login_user_friend_list': _login_user_friend_list,
        'one_page_num': _one_page_num,
        'one_page_num_list': _one_page_num_list,
    }

    _output = _template.render(_context)

    return HttpResponse(_output)


# return user login status
def __is_login(request):
     return request.session.get('islogin', False)


# get session user id
def __user_id(request):
    return request.session.get('userid',-1)


# get session realname
def __user_name(request):
    return request.session.get('username','')


# 用户注册
@csrf_exempt
def signup(request):
    # check is login
    _islogin = __is_login(request)

    if (_islogin):
        return HttpResponseRedirect('/')

    _userinfo = {
        'username': '',
        'password': '',
        'confirm': '',
        'realname': '',
        'email': '',
    }

    try:
        # get post params
        _userinfo = {
            'username': request.POST['username'],
            'password': request.POST['password'],
            'confirm': request.POST['confirm'],
            'realname': request.POST['realname'],
            'email': request.POST['email'],
        }
        _is_post = True
    except (KeyError):
        _is_post = False

    if (_is_post):
        _state = __do_signup(request, _userinfo)
    else:
        _state = {
            'success': False,
            'message': _('注 册')
        }

    if (_state['success']):
        return __result_message(request, _('注册成功！'), _('你的信息注册成功！'))

    _result = {
        'success': _state['success'],
        'message': _state['message'],
        'form': {
            'username': _userinfo['username'],
            'realname': _userinfo['realname'],
            'email': _userinfo['email'],
        }
    }

    # body content
    _template = loader.get_template('signup.html')
    _context = {
        'page_title': _('注册'),
        'state': _result,
    }
    _output = _template.render(_context)
    return HttpResponse(_output)


# post signup data
def __do_signup(request, _userinfo):
    _state = {
        'success': False,
        'message': '',
    }

    # check username exist
    if (_userinfo['username'] == ''):
        _state['success'] = False
        _state['message'] = _('用户名未输入！')
        return _state

    if (_userinfo['password'] == ''):
        _state['success'] = False
        _state['message'] = _('密码未输入！')
        return _state

    if (_userinfo['realname'] == ''):
        _state['success'] = False
        _state['message'] = _('真实姓名未输入！')
        return _state

    if (_userinfo['email'] == ''):
        _state['success'] = False
        _state['message'] = _('邮箱未输入！')
        return _state

    # check username exist
    if (__check_username_exist(_userinfo['username'])):
        _state['success'] = False
        _state['message'] = _('用户名已经存在！')
        return _state

        # check password & confirm password
    if (_userinfo['password'] != _userinfo['confirm']):
        _state['success'] = False
        _state['message'] = _('确认密码不匹配！')
        return _state

    _user = User(
        username=_userinfo['username'],
        realname=_userinfo['realname'],
        password=_userinfo['password'],
        email=_userinfo['email'],
        area=Area.objects.get(id=1)
    )
    # try:
    _user.save()
    _state['success'] = True
    _state['message'] = _('成功！')
    # except:
    # _state['success'] = False
    # _state['message'] = '程序异常,注册失败.'

    # send regist success mail
    mailer.send_regist_success_mail(_userinfo)

    return _state


# check user was existed
def __check_username_exist(_username):
    _exist = True

    try:
        _user = User.objects.get(username=_username)
        _exist = True
    except (User.DoesNotExist):
        _exist = False

    return _exist


# response result message page
def __result_message(request, _title=_('Message'), _message=_('Unknow error,processing interrupted.'), _go_back_url=''):
    _islogin = __is_login(request)

    if _go_back_url == '':
        _go_back_url = function.get_referer_url(request)

    # body content
    _template = loader.get_template('result_message.html')

    _context = {
        'page_title': _title,
        'message': _message,
        'go_back_url': _go_back_url,
        'islogin': _islogin
    }

    _output = _template.render(_context)

    return HttpResponse(_output)


# signin view
@csrf_exempt
def signin(request):
    # get user login status
    _islogin = __is_login(request)

    try:
        # get post params
        _username = request.POST['username']
        _password = request.POST['password']
        _is_post = True
    except (KeyError):
        _is_post = False

    # check username and password
    if _is_post:
        _state = __do_login(request, _username, _password)

        if _state['success']:
            # return __result_message(request, _('Login successed'), _('You are logied now.'))
            return index(request)
    else:
        _state = {
            'success': False,
            'message': _('请先登录！')
        }

    # body content
    _template = loader.get_template('signin.html')
    _context = {
        'page_title': _('Signin'),
        'state': _state,
    }
    _output = _template.render(_context)
    return HttpResponse(_output)


# do login
def __do_login(request, _username, _password):
    _state = __check_login(_username, _password)
    if _state['success']:
        # save login info to session
        request.session['islogin'] = True
        request.session['userid'] = _state['userid']
        request.session['username'] = _username
        request.session['realname'] = _state['realname']

    return _state


# check username and password
def __check_login(_username, _password):
    _state = {
        'success': True,
        'message': 'none',
        'userid': -1,
        'realname': '',
    }

    try:
        _user = User.objects.get(username=_username)

        # to decide password
        if (_user.password == function.md5_encode(_password)):
            _state['success'] = True
            _state['userid'] = _user.id
            _state['realname'] = _user.realname
        else:
            # password incorrect
            _state['success'] = False
            _state['message'] = _('Password incorrect.')
    except (User.DoesNotExist):
        # user not exist
        _state['success'] = False
        _state['message'] = _('User does not exist.')

    return _state


# add friend
def friend_add(request, _username):
    # check is login
    _islogin = __is_login(request)

    if (not _islogin):
        return HttpResponseRedirect('/signin/')

    _state = {
        "success": False,
        "message": "",
    }

    _user_id = __user_id(request)
    try:
        _user = User.objects.get(id=_user_id)
    except:
        return __result_message(request, _('Sorry'), _('This user dose not exist.'))

    # check friend exist
    try:
        _friend = User.objects.get(username=_username)
        _user.friend.add(_friend)
        return __result_message(request, _('Successed'), _('%s and you are friend now.') % _friend.realname)
    except:
        return __result_message(request, _('Sorry'), _('This user dose not exist.'))


def friend_remove(request, _username):
    """
    summary:
        解除与某人的好友关系
    """
    # check is login
    _islogin = __is_login(request)

    if (not _islogin):
        return HttpResponseRedirect('/signin/')

    _state = {
        "success": False,
        "message": "",
    }

    _user_id = __user_id(request)
    try:
        _user = User.objects.get(id=_user_id)
    except:
        return __result_message(request, _('Sorry'), _('This user dose not exist.'))

    # check friend exist
    try:
        _friend = User.objects.get(username=_username)
        _user.friend.remove(_friend)
        return __result_message(request, _('Successed'), u'Friend "%s" removed.' % _friend.realname)
    except:
        return __result_message(request, _('Undisposed'), u'He/She dose not your friend,undisposed.')


# signout view
@csrf_exempt
def signout(request):
    request.session['islogin'] = False
    request.session['userid'] = -1
    request.session['username'] = ''

    return HttpResponseRedirect('/')


# 个人资料配置
@csrf_exempt
def settings(request):
    # check is login
    _islogin = __is_login(request)

    if (not _islogin):
        return HttpResponseRedirect('/signin/')

    _user_id = __user_id(request)
    try:
        _user = User.objects.get(id=_user_id)
    except:
        return HttpResponseRedirect('/signin/')

    if request.method == "POST":
        # get post params
        _userinfo = {
            'realname': request.POST['realname'],
            'password': request.POST['password'],
            'confirm_password': request.POST['confirm_password'],
            'email': request.POST['email'],
            'face': request.FILES.get('face', None),
            "about": request.POST['about'],
        }
        _is_post = True
    else:
        _is_post = False

    _state = {
        'message': ''
    }

    # save user info
    if _is_post:
        if _userinfo['password'] == _userinfo['confirm_password']:
            _user.realname = _userinfo['realname']
            _user.email = _userinfo['email']
            _user.about = _userinfo['about']
            _file_obj = _userinfo['face']
            if _file_obj:
                _upload_state = uploader.upload_face(_file_obj)
                if _upload_state['success']:
                    _user.face = _upload_state['message']
                else:
                    return __result_message(request, _('Error'), _upload_state['message'])

            if _userinfo['password'] != '':
                _user.password = _userinfo['password']
                _user.save(True)
                _state['message'] = _('保存成功，密码已修改！')
            else:
                _user.save(False)
                _state['message'] = _('保存成功，密码未修改！')
        else:
            _state['message'] = _('密码与确认密码不匹配！')

    # body content
    _template = loader.get_template('settings.html')
    _context = {
        'page_title': _('Profile'),
        'state': _state,
        'islogin': _islogin,
        'user': _user,
    }
    _output = _template.render(_context)
    return HttpResponse(_output)


# all users list
def users_index(request):
    return users_list(request, 1)


# all users list
def users_list(request, _page_index=1):
    # check is login
    _islogin = __is_login(request)

    _page_title = _('Everyone')

    _login_user = None
    _login_user_friend_list = None
    if _islogin:
        try:
            _login_user = User.objects.get(id=__user_id(request))
            _login_user_friend_list = _login_user.friend.all()

            # 使自己排在第一位
            # _users = User.objects.order_by('-addtime').exclude(id=__user_id(request))
            _users = User.objects.order_by('-addtime')
        except:
            _login_user = None

    else:
        _users = User.objects.order_by('-addtime')


    # page bar
    _page_bar = formatter.pagebar(_users, _page_index, '', 'control/userslist_pagebar.html', islogin=_islogin)

    # get message list
    _offset_index = (int(_page_index) - 1) * PAGE_SIZE
    _last_item_index = PAGE_SIZE * int(_page_index)

    # get current page
    _users = _users[_offset_index:_last_item_index]

    # body content
    _template = loader.get_template('users_list.html')

    _one_page_num = len(_users)
    if _one_page_num < 4:
        _one_page_num_list = [i for i in range(4 - _one_page_num)]
    else:
        _one_page_num_list = ''

    _context = {
        'page_title': _page_title,
        'users': _users,
        'userself': _login_user,
        'login_user_friend_list': _login_user_friend_list,
        'islogin': _islogin,
        'userid': __user_id(request),
        'page_bar': _page_bar,
        'one_page_num': _one_page_num,
        'one_page_num_list': _one_page_num_list,
    }

    _output = _template.render(_context)

    return HttpResponse(_output)


# detail view
def detail(request, _id):
    # get user login status
    _islogin = __is_login(request)

    _note = get_object_or_404(Note, id=_id)

    _go_back_url = function.get_referer_url(request)

    # body content
    _template = loader.get_template('detail.html')

    _context = {
        'page_title': _('Message %s') % _id,
        'item': _note,
        'islogin': _islogin,
        'userid': __user_id(request),
        'go_back_url': _go_back_url,
    }

    _output = _template.render(_context)

    return HttpResponse(_output)


def detail_delete(request, _id):
    # get user login status
    _islogin = __is_login(request)

    _note = get_object_or_404(Note, id=_id)

    _message = ""

    try:
        _note.delete()
        _message = _('Message deleted.')
    except:
        _message = _('Delete failed.')

    return __result_message(request, _('Message %s') % _id, _message, _go_back_url='/')


# user messages view by self
# 好友，需要改进
def friends_list(request, _page_index=1):
    # check is login
    _islogin = __is_login(request)

    _page_title = _('Friends')

    _login_user = None
    _login_user_friend_list = None
    if _islogin:
        try:
            _login_user = User.objects.get(id=__user_id(request))
            _login_user_friend_list = _login_user.friend.all()
        except:
            _login_user = None


    # page bar
    _page_bar = formatter.pagebar(_login_user_friend_list, _page_index, '', 'control/friendslist_pagebar.html', islogin=_islogin)

    # get message list
    _offset_index = (int(_page_index) - 1) * PAGE_SIZE
    _last_item_index = PAGE_SIZE * int(_page_index)

    # get current page
    _login_user_friend_list = _login_user_friend_list[_offset_index:_last_item_index]

    # body content
    _template = loader.get_template('friends_list.html')

    _one_page_num = len(_login_user_friend_list)
    if _one_page_num < 4:
        _one_page_num_list = [i for i in range(4 - _one_page_num)]
    else:
        _one_page_num_list = ''

    _context = {
        'page_title': _page_title,
        'userself': _login_user,
        'login_user_friend_list': _login_user_friend_list,
        'islogin': _islogin,
        'userid': __user_id(request),
        'page_bar': _page_bar,
        'friends_list': True,
        'one_page_num': _one_page_num,
        'one_page_num_list': _one_page_num_list,
    }

    _output = _template.render(_context)

    return HttpResponse(_output)


def friend_chat(request, _username):
    _user2friend = 'yes'
    _ischat = True
    _friend_id = User.objects.get(username=_username).id
    _user_id = __user_id(request)
    user_id = _user_id
    _islogin = __is_login(request)

    user_face = str(User.objects.get(id=_user_id).face)
    friend_face = str(User.objects.get(id=_friend_id).face)


    # 先转为字符串拼接后转为数字
    if _user_id >= _friend_id:
        _user2friend = 'no'
        middle = _friend_id
        _friend_id = _user_id
        _user_id = middle
    _id = str(_user2friend) + '_' + str(_user_id) + '_' + str(_friend_id)

    # body content
    _template = loader.get_template('chat2.html')

    _context = {
        'islogin': _islogin,
        'room_name_json': _id,
        'user_id': user_id,
        'username': _username,
        'ischat': _ischat,
        'user_face': user_face,
        'friend_face': friend_face,
    }

    _output = _template.render(_context)

    return HttpResponse(_output)


@csrf_exempt
def handle_write_blog(request):
    # get user login status
    _islogin = __is_login(request)
    try:
        # get post params
        _message = request.POST['message']
        _is_post = True
    except (KeyError):
        _is_post = False

    # check login
    if not _islogin:
        return HttpResponseRedirect('/signin/')

    # save messages
    (_category, _is_added_cate) = Category.objects.get_or_create(name=u'网页')

    try:
        _user = User.objects.get(id=__user_id(request))
    except:
        return HttpResponseRedirect('/signin/')

    _note = Note(message=_message, category=_category, user=_user)
    _note.save()

    return HttpResponseRedirect('/user/' + _user.username)


def write_blog(request, _username=''):
    # check is login
    _islogin = __is_login(request)

    if (not _islogin):
        return HttpResponseRedirect('/signin/')

    ischat = True       # 去掉base页的头部
    # body content
    _template = loader.get_template('postform.html')

    user = User.objects.get(username=__user_name(request))

    _go_back_url = function.get_referer_url(request)

    try:
        search_content = request.path_info.split('/')[2]
    except:
        search_content = ''

    _this_url = request.path_info

    _context = {
        'ischat': ischat,
        'user': user,
        'go_back_url': _go_back_url,
        'search_content': search_content,
        'this_url': _this_url,
    }

    _output = _template.render(_context)

    return HttpResponse(_output)


def searching(request):
    # body content
    _template = loader.get_template('searching.html')

    _go_back_url = function.get_referer_url(request)

    _context = {
        'ischat': True,
        'go_back_url': _go_back_url,
    }

    _output = _template.render(_context)

    return HttpResponse(_output)


@csrf_exempt
def searching_handle(request):
    if 'search_content' in request.POST:
        search_content = request.POST['search_content']
        go_back_url = request.POST['go_back_url']
    else:
        search_content = request.GET['search_content']
        go_back_url = request.GET['go_back_url']

    _islogin = __is_login(request)

    _login_user = None
    _userid = None

    if _islogin:
        _login_user = User.objects.get(username=__user_name(request))
        _userid = _login_user.id


    if search_content == '':
        return __result_message(request, _message=_('请输入搜索内容！'), _go_back_url=go_back_url)

    _searching_user = User.objects.filter(realname__contains=search_content)

    _searching_notes = Note.objects.filter(message__contains=search_content)

    # body content
    _template = loader.get_template('search_result.html')

    _context = {
        'islogin': _islogin,
        'userself': _login_user,
        'userid': _userid,
        'search_content': search_content,
        'searching_user': _searching_user,
        'searching_notes': _searching_notes,
        'go_back_url': go_back_url,
    }

    _output = _template.render(_context)

    return HttpResponse(_output)
