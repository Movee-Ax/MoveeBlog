from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask('sayhello')
app.config.from_pyfile('settings.py')
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
login_manager = LoginManager(app)
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数,接受用户 ID 作为参数
    from moveeblog.models import User
    user = User.query.get(int(user_id))  # 用 ID 作为 User 模型的主键查询对应的用户
    return user
# 返回用户对象


from moveeblog import views, errors, commands
