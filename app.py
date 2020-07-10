import os
import vk_oauth
import requests
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, redirect, url_for, render_template
from flask_login import current_user, login_user, logout_user, LoginManager, UserMixin


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config.from_pyfile('instance/config.py')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)


@login.user_loader
def load_user(user_id):
    return VkUser.query.get(int(user_id))


class VkUser(UserMixin, db.Model):
    __tablename__ = 'vk_user'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,nullable=False, unique=True)
    token = db.Column(db.String(128))


@app.route('/', methods=['GET'])
def index():
    if current_user.is_authenticated:
        user = vk_oauth.get_user_name(current_user.token)
        friend_list = vk_oauth.get_friends_names(current_user.token, 5)
        if user[1] == 400 or friend_list[1] == 400:
            deleted_user = current_user
            logout()
            db.session.delete(deleted_user)
            db.session.commit()
        return render_template('index.html', link=None, user=user[0], friend_list=friend_list[0])
    else:
        oauth = vk_oauth.VkOAuth()
        return render_template('index.html', link=oauth.get_authorization_url(), user=None, friendList=None)


@app.route('/oauth/redirect', methods=['GET'])
def oauth_redirect():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.args.get('code'):
        oauth = vk_oauth.VkOAuth()
        code = request.args.get('code')
        req = requests.get(oauth.get_receive_url(code)).json()
        if 'access_token' in req:
            user = VkUser.query.filter_by(user_id=req['user_id']).first()
            if not user:
                user = VkUser(user_id=req['user_id'], token=req['access_token'])
                db.session.add(user)
                db.session.commit()
            login_user(user, remember=True)
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    db.create_all()
    app.run()
