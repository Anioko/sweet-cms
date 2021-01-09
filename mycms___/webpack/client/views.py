import os

from flask import Blueprint, render_template, request, redirect, flash, url_for, current_app, send_from_directory, abort
from flask_login import login_required,current_user
from wtforms.validators import Optional

from libs import get_compressed_files
from mycms.client.models import BrandInfo
from mycms.user.models import User
from mycms.admin.models import Logo, FooterText, FooterImage, SocialMediaIcon, CopyRight
from mycms.client.forms import ClientDataForm, ClientBrandForm
from mycms.extensions import db
from flask_uploads import UploadSet, IMAGES

blueprint = Blueprint("client", __name__, url_prefix="/client", static_folder="../static")
images = UploadSet('images', IMAGES)
 

@blueprint.route('account/', methods=["GET", "POST"])
@login_required
def account():
	form = ClientDataForm(obj=current_user)
	logo = Logo.query.first()
    # footer_text = FooterText.query.all()
    # media_icons = SocialMediaIcon.query.all()
    # footer_image = FooterImage.query.first()
    # copyright_text = CopyRight.query.first()
	if request.method == 'POST':
		if form.validate_on_submit():
			current_user.first_name = form.first_name.data
			current_user.last_name = form.last_name.data
			if form.password.data:
				current_user.set_password(form.password.data)
				db.session.add(current_user)
				db.session.commit()
				return redirect(url_for('client.account'))
	# print("Stop Here!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
	return render_template('client/account.html', form=form, logo=logo, footer_text=FooterText.query.all(), footer_image=FooterImage.query.first(), icons=SocialMediaIcon.query.all(), copyright_text=CopyRight.query.first())


@blueprint.route('brand/', methods=["GET", "POST"])
@login_required
def brand():
	brand = current_user.brand_info
	logo = Logo.query.first()
	current_app.logger.info(brand)
	form = ClientBrandForm(obj=brand)
	if brand:
		form.image.validators = form.image.validators[1:]
		form.image.validators.insert(0, Optional())
		form.image.flags.required = False
	if request.method == 'POST':
		if form.validate_on_submit():
			if request.files['image']:
				image = images.save(request.files['image'])
			if brand:
				if os.path.exists(brand.image_path):
					os.remove(brand.image_path)
				brand.name = form.name.data
				brand.email = form.email.data
				brand.site_link = form.site_link.data
				if request.files['image']:
					brand.image_filename = image
			else:
				brand = BrandInfo.create(
					user=current_user,
					name=form.name.data,
					email=form.email.data,
					image_filename=image,
					site_link=form.site_link.data
				)
			db.session.add(brand)
			db.session.commit()
			flash("Brand Info Updated Successfully .", "success")
			return redirect(url_for('client.brand'))
	return render_template('client/brand.html', form=form, brand=brand, logo=logo, footer_text=FooterText.query.all(), footer_image=FooterImage.query.first(), icons=SocialMediaIcon.query.all(), copyright_text=CopyRight.query.first())


@blueprint.route('/download/')
@login_required
def download():
	brand = current_user.brand_info
	if not brand:
		flash("You have to add your brand details first", 'info')
		return redirect(url_for('client.brand'))
	user_files = get_compressed_files(current_user.username)
	generated_files = [os.path.basename(file) for file in user_files]
	return render_template('client/download.html', generated_files=generated_files, logo=Logo.query.first(), footer_text=FooterText.query.all(), footer_image=FooterImage.query.first(), icons=SocialMediaIcon.query.all(), copyright_text=CopyRight.query.first())


@blueprint.route('download_archive/<file_name>')
@login_required
def download_archive(file_name):
	user_files = get_compressed_files(current_user.username)
	for file in user_files:
		if os.path.basename(file) == file_name:
			return send_from_directory(os.path.dirname(file), file_name)
	abort(404)
