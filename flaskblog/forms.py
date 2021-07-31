from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Tên người dùng', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mật khẩu', validators=[DataRequired()])
    confirm_password = PasswordField('Xác nhận mật khẩu', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Đăng ký')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Tên người dùng này đã tồn tại! Vui lòng chọn một cái khác.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email này đã tồn tại! Vui lòng chọn một cái khác.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mật khẩu', validators=[DataRequired()])
    remember = BooleanField('Ghi nhớ tôi')
    submit = SubmitField('Đăng nhập')


class UpdateAccountForm(FlaskForm):
    username = StringField('Tên người dùng', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Ảnh đại diện', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Cập nhật')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Tên người dùng này đã tồn tại! Vui lòng chọn một cái khác.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email này đã tồn tại! Vui lòng chọn một cái khác.')


class PostForm(FlaskForm):
    title = StringField('Tiêu đề', validators=[DataRequired()])
    content = TextAreaField('Nội dung', validators=[DataRequired()])
    submit = SubmitField('Đăng bài')