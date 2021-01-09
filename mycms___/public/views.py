# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_required, login_user, logout_user, current_user

from mycms.decorators import anonymous_required
from mycms.admin.models import Module, SlideShowImage
from mycms.extensions import login_manager
from mycms.public.forms import LoginForm
from mycms.user.forms import RegisterForm
from mycms.user.models import User
from mycms.utils import sync_cart, get_current_cart

blueprint = Blueprint("public", __name__, static_folder="../static")


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route("/", methods=["GET", "POST"])
def home():
    """Home page."""
    form = LoginForm()
    slideshows = SlideShowImage.query.all()
    return render_template("public/home.html", form=form, slideshows=slideshows)


@blueprint.route('/under_construction')
def under_construction():
    return render_template("public/undre_construction.html")


@blueprint.route('/login/', methods=['GET', 'POST'])
@anonymous_required
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            login_user(form.user)
            sync_cart()
            redirect_url = request.args.get("next") or url_for("public.home")
            return redirect(redirect_url)
    return render_template("public/login.html", form=form)


@blueprint.route('/product/<int:product_id>/<product_name>')
def view_product(product_id, product_name):
    product = Module.query.get_or_404(product_id)
    return render_template("public/product.html", product=product)


@blueprint.route("/logout/")
@login_required
def logout():
    """Logout."""
    logout_user()
    return redirect(url_for("public.home"))


@blueprint.route("/register/", methods=["GET", "POST"])
@anonymous_required
def register():
    """Register new user."""
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        User.create(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            active=True,
        )
        flash("Thank you for registering. You can now log in.", "web_success")
        return redirect(url_for("public.home"))
    return render_template("public/register.html", form=form)


@blueprint.route("/about/")
def about():
    """About page."""
    form = LoginForm(request.form)
    return render_template("public/about.html", form=form)


@blueprint.route('/cart/')
def cart_details():
    cart = get_current_cart()
    return render_template('public/cart/view.html', cart=cart)


@blueprint.route('/download/')
def download():
    if current_user.is_authenticated:
        return redirect(url_for('client.download'))
    return render_template('public/download.html')
