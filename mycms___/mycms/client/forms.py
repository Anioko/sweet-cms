from flask_uploads import UploadSet, IMAGES
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, PasswordField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional
from wtforms_alchemy import Unique, ModelForm, model_form_factory

from mycms.user.models import User

images = UploadSet('images', IMAGES)
BaseModelForm = model_form_factory(FlaskForm)


class ClientDataForm(BaseModelForm):
    """Client Form ."""
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=25), Unique(User.username)], render_kw={'disabled': ''})
    first_name = StringField("First Name", validators=[DataRequired(), Length(min=3, max=40)])
    last_name = StringField("Last Name", validators=[DataRequired(), Length(min=3, max=40)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(min=6, max=40), Unique(User.email)], render_kw={'disabled': ''},)
    password = PasswordField("Password", validators=[Optional(), Length(min=6, max=40)])
    confirm = PasswordField("Verify password",validators=[Optional(), EqualTo("password", message="Passwords must match")])


class ClientBrandForm(BaseModelForm):
    name = StringField("Brand Name", validators=[DataRequired(),Length(min=3, max=128)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(min=6, max=128)])
    image = FileField('Brand Logo (182x33)', validators=[FileRequired(), FileAllowed(images, 'Images only allowed!')])
    site_link = StringField("Website", validators=[DataRequired(), Length(min=3, max=128)])

