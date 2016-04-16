from flask import Blueprint, render_template
from flask.views import MethodView


bp = Blueprint('public', __name__)

@bp.route('/')
def index():
    return render_template('public/index.html')

class Signup(MethodView):
    template = 'public/sign_up.html'

    def get(self):
        return render_template(self.template)

    def post(self):
        form = ''
        return render_template(self.template)

bp.add_url_rule('/sign_up', view_func=Signup.as_view('sign_up'))


class Login(MethodView):
    template = 'public/login.html'

    def get(self):
        return render_template(self.template)

    def post(self):
        form = ''
        return render_template(self.template)

bp.add_url_rule('/login', view_func=Login.as_view('login'))
