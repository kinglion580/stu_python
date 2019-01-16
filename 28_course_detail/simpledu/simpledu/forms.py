from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, ValidationError
from wtforms.validators import Length, Email, EqualTo, Required, URL, NumberRange
from simpledu.models import db, User, Course


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[Required(), Length(3,24)])
    email = StringField('email', validators=[Required(), Email()])
    password = PasswordField('password', validators=[Required(), Length(6, 24)])
    repeat_password = PasswordField('repeat password', validators=[Required(), EqualTo('password')])
    submit = SubmitField('submit')
    
    def create_user(self):
        user = User()
        user.username = self.username.data
        user.email = self.email.data
        user.password = self.password.data
        
        db.session.add(user)
        db.session.commit()
        return user

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('username is already exist')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('email is already exist')

class LoginForm(FlaskForm):
    email = StringField('email', validators=[Required(), Email()])
    #username = StringField('username', validators=[Required(), Length(3, 24)])
    password = PasswordField('password', validators=[Required(), Length(6, 24)])
    remember_me = BooleanField('remember me')
    submit = SubmitField('submit')

    def validate_email(self, field):
        if field.data and not User.query.filter_by(email=field.data).first():
            raise ValidationError('email not register')

    '''
    def validate_username(self, field):
        if field.data and not User.query.filter_by(username=field.data).first():
            raise ValidationError('username not register')
    '''

    def validate_password(self, field):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('password wrong')

class CourseForm(FlaskForm):
    name = StringField('course name', validators=[Required(), Length(5, 32)])
    description = TextAreaField('course description', validators=[Required(), Length(20, 256)])
    image_url = StringField('cover image', validators=[Required(), URL()])
    author_id = IntegerField('author id', validators=[Required(), NumberRange(min=1, message='invalid user id')])
    submit = SubmitField('submit')

    def validate_author_id(self, field):
        if not User.query.get(self.author_id.data):
            raise ValidationError('user not exist')

    def create_course(self):
        course = Course()
        self.populate_obj(course)
        db.session.add(course)
        db.session.commit()
        return course

    def update_course(self, course):
        self.populate_obj(course)
        db.session.add(course)
        db.session.commit()
        return course
