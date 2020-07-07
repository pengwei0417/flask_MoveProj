import datetime
from app import db


# ----------会员及会员登录日志数据模型设计--------------
# ------------------------------------------------------
# 定义会员数据模型
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.BIGINT, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 昵称
    pwd = db.Column(db.String(100))  # 密码
    email = db.Column(db.String(100), unique=True)  # 邮箱
    phone = db.Column(db.String(11), unique=True)  # 电话
    info = db.Column(db.Text)  # 个性简介
    face = db.Column(db.String(255), unique=True)  # 头像
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow())  # 注册时间
    uuid = db.Column(db.String(255), unique=True)  # 唯一标识符

    userlogs = db.relationship('Userlog', backref='user')  # 会员日志外键关系关联
    comments = db.relationship('Comment', backref='user')  # 评论外键关系关联
    moviecols = db.relationship('Moviecol', backref='user')  # 电影收藏关系关联

    def __repr__(self):
        return f'<User:{self.name}>'


# 定义会员登录日志
class Userlog(db.Model):
    __tablename__ = "userlog"
    id = db.Column(db.BIGINT, primary_key=True)  # 编号
    user_id = db.Column(db.BIGINT, db.ForeignKey('user.id'))  # 会员Id
    ip = db.Column(db.String(100))  # 会员登录IP
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow())  # 添加时间

    def __repr__(self):
        return f'<Userlog:{self.id}>'


# ----------标签、电影、上映预告数据模型设计------------
# ------------------------------------------------------

# 定义电影标签
class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.BIGINT, primary_key=True)  # id
    name = db.Column(db.String(100), unique=True)  # 标签名
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow())  # 标签添加时间

    movies = db.relationship('Movie', backref='tag')  # 电影外键关联

    def __repr__(self):
        return f'<Tag:{self.name}>'


# 定义电影
class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.BIGINT, primary_key=True)  # id
    title = db.Column(db.String(255), unique=True)  # 电影标题
    url = db.Column(db.String(255), unique=True)  # 电影链接地址
    info = db.Column(db.Text)  # 电影简介
    logo = db.Column(db.String(255), unique=True)  # 封面
    star = db.Column(db.SmallInteger)  # 星级
    playnum = db.Column(db.BigInteger)  # 播放量
    commentnum = db.Column(db.BigInteger)  # 评论量
    area = db.Column(db.String(255))  # 所属地区
    release_time = db.Column(db.Date)  # 上映时间
    length = db.Column(db.String(100))  # 电影时长
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow())  # 添加时间

    tag_id = db.Column(db.BIGINT, db.ForeignKey('tag.id'))  # 所属标签

    comments = db.relationship('Comment', backref='movie')  # 电影评论外键关联
    moviemcols = db.relationship('Moviecol', backref='movie')  # 电影收藏外键关系关联

    def __repr__(self):
        return f'<Movie {self.title}>'


# 电影上映预告
class Preview(db.Model):
    __tablename__ = 'preview'
    id = db.Column(db.BIGINT, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True)  # 标题
    logo = db.Column(db.String(255), unique=True)  # 封面
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow())  # 添加时间

    def __repr__(self):
        return f'<Preview:{self.title}>'


# --------------评论及收藏数据模型设计------------------
# ------------------------------------------------------

# 评论
class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.BIGINT, primary_key=True)  # 编号
    content = db.Column(db.Text)  # 评论内容
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow())  # 添加时间

    movie_id = db.Column(db.BIGINT, db.ForeignKey('movie.id'))  # 所属电影
    user_id = db.Column(db.BIGINT, db.ForeignKey('user.id'))  # 所属用户

    def __repr__(self):
        return f'<Comment:{self.id}>'


# 电影收藏
class Moviecol(db.Model):
    __tablename__ = 'moviecol'
    id = db.Column(db.BIGINT, primary_key=True)
    movie_id = db.Column(db.BIGINT, db.ForeignKey('movie.id'))
    user_id = db.Column(db.BIGINT, db.ForeignKey('user.id'))
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow())

    def __repr__(self):
        return f'<Moviecol:{self.id}>'


# --------------权限及角色数据模型设计------------------
# ------------------------------------------------------

# 权限
class Auth(db.Model):
    __tablename__ = "auth"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 权限名称
    url = db.Column(db.String(255), unique=True)  # 允许访问地址
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow())  # 添加时间

    def __repr__(self):
        return f'<Auth:{self.name}>'


# 角色
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 角色名称
    auths = db.Column(db.String(600))
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow())

    admins = db.relationship('Admin', backref='role')  # 与管理员建立外键关系

    def __repr__(self):
        return f'<Rolw:{self.name}>'


# 管理员
class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(1000), unique=True)
    is_super = db.Column(db.Boolean)
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow())

    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    adminlogs = db.relationship('AdminLog', backref='admin')
    oplogs = db.relationship('OpLog', backref='admin')

    def __repr__(self):
        return f'<Admin:{self.name}>'

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


# 管理员登录日志
class AdminLog(db.Model):
    __tablename__ = 'adminlog'
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow())

    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))

    def __repr__(self):
        return f'<AdminLog:{self.id}>'


# 管理员操作日志
class OpLog(db.Model):
    __tablename__ = 'oplog'
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(100))
    reason = db.Column(db.String(600))
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow())

    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))

    def __repr__(self):
        return f'<OpLog:{self.id}>'
