# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
import uuid
from hashlib import sha512

from flask import flash, request, session
from flask_login._compat import text_type
from flask_login.utils import _get_remote_addr, current_user

from mycms.admin.models import Setting
from mycms.extensions import db


def flash_errors(form, category="warning"):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{getattr(form, field).label.text} - {error}", category)


def put_session_cart_id():
    try:
        session['cart_id']
    except:
        u = uuid.uuid4()
        user_agent = request.headers.get('User-Agent')
        if user_agent is not None:
            user_agent = user_agent.encode('utf-8')
        base = 'cart: {0}|{1}|{2}'.format(_get_remote_addr(), user_agent, u)
        if str is bytes:
            base = text_type(base, 'utf-8', errors='replace')  # pragma: no cover
        h = sha512()
        h.update(base.encode('utf8'))
        session['cart_id'] = h.hexdigest()


def sync_cart():
    from mycms.client.models import Cart

    user_cart = Cart.query.filter_by(user_id=current_user.id).order_by(Cart.id.desc()).first()
    if user_cart:
        Cart.query.filter_by(user_id=current_user.id).filter(Cart.id != user_cart.id).delete()
    else:
        session_id = session['cart_id']
        cart = Cart.query.filter_by(session_id=session_id).order_by(Cart.id.desc()).first()
        if cart:
            Cart.query.filter_by(session_id=session_id).filter(Cart.id != cart.id).delete()
            cart.user_id = current_user.id
            db.session.add(cart)
            db.session.commit()


def get_current_cart():
    from mycms.client.models import Cart

    session_id = session['cart_id']
    if current_user.is_authenticated:
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if cart:
            Cart.query.filter_by(user_id=current_user.id).filter(Cart.id != cart.id).delete()
        else:
            cart = Cart(user_id=current_user.id)
            db.session.add(cart)
            db.session.commit()
            db.session.refresh(cart)
    else:
        cart = Cart.query.filter_by(session_id=session_id).first()
        if cart:
            Cart.query.filter_by(session_id=session_id).filter(Cart.id != cart.id).delete()
        else:
            cart = Cart(session_id=session_id)
            db.session.add(cart)
            db.session.commit()
            db.session.refresh(cart)

    return cart


def get_setting_val(setting):
    if type(()) != type(setting):
        return None
    if len(setting) < 2:
        return None
    setting_obj = Setting.query.filter_by(name=setting[0]).first()
    if not setting_obj:
        setting_obj = Setting.create(
            name=setting[0],
            display_name=setting[1],
            value=''
        )
        db.session.add(setting_obj)
        db.session.commit()
    return setting_obj
