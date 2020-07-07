from . import home_blueprint
from flask import render_template, redirect, url_for


# 登录页面
@home_blueprint.route('/login')
def login():
    return render_template('home/login.html')


# 退出页面
@home_blueprint.route('/loginout')
def loginout():
    return redirect(url_for('home_blueprint.login'))


# 注册页面
@home_blueprint.route('/regist')
def regist():
    return render_template('home/regist.html')


# 会员中心页面
@home_blueprint.route('/user')
def user():
    return render_template('home/user.html')


# 修改密码页面
@home_blueprint.route('/pwd')
def pwd():
    return render_template('home/pwd.html')


# 登录日志
@home_blueprint.route('/loginlog')
def loginlog():
    return render_template('home/loginlog.html')


# 评论
@home_blueprint.route('/comments')
def comments():
    return render_template('home/comments.html')


# 电影收藏
@home_blueprint.route('/movecol')
def movecol():
    return render_template('home/movecol.html')


# 首页
@home_blueprint.route('/')
def index():
    return render_template('home/index.html')


# 动画页
@home_blueprint.route('/animation')
def animation():
    return render_template('home/animation.html')


# 搜索
@home_blueprint.route('/search')
def search():
    return render_template('home/search.html')


# 播放
@home_blueprint.route('/play')
def play():
    return render_template('home/play.html')
