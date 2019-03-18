from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

from back.models import User, Article, ArticleType
from utils.functions import is_login

back_blue = Blueprint('back', __name__)


@back_blue.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('back/register.html')
    elif request.method == 'POST':
        # 获取数据
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        if username and password and password2:
            user = User.query.filter(User.username == username).first()
            if user:
                error = '该账号已注册，请更换账号'
                return render_template('back/register.html', error=error)
            else:
                if password2 == password:
                    # 录入数据
                    user = User()
                    user.username = username
                    user.password = generate_password_hash(password)
                    user.save()
                    return redirect(url_for('back.login'))
                else:
                    error = '两次密码不一致'
                    return render_template('back/register.html', error=error)
        else:
            error = '请填写完整的信息'
            return render_template('back/register.html', error=error)


@back_blue.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('back/login.html')
    elif request.method == 'POST':
        # 获取数据
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            user = User.query.filter(User.username == username).first()
            if not user:
                error = '该账号不存在，请去注册'
                return render_template('back/login.html', error=error)
            elif not check_password_hash(user.password, password):
                error = '密码错误，请修改密码'
                return render_template('back/login.html', error=error)
            else:
                # 账号密码匹配正确，跳转首页
                session['user_id'] = user.id
                return redirect(url_for('back.index'))
        else:
            error = '请填写完整的登录信息'
            return render_template('back/login.html', error=error)


@back_blue.route('/index/')
@is_login
def index():
    arts = Article.query.all()
    art_num = 0
    for art in arts:
        if art.us == session['user_id']:
            art_num += 1
    types = ArticleType.query.all()
    type_num = 0
    for type in types:
        if type.us == session['user_id']:
            type_num += 1
    return render_template('back/index.html', arts=arts, types=types, art_num=art_num, type_num=type_num)


@back_blue.route('/logout/', methods=['GET'])
@is_login
def logout():
    del session['user_id']
    return redirect(url_for('back.login'))


@back_blue.route('/articles_category/', methods=['GET', 'POST'])
@is_login
def articles_category():
    if request.method == 'GET':
        types = ArticleType.query.all()
        num = 0
        for type in types:
            if type.us == session['user_id']:
                num += 1
        return render_template('back/articles_category.html', types=types, num=num)


@back_blue.route('/articles_category_add/', methods=['GET', 'POST'])
@is_login
def articles_category_add():
    if request.method == 'GET':
        return render_template('back/articles_category_add.html')
    elif request.method == 'POST':
        art_type = request.form.get('art_type')
        if art_type:
            articletype = ArticleType.query.filter(ArticleType.at_name == art_type).first()
            if articletype:
                error = '该分类已存在'
                return render_template('back/articles_category_add.html', error=error)
            else:
                # 保存分类信息
                articletype = ArticleType()
                articletype.at_name = art_type
                articletype.us = session['user_id']
                articletype.save()
                return redirect(url_for('back.articles_category'))
        else:
            error = '请填写分类信息'
            return render_template('back/articles_category_add.html', error=error)


@back_blue.route('/del_type/<int:id>/', methods=['GET'])
@is_login
def del_type(id):
    # 删除分类
    atype = ArticleType.query.get(id)
    atype.dele()
    return redirect(url_for('back.articles_category'))


@back_blue.route('/articles_list/', methods=['GET'])
@is_login
def articles_list():
    arts = Article.query.all()
    num = 0
    for art in arts:
        if art.us == session['user_id']:
            num += 1
    return render_template('back/articles_list.html', arts=arts, num=num)


@back_blue.route('/articles_list_add/', methods=['GET', 'POST'])
@is_login
def articles_list_add():
    if request.method == 'GET':
        types = ArticleType.query.all()
        return render_template('back/articles_list_add.html', types=types)
    elif request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('desc')
        content = request.form.get('content')
        type = request.form.get('category')
        us = session['user_id']
        if title and desc and content and type:
            # 保存
            art = Article()
            art.title = title
            art.desc = desc
            art.content = content
            art.type = type
            art.us = us
            art.save()
            return redirect(url_for('back.articles_list'))
        else:
            error = '请填写完整的文章信息'
            types = ArticleType.query.all()
            return render_template('back/articles_list_add.html', error=error, types=types)


@back_blue.route('/del_art/<int:id>/', methods=['GET'])
@is_login
def del_art(id):
    # 删除文章
    article = Article.query.get(id)
    article.dele()
    return redirect(url_for('back.articles_list'))


@back_blue.route('/alter_art/<int:id>/', methods=['GET', 'POST'])
@is_login
def alter_art(id):
    article = Article.query.get(id)
    types = ArticleType.query.all()
    if request.method == 'GET':
        # 修改文章
        return render_template('/back/articles_list_alter.html', article=article, types=types)
    elif request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('desc')
        content = request.form.get('content')
        type = request.form.get('category')
        us = session['user_id']
        if title and desc and content and type:
            # 保存
            article.title = title
            article.desc = desc
            article.content = content
            article.type = type
            article.us = us
            article.save()
            return redirect(url_for('back.articles_list'))
        else:
            error = '请填写完整的文章信息'
            return render_template('back/articles_list_alter.html', error=error, article=article, types=types)


@back_blue.route('user_settings', methods=['GET', 'POST'])
@is_login
def user_settings():
    if request.method == 'GET':
        return render_template('back/user_settings.html')
    elif request.method == 'POST':
        return redirect(url_for('back.index'))


@back_blue.route('change_password', methods=['GET', 'POST'])
@is_login
def change_password():
    if request.method == 'GET':
        return render_template('back/change_password.html')
    elif request.method == 'POST':
        password = request.form.get('password')
        con_password = request.form.get('con_password')
        if password and con_password:
            return redirect(url_for('back.index'))
        else:
            error = '请填写完整的密码信息'
            return render_template('back/change_password.html', error=error)
