from . import admin_blueprint
from flask import render_template, url_for, redirect, flash, session, request, current_app
from app.admin.forms import LoginForm, TagForm, MovieForm, PreviewForm
from app.models import Admin, Tag, Movie, Preview, User
from functools import wraps
from app import db
from werkzeug.utils import secure_filename
import os
import uuid
import datetime


# 定义访问控制装饰器
def admin_login_req(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'admin' not in session:
            return redirect(url_for('admin_blueprint.login'))
        return f(*args, **kwargs)

    return wrapper


# 生成文件名称
def change_filename(filename):
    fileinfo = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + \
        str(uuid.uuid4().hex) + fileinfo[-1]
    return filename


@admin_blueprint.route('/')
@admin_login_req
def index():
    return render_template('admin/index.html')


# 登录
@admin_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    loginForm = LoginForm()
    if loginForm.validate_on_submit():
        data = loginForm.data
        admin = Admin.query.filter_by(name=data['account']).first()
        if not admin.check_pwd(data['pwd']):  # 如果密码不正确
            flash('密码错误')
            return redirect(url_for('admin_blueprint.login'))
        session['admin'] = data['account']
        return redirect(request.args.get('next') or url_for('admin_blueprint.index'))
    return render_template('admin/login.html', loginForm=loginForm)


# 退出
@admin_blueprint.route('/loginout')
@admin_login_req
def loginout():
    session.pop('admin', None)
    return redirect(url_for('admin_blueprint.login'))


# 修改密码
@admin_blueprint.route('/pwd')
@admin_login_req
def pwd():
    return render_template('admin/pwd.html')


# 标签添加
@admin_blueprint.route('/tag/add', methods=['POST', 'GET'])
@admin_login_req
def tag_add():
    tagForm = TagForm()
    if tagForm.validate_on_submit():
        data = tagForm.name.data
        tag = Tag.query.filter_by(name=data).count()
        if tag == 1:
            flash('标签名称已存在！', 'err')
            return redirect(url_for('admin_blueprint.tag_add'))
        tag = Tag(name=data)
        db.session.add(tag)
        db.session.commit()
        flash('添加标签成功', 'success')

    return render_template('admin/tag_add.html', tagForm=tagForm)


# 标签浏览
@admin_blueprint.route('/tag/list/<int:page>')
@admin_login_req
def tag_list(page=None):
    if page is None:
        page = 1
    page_data = Tag.query.order_by(Tag.addtime.desc()).paginate(
        page=page, per_page=10)  # 分页显示
    return render_template('admin/tag_list.html', page_data=page_data)


# 标签删除
@admin_blueprint.route('/tag/del/<int:id>', methods=['GET'])
@admin_login_req
def tag_del(id):
    tag = Tag.query.filter_by(id=id).first_or_404()
    db.session.delete(tag)
    db.session.commit()
    flash('删除成功', 'success')
    return redirect(url_for('admin_blueprint.tag_list', page=1))


# 标签编辑
@admin_blueprint.route('/tag/edit/<int:id>', methods=['POST', 'GET'])
@admin_login_req
def tag_edit(id):
    tagForm = TagForm()
    tag = Tag.query.filter_by(id=id).first_or_404()
    if tagForm.validate_on_submit():
        data = tagForm.data
        tagcount = Tag.query.filter_by(name=data['name']).count()
        if tagcount == 1:
            flash('该名称已存在！', 'err')
            return redirect(url_for('admin_blueprint.tag_edit', id=id))
        tag.name = data['name']
        db.session.add(tag)
        db.session.commit()
        flash('修改成功', 'success')
        return redirect(url_for('admin_blueprint.tag_edit', id=id))
    return render_template('admin/tag_edit.html', tagForm=tagForm, tag=tag)


# 电影添加
@admin_blueprint.route('/movie/add', methods=['POST', 'GET'])
@admin_login_req
def movie_add():
    movieform = MovieForm()
    if movieform.validate_on_submit():
        data = movieform.data
        file_url = secure_filename(movieform.url.data.filename)
        file_logo = secure_filename(movieform.logo.data.filename)
        if not os.path.exists(current_app.config['UP_DIR']):
            os.mkdir(current_app.config['UP_DIR'])
            os.chmod(current_app.config['UP_DIR'], 'rw')
        url = change_filename(file_url)
        logo = change_filename(file_logo)
        movieform.url.data.save(current_app.config['UP_DIR'] + url)
        movieform.logo.data.save(current_app.config['UP_DIR'] + logo)
        movie = Movie(
            title=data['title'],
            url=url,
            info=data['info'],
            logo=logo,
            star=int(data['star']),
            playnum=0,
            commentnum=0,
            tag_id=int(data['tag_id']),
            area=data['area'],
            release_time=data['release_time'],
            length=data['length']
        )
        db.session.add(movie)
        db.session.commit()
        flash('添加电影成功', 'success')
        return redirect(url_for('admin_blueprint.movie_add'))
    return render_template('admin/movie_add.html', movieform=movieform)


# 电影列表
@admin_blueprint.route('/movie/list/<int:page>', methods=['POST', 'GET'])
@admin_login_req
def movie_list(page):
    movie_list = Movie.query.join(Tag).order_by(
        Movie.addtime.desc()).paginate(page=page, per_page=10)
    return render_template('admin/movie_list.html', page_data=movie_list)


# 电影编辑
@admin_blueprint.route('/movie/edit/<int:id>', methods=['POST', 'GET'])
@admin_login_req
def movie_edit(id):
    movieform = MovieForm()
    movieform.url.validators = []
    movieform.logo.validators = []
    movie = Movie.query.filter_by(id=id).first_or_404()
    if request.method == 'GET':
        movieform.info.data = movie.info
        movieform.tag_id.data = movie.tag_id
        movieform.star.data = movie.star
    if movieform.validate_on_submit():
        # data = movieform.data
        movie_count = Movie.query.filter_by(title=movieform.title.data).count()
        if movie_count == 1:
            flash('该片名已存在', 'err')
            return redirect(url_for('admin_blueprint.movie_edit', id=id))

        if not os.path.exists(current_app.config['UP_DIR']):
            os.mkdir(current_app.config['UP_DIR'])
            os.chmod(current_app.config['UP_DIR'], 'rw')

        if movieform.url.data.filename != "":
            file_url = secure_filename(movieform.url.data.filename)
            movie.url = change_filename(file_url)
            movieform.url.data.save(current_app.config['UP_DIR'] + movie.url)

        if movieform.logo.data.filename != "":
            file_logo = secure_filename(movieform.logo.data.filename)
            movie.logo = change_filename(file_logo)
            movieform.logo.data.save(current_app.config['UP_DIR'] + movie.logo)

        movie.star = movieform.star.data
        movie.tag_id = movieform.tag_id.data
        movie.info = movieform.info.data
        movie.title = movieform.title
        movie.area = movieform.area
        movie.length = movieform.length.data
        movie.release_time = movieform.release_time.data
        db.session.add(movie)
        db.session.commit()
        flash('修改电影成功', 'success')
        return redirect(url_for('admin_blueprint.movie_edit', id=id))
    return render_template('admin/movie_edit.html', movieform=movieform, movie=movie)


# 删除电影
@admin_blueprint.route('/movie/del/<int:id>', methods=['POST', 'GET'])
@admin_login_req
def movie_del(id):
    movie = Movie.query.filter_by(id=id).first_or_404()
    db.session.delete(movie)
    db.session.commit()
    flash('删除电影成功', 'success')
    return redirect(url_for('admin_blueprint.movie_list', page=1))


# 上映预告添加
@admin_blueprint.route('/preview/add', methods=['GET', 'POST'])
@admin_login_req
def preview_add():
    previewform = PreviewForm()
    if previewform.validate_on_submit():
        title = previewform.title.data
        file_logo = secure_filename(previewform.logo.data.filename)
        if not os.path.exists(current_app.config['UP_DIR']):
            os.mkdir(current_app.config['UP_DIR'])
            os.chmod(current_app.config['UP_DIR'], 'rw')
        logo = change_filename(file_logo)
        previewform.logo.data.save(current_app.config['UP_DIR'] + logo)
        preview = Preview(
            title=title,
            logo=logo
        )
        db.session.add(preview)
        db.session.commit()
        flash('保存成功', 'success')
        return redirect(url_for('admin_blueprint.preview_add'))
    return render_template('admin/preview_add.html', previewform=previewform)


# 上映预告列表
@admin_blueprint.route('/preview/list/<int:page>', methods=['GET'])
@admin_login_req
def preview_list(page=None):
    if page is None:
        page = 1

    page_data = Preview.query.order_by(
        Preview.addtime.desc()).paginate(page=page, per_page=10)
    return render_template('admin/preview_list.html', page_data=page_data)

# 预告删除


@admin_blueprint.route('/preview/del/<int:id>', methods=['GET', 'POST'])
def preview_del(id):
    preview = Preview.query.filter_by(id=id).first_or_404()
    db.session.delete(preview)
    db.session.commit()
    flash('删除成功', 'success')
    return redirect(url_for('admin_blueprint.preview_list', page=1))

# 预告编辑


@admin_blueprint.route('/preview/edit/<int:id>', methods=['POST', 'GET'])
@admin_login_req
def preview_edit(id):
    previewform = PreviewForm()
    previewform.logo.validators = []
    preview = Preview.query.filter_by(id=int(id)).first_or_404()
    if request.method == 'GET':
        previewform.title.data = preview.title

    if previewform.validate_on_submit():
        if previewform.logo.data.filename != "":
            file_logo = secure_filename(previewform.logo.data.filename)
            preview.logo = change_filename(file_logo)
            previewform.logo.data.save(
                current_app.config['UP_DIR'] + preview.logo)

        preview.title = previewform.title.data
        db.session.add(preview)
        db.session.commit()
        flash('编辑成功', 'success')
        return redirect(url_for('admin_blueprint.preview_edit', id=id))
    return render_template("admin/preview_edit.html", previewform=previewform, preview=preview)


# 用户列表
@admin_blueprint.route('/user/list/<int:page>', methods=['GET'])
@admin_login_req
def user_list(page):
    page_date = User.query.order_by(
        User.addtime.desc()).paginate(page=page, per_page=10)
    return render_template('admin/user_list.html', page_data=page_date)


# 用户查看
@admin_blueprint.route('/user/view/<int:id>', methods=['GET'])
@admin_login_req
def user_view(id=None):
    user = User.query.filter_by(id=int(id)).first_or_404()
    return render_template('admin/user_view.html', user=user)


@admin_blueprint.route('/user/del/<int:id>', methods=['GET'])
@admin_login_req
def user_del(id=None):
    user = User.query.filter_by(id=int(id)).first_or_404()
    db.session.delete(user)
    db.commit()
    flash('删除成功', 'success')
    return redirect(url_for('admin_blueprint.user_list', page=1)) 


# 评论列表
@admin_blueprint.route('/comment/list')
@admin_login_req
def comment_list():
    return render_template('admin/comment_list.html')


# 电影收藏
@admin_blueprint.route('/moviecol/list')
@admin_login_req
def moviecol_list():
    return render_template('admin/moviecol_list.html')


# 操作日志
@admin_blueprint.route('/oplog/list')
@admin_login_req
def oplog_list():
    return render_template('admin/oplog_list.html')


# 管理员登录日志
@admin_blueprint.route('/oplog/adminloginlog')
@admin_login_req
def oplog_adminloginlog():
    return render_template('admin/oplog_adminloginlog.html')


# 会员登录日志
@admin_blueprint.route('/oplog/userloginlog')
@admin_login_req
def oplog_userloginlog():
    return render_template('admin/oplog_userloginlog.html')


# 角色添加
@admin_blueprint.route('/role/add')
@admin_login_req
def role_add():
    return render_template('admin/role_add.html')


# 角色列表
@admin_blueprint.route('/role/list')
@admin_login_req
def role_list():
    return render_template('admin/role_list.html')


# 权限添加
@admin_blueprint.route('/auth/add')
@admin_login_req
def auth_add():
    return render_template('admin/auth_add.html')


# 权限列表
@admin_blueprint.route('/auth/list')
@admin_login_req
def auth_list():
    return render_template('admin/auth_list.html')


# 管理员添加
@admin_blueprint.route('/admin/add')
@admin_login_req
def admin_add():
    return render_template('admin/admin_add.html')


# 管理员列表
@admin_blueprint.route('/admin/list')
@admin_login_req
def admin_list():
    return render_template('admin/admin_list.html')
