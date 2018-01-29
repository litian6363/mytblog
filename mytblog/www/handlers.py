#!usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio, time, re, hashlib, json, logging, markdown2
from coroweb import get, post
from models import User, Comment, Blog, next_id
from apis import APIValueError, APIResourceNotFoundError, APIError, APIPermissionError, Page
from aiohttp import web
from config import configs


COOKIE_NAME = 'awesession'  # 用来在set_cookie中命名
_COOKIE_KEY = configs['session']['secret']  # 导入默认设置


# 制作cookie的数值，即set_cookie的value
def user2cookie(user, max_age):
    # build cookie string by: id-expires-sha1（id-到期时间-sha1）
    expires = str(time.time()+max_age)
    s = '%s-%s-%s-%s' % (user.id, user.password, expires, _COOKIE_KEY)  # s的组成：id, password, expires, _COOKIE_KEY
    l = [user.id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]  # 再把s进行摘要算法
    return '-'.join(l)


# 解析cookie
async def cookie2user(cookie_str):
    """
    Parse cookie and load user if cookie is valid.
    """
    if not cookie_str:
        return None
    try:
        l = cookie_str.split('-')
        if len(l) != 3:
            return None
        uid, expires, sha1 = l
        if int(float(expires)) < time.time():
            return None
        user = await User.find(uid)
        if user is None:
            return None
        s = '%s-%s-%s-%s' % (uid, user.password, expires, _COOKIE_KEY)
        if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
            logging.info('invalid sha1')
            return None
        user.password = '******'
        return user
    except Exception as e:
        logging.exception(e)
        return None


# 用于选择当前页面
def get_page_index(page_str):
    p = 1  # 初始化页数取整
    try:
        p = int(page_str)
    except ValueError as e:
        pass
    if p < 1:
        p = 1
    return p


# r'(^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$)'
_re_email = re.compile(r'^(\w)+(\.\w)*@(\w)+((\.\w{2,3}){1,3})$')
_re_sha1 = re.compile(r'^[\w.]{40}')


# 编写URL处理函数
# 主页处理函数
@get('/')
async def index(*, page='1'):
    page_index = get_page_index(page)
    num = await Blog.find_number('count(id)')
    page = Page(num, page_index)
    if num == 0:
        blogs = []
    else:
        blogs = await Blog.find_all(orderBy='created_at desc', limit=(page.offset, page.limit))
    return {
        '__template__': 'blogs.html',
        'page': page,
        'blogs': blogs
    }


# 显示博客内容
@get('/blog/{id}')
async def get_blog(id):
    blog = await Blog.find(id)
    comments = await Comment.find_all('blog_id=?', [id], orderBy='created_at desc')
    for c in comments:
        c.html_content = text2html(c.content)
    blog.html_content = markdown2.markdown(blog.content)
    return {
        '__template__': 'blog.html',
        'blog': blog,
        'comments': comments
    }


# 显示注册页面
@get('/register')
def register():
    return {
        '__template__': 'register.html'
    }


# 显示登录页面
@get('/signin')
def signin():
    return {
        '__template__': 'signin.html'
    }


# 用户登录API
@post('/api/authenticate')
async def authenticate(*, email, password):
    if not email:
        raise APIValueError('email', 'Invalid email')
    if not password:
        raise APIValueError('password', 'Invalid password')
    users = await User.find_all('email=?', [email])
    if len(users) == 0:
        raise APIValueError('email', 'Email not exist.')
    user = users[0]
    # 检查密码
    sha1 = hashlib.sha1()
    sha1.update(user.id.encode('utf-8'))
    sha1.update(b':')
    sha1.update(password.encode('utf-8'))
    if sha1.hexdigest() != user.password:
        raise APIValueError('password', 'Invalid password')
    # session cookie:
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.password = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r


# 用户登出
@get('/signout')
def signout(request):
    referer = request.headers.get('Referer')
    r = web.HTTPFound(referer or '/')
    r.set_cookie(COOKIE_NAME, '-deleted-', max_age=0, httponly=True)
    logging.info('user signed out.')
    return r


# 管理主页
@get('/manage/')
def manage():
    return 'redirect:/manage/comments'


# 评论管理
@get('/manage/comments')
def manage_comments(*, page='1'):
    return {
        '__template__': 'manage_comments.html',
        'page_index': get_page_index(page)
    }


# 显示博客创建页面
@get('/manage/blogs/create')
def manage_create_blog():
    return {
        '__template__': 'manage_blog_edit.html',
        'id': '',
        'action': '/api/blogs'
    }


# 博客修改页面
@get('/manage/blogs/edit')
def manage_edit_blog(*, id):
    return {
        '__template__': 'manage_blog_edit.html',
        'id': id,
        'action': '/api/blogs/%s' % id
    }


# 显示博客管理页面
@get('/manage/blogs')
def manage_blogs(*, page='1'):
    return {
        '__template__': 'manage_blogs.html',
        'page_index': get_page_index(page)
    }


# 用户管理页面
@get('/manage/users')
def manage_users(*, page='1'):
    return {
        '__template__': 'manage_users.html',
        'page_index': get_page_index(page)
    }


# 获取评论API
@get('/api/comments')
async def api_comments(*, page='1'):
    page_index = get_page_index(page)
    num = await Comment.find_number('count(id)')
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p, comments=())
    comments = await Comment.find_all(orderBy='created_at desc', limit=(p.offset, p.limit))
    return dict(page=p, comments=comments)


# 创建评论API
@post('/api/blogs/{id}/comments')
async def api_create_comment(id, request, *, content):
    user = request.__user__
    if user is None:
        raise APIPermissionError('Please signin first.')
    if not content or not content.strip():
        raise APIValueError('content')
    blog = await Blog.find(id)
    if blog is None:
        raise APIResourceNotFoundError('Blog')
    comment = Comment(blog_id=blog.id, user_id=user.id, user_name=user.name, user_image=user.image, content=content.strip())
    await comment.save()
    return comment


# 评论删除API
@post('/api/comments/{id}/delete')
async def api_delete_comments(id, request):
    check_admin(request)
    c = await Comment.find(id)
    if c is None:
        raise APIResourceNotFoundError('Comment')
    await c.remove()
    return dict(id=id)


# 获取用户数据API
@get('/api/users')
async def api_get_users(*, page='1'):
    page_index = get_page_index(page)
    num = await User.find_number('count(id)')
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p, users=())
    users = await User.find_all(orderBy='created_at desc', limit=(p.offset, p.limit))
    for u in users:
        u.password = '******'
    return dict(page=p, users=users)


# 用户注册API
@post('/api/users')
async def api_register_user(*, email, name, password):
    # 排除错误
    if not name or not name.strip():
        raise APIValueError('name')
    if not email or not _re_email.match(email):
        raise APIValueError('email')
    if not password or not _re_sha1.match(password):
        raise APIValueError('password')
    users = await User.find_all('email=?', [email])
    if len(users) > 0:
        raise APIError('register:failed', 'email', 'Email is already in use.')
    # 准备要保存的用户资料
    uid = next_id()
    sha1_password = '%s:%s' % (uid, password)
    last_password = hashlib.sha1(sha1_password.encode('utf-8')).hexdigest()
    last_image = 'http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email.encode('utf-8')).hexdigest()
    user = User(id=uid, name=name.strip(), email=email, password=last_password, image=last_image)
    # 保存进数据库
    await user.save()
    # session cookie:
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.password = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r


# 检查是否登录和是否管理员
def check_admin(request):
    if request.__user__ is None or not request.__user__.admin:
        raise APIPermissionError()


# 创建blog
@post('/api/blogs')
async def api_create_blog(request, *, name, summary, content):
    check_admin(request)
    if not name or not name.strip():
        raise APIValueError('name', 'name cannot be empty.')
    if not summary or not summary.strip():
        raise APIValueError('summary', 'summary cannot be empty.')
    if not content or not content.strip():
        raise APIValueError('content', 'content cannot be empty.')
    blog = Blog(id=next_id(), user_id=request.__user__.id, user_name=request.__user__.name, user_image=request.__user__.image,
                name=name.strip(), summary=summary.strip(), content=content.strip())
    await blog.save()
    return blog


# 接口用于数据库返回日志,见manage_blogs.html
@get('/api/blogs')
async def api_blogs(*, page='1'):
    page_index = get_page_index(page)
    num = await Blog.find_number('count(id)')  # 查询日志总数
    p = Page(num, page_index)
    if num == 0:  # 数据库没日志
        return dict(page=p, blogs=())
    blogs = await Blog.find_all(orderBy='create_at desc', limit=(p.offset, p.limit))  # 选取对应的日志
    return dict(page=p, blogs=blogs)  # 返回管理页面信息，及显示日志数


def text2html(text):
    lines = map(lambda s: '<p>%s</p>' % s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'), filter(lambda s: s.strip() != '', text.split('\n')))
    return ''.join(lines)


# 获取博客API
@get('/api/blogs/{id}')
async def api_get_blog(*, id):
    blog = await Blog.find(id)
    return blog


# 更新博客API
@post('/api/blogs/{id}')
async def api_update_blog(id, request, *, name, summary, content):
    check_admin(request)
    blog = await Blog.find(id)
    if not name or not name.strip():
        raise APIValueError('name', 'name cannot be empty.')
    if not summary or not summary.strip():
        raise APIValueError('summary', 'summary cannot be empty.')
    if not content or not content.strip():
        raise APIValueError('content', 'content cannot be empty.')
    blog.name = name.strip()
    blog.summary = summary.strip()
    blog.content = content.strip()
    await blog.update()
    return blog


# 删除博客API
@post('/api/blogs/{id}/delete')
async def api_delete_blog(request, *, id):
    check_admin(request)
    blog = await Blog.find(id)
    await blog.remove()
    return dict(id=id)
