"""Admin forms."""
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import PasswordField, StringField, FloatField, MultipleFileField, FileField, SelectField, DateField, \
    TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired
from wtforms_alchemy import Unique, ModelForm, model_form_factory

from mycms.user.models import User
from flask_uploads import UploadSet, IMAGES

images = UploadSet('images', IMAGES)
BaseModelForm = model_form_factory(FlaskForm)


class AdminLoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(AdminLoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(AdminLoginForm, self).validate()
        if not initial_validation:
            return False

        self.user = User.query.filter_by(username=self.username.data).first()
        
        if not self.user:
            self.username.errors.append("Unknown username")
            return False

        if not self.user.check_password(self.password.data):
            self.password.errors.append("Invalid password")
            return False

        if not self.user.active:
            self.username.errors.append("User not activated")
            return False
        return True


class UserCrudForm(BaseModelForm):
    """Client Form ."""
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=25), Unique(User.username)])
    first_name = StringField("First Name", validators=[ Length(min=3, max=40)])
    last_name = StringField("Last Name", validators=[ Length(min=3, max=40)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(min=6, max=40), Unique(User.email)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=40)])
    confirm = PasswordField("Verify password",[DataRequired(), EqualTo("password", message="Passwords must match")])


class ModuleCrudForm(BaseModelForm):
    """Client Form ."""
    name = StringField("Name", validators=[DataRequired(), Length(min=5, max=80)])
    description = StringField("Description", validators=[DataRequired(), Length(min=5, max=256)])
    long_description = TextAreaField("Long Description", validators=[DataRequired(), Length(min=5)])
    tags = StringField("Tags (comma separated)", validators=[DataRequired(), Length(min=5)])
    demo_url = StringField("Demo Url", validators=[DataRequired(), Length(min=5, max=256)])
    code_path = StringField("Code Path", validators=[DataRequired(), Length(min=5, max=256)])
    price = FloatField("Price", validators=[DataRequired()])
    support_price = FloatField("Support Price", validators=[DataRequired()])
    release_date = DateField("Release Date", validators=[DataRequired()])
    last_update_date = DateField("Release Date", validators=[DataRequired()])
    image = FileField('Product Image (397x306)', validators=[FileRequired(), FileAllowed(images, 'Images only allowed!')])
    images = MultipleFileField('Product Screenshots (726x403)', validators=[DataRequired(), FileAllowed(images, 'Images only!')])


class SlideShowCrudForm(BaseModelForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=5, max=80)])
    image = FileField('SlideShow Image (928x413)', validators=[FileRequired(), FileAllowed(images, 'Images only allowed!')])


class SeoCrudForm(BaseModelForm):
    meta_tag = SelectField(u'Meta Tag',choices=[('name','name'),('property','property')] ,validators=[DataRequired()])
    title = StringField("Title", validators=[DataRequired(), Length(min=5, max=80)])
    content = StringField("Content", validators=[DataRequired(), Length(min=5, max=255)])


#############################################################
class HomeTextForm(BaseModelForm):
    firstext = StringField("First Title", validators=[DataRequired(), Length(min=25, max=80)])
    secondtext = StringField("Second Title", validators=[DataRequired(), Length(min=25, max=80)])

class TechnologiesForm(BaseModelForm):
    firstext = StringField("First Title", validators=[DataRequired(), Length(min=25, max=80)])
    secondtext = StringField("Second Title", validators=[DataRequired(), Length(min=25, max=80)])

class ImageTechnologyForm(BaseModelForm):
    image = FileField('Technology Image (128x128)', validators=[FileRequired(), FileAllowed(images, 'Images only allowed!')])

class WebsiteLogoForm(BaseModelForm):
    logo_image = FileField('Logo Image (128x128)', validators=[FileRequired(), FileAllowed(images, 'Logo Only allowed!')])


# Footer Text Form
class FooterTextForm(BaseModelForm):
    title = TextAreaField("Long Description", validators=[DataRequired(), Length(min=5)])


# Social Media Form 
class SocialIocnForm(BaseModelForm):
    # image = FileField('Logo Image (128x128)', validators=[FileRequired(), FileAllowed(images, 'Social Iocn Image Only!')])
    icon = StringField("Icon Html Code(fab fa-facebook-f)", validators=[DataRequired()])
    url_link = StringField("Icon Link", validators=[DataRequired()])


# Copyright Form Model
class CopyRightForm(BaseModelForm):
    text = StringField("Copyright Footer Text", validators=[DataRequired(), Length(min=6, max=60)])


# Footer Image Model Form
class FooterImageForm(BaseModelForm):
    image = FileField('Footer Image', validators=[FileRequired(), FileAllowed(images, "Image Allowed Only !")])


# Resource Title Role Model Form
class ResourcesForm(BaseModelForm):
    role_title = StringField("Role Add ...", validators=[DataRequired(), Length(min=3, max=20)])


# Resource Detais Add with Role
class ResourceDetailAddForm(BaseModelForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=5, max=20)])
    description = TextAreaField("Description", validators=[DataRequired(), Length(min=5)])