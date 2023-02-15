import os
from typing import Optional, Dict

from flask import (
    Blueprint, request,
    render_template, current_app,
    session, redirect, url_for
)

from database.operations import select
from database.sql_provider import SQLProvider


blueprint_auth = Blueprint('blueprint_auth', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_auth.route('/', methods=['GET', 'POST'])
def start_auth():
    if request.method == 'GET':
        return render_template('input_login.html', message='')
    else:
        login = request.form.get('login')
        password = request.form.get('password')
        if login and password:
                user_info = define_user(login, password)
                if user_info:
                    session['user_id'] = user_info['user_id']
                    session['user_group'] = user_info['user_group']
                    session.permanent = True
                    return redirect(url_for('menu_choice'))
                else:
                    return render_template('input_login.html', message='Пользователь не найден')
        return render_template('input_login.html', message='Заполните все поля')


def define_user(login: str, password: str) -> Optional[Dict]:
    sql_internal = provider.get('internal_user.sql', login=login, password=password)
    sql_external = provider.get('external_user.sql', login=login, password=password)

    user_info = None

    for sql_search in [sql_internal, sql_external]:
        _user_info = select(current_app.config['db_config'], sql_search)
        print(_user_info)
        if _user_info:
            user_info = _user_info
            del _user_info
            break
    if user_info is None:
        return user_info

    return user_info[0]
