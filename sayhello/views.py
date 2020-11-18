from flask import render_template, request, url_for, redirect, flash
from sayhello import app, db
from sayhello.forms import HelloForm
from sayhello.models import Message
from flask_login import login_user
from sayhello.models import User
from flask_login import login_required, logout_user, current_user


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('index'))

        name = request.form['name']
        body = request.form['body']
        if not name or not body:
            flash('Invalid input.')
            return redirect(url_for('index'))
        message = Message(name=name, body=body)
        db.session.add(message)
        db.session.commit()
        flash('Item created.')
        return redirect(url_for('index'))

    messages = Message.query.all()
    return render_template('index.html', messages=messages)


@app.route('/message/edit/<int:message_id>', methods=['GET', 'POST'])
@login_required
def edit(message_id):
    message = Message.query.get_or_404(message_id)

    if request.method == 'POST':
        name = request.form['name']
        body = request.form['body']

        if not name or not body:
            flash('Invalid input.')
            return redirect(url_for('edit', message_id=message_id))

        message.name = name
        message.body = body
        db.session.commit()
        flash('Item updated.')
        return redirect(url_for('index'))

    return render_template('edit.html', message=message)


@app.route('/message/delete/<int:message_id>', methods=['POST'])
@login_required
def delete(message_id):
    message = Message.query.get_or_404(message_id)
    db.session.delete(message)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.first()

        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('Login success.')
            return redirect(url_for('index'))

        flash('Invalid username or password.')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
@login_required
# 用于视图保护,后面会详细介绍
def logout():
    logout_user()  # 登出用户
    flash('Goodbye.')
    return redirect(url_for('index'))  # 重定向回首页


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))

        current_user.name = name
        # current_user 会返回当前登录用户的数据库记录对象
        # 等同于下面的用法
        # user = User.query.first()
        # user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))
    return render_template('settings.html')


