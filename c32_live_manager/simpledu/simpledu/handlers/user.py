from flask import Blueprint, render_template
from simpledu.models import User

user = Blueprint('user', __name__, url_prefix='/users')

@user.route('/<user_id>')
def index(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    return render_template('user/detail.html', user=user) 
