from flask import Blueprint, render_template
from flask.views import MethodView
from flask_login import current_user

bp = Blueprint('public', __name__)


class IndexView(MethodView):

    def get(self):
        if current_user.is_authenticated:
            return render_template('app.html')
        return render_template('public/index.html')

bp.add_url_rule('/', IndexView.as_view('index'))

class RenderTemplateView(MethodView):

    def __init__(self, template_name):
        self.template_name = template_name

    def get(self):
        return render_template(self.template_name)

bp.add_url_rule('/sign-up', RenderTemplateView.as_view('signup', template_name='public/sign_up.html'))
bp.add_url_rule('/login', RenderTemplateView.as_view('login', template_name='public/login.html'))
