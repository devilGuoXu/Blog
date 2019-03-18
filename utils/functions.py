from functools import wraps

from flask import session, redirect, url_for


def is_login(func):
    @wraps(func)
    def check(*args, **kwargs):
        user_id = session.get('user_id')
        if user_id:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('back.login'))

    return check

