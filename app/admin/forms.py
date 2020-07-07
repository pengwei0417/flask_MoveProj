from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError

from app.models import Admin, Tag


# 后台登录表单
class LoginForm(FlaskForm):
    # 用户名
    account = StringField(
        # 元素标题
        label="账号",
        # 验证
        validators=[
            DataRequired("请输入帐号！")
        ],
        # 描述
        description='账号',
        # 附加
        render_kw={
            "class": "form-control",
            "placeholder": "请输入账号！",
            "required": "required"
        }
    )

    # 密码
    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码")
        ],
        description='密码',
        render_kw={
            "class": "form-control",
            "placeholder": "请输入登录密码",
            "required": "required"
        }
    )

    # 登录
    submit = SubmitField(
        label="登录",
        render_kw={
            "class": "btn btn-primary btn-block btn-flat"
        }
    )

    #
    # 登录验证
    def validate_account(self, field):
        account = field.data
        admin = Admin.query.filter_by(name=account).count()  # 验证用户名
        if admin == 0:
            raise ValidationError('账号不存在！')  # 抛出错误验证信息


# 后台标签管理表单
class TagForm(FlaskForm):
    name = StringField(
        label='名称',
        validators=[DataRequired('请输入标签')],
        description='标签',
        render_kw={
            'class': "form-control",
            'id': "input_name",
            'placeholder': "请输入标签名称！"
        }
    )
    submit = SubmitField(
        label='编辑',
        render_kw={
            "class": "btn btn-primary"
        }
    )


# 电影管理表单
class MovieForm(FlaskForm):
    title = StringField(
        label='片名',
        validators=[
            DataRequired('请输入电影名称')],
        description='片名',
        render_kw={
            "class": "form-control",
            "id": "input_title",
            "placeholder": "请输入影片名"
        }
    )

    url = FileField(
        label='文件',
        validators=[DataRequired('请输入影片')],
        description='影片文件'
    )

    info = TextAreaField(
        label="简介",
        render_kw={
            "class": "form-control",
            "rows": 10
        }
    )

    logo = FileField(
        label='封面',
        description='封面'
    )

    star = SelectField(
        label="星级",
        coerce=int,
        choices=[(1, "1星"), (2, "2星"), (3, "3星"), (4, "4星"), (5, "5星")],
        render_kw={
            "class": "form-control"
        }
    )

    tags = Tag.query.all()
    tag_id = SelectField(
        label="标签",
        coerce=int,
        description='所属标签',
        choices=[(v.id, v.name) for v in tags]
    )

    area = StringField(
        label='地区',
        render_kw={
            "class": "form-control",
            "placeholder": "请输入地区"
        }
    )

    length = StringField(
        label='片长',
        validators=[DataRequired('请输入片长')],
        render_kw={
            "class": "form-control",
            "placeholder": "请输入片长"
        }
    )

    release_time = StringField(
        label='上映时间',
        validators=[DataRequired('请输入上映时间')],
        render_kw={
            "class": "form-control",
            "placeholder": "请选择上映时间",
            "id": "input_release_time"
        }
    )

    submit = SubmitField(
        label="编辑",
        render_kw={
            "class": "btn btn-primary"
        }
    )


class PreviewForm(FlaskForm):
    title = StringField(
        label='标题',
        validators=[DataRequired('请输入预告影片名称')],
        description="预告标题",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入预告标题"
        }
    )

    logo = FileField(
        label="预告封面",
        validators=[DataRequired('请上传预告封面')],
    )

    submit = SubmitField(
        label='保存',
        render_kw={
            "class": "btn btn-primary"
        }
    )
