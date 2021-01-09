# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, logout_user, current_user

blueprint = Blueprint("user", __name__, url_prefix="/users", static_folder="../static")


@blueprint.route("/")
@login_required
def members():
    """List members."""
    return render_template("users/members.html")


@login_required
@blueprint.route("/logout")
def logout_of_system():
    logout_user()
    return redirect(url_for("public.home"))
