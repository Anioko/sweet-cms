import os

from flask import url_for

from mycms.database import PkModel, Column, reference_col, relationship
from mycms.extensions import db, ma


class Module(PkModel):
    """A role for a user."""

    __tablename__ = "modules"
    name = Column(db.String(80), nullable=False)
    description = Column(db.String(256), nullable=False)
    long_description = Column(db.Text, nullable=False)
    demo_url = Column(db.String(256), nullable=False)
    code_path = Column(db.String(256), nullable=False)
    price = Column(db.Float, nullable=False)
    support_price = Column(db.Float, nullable=False)
    image_filename = Column(db.String(256), nullable=False)
    tags = Column(db.Text, nullable=False)
    release_date = Column(db.Date, server_default='current_timestamp', default=db.func.now(), nullable=False)
    last_update_date = Column(db.Date, server_default='current_timestamp', default=db.func.now(), nullable=False)

    @property
    def image_url(self):
        return url_for('_uploads.uploaded_file', setname='images', filename=self.image_filename, _external=True)

    @property
    def image_path(self):
        from flask import current_app
        return os.path.join(current_app.config['UPLOADED_IMAGES_DEST'], self.image_filename)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Role({self.name})>"


class ModuleImage(PkModel):
    __tablename__ = "module_images"

    image_filename = Column(db.String(256), nullable=False)

    module_id = reference_col("modules", nullable=True)
    module = relationship("Module", backref="screenshots")

    @property
    def image_url(self):
        return url_for('_uploads.uploaded_file', setname='images', filename=self.image_filename, _external=True)

    @property
    def image_path(self):
        from flask import current_app
        return os.path.join(current_app.config['UPLOADED_IMAGES_DEST'], self.image_filename)


class SlideShowImage(PkModel):
    __tablename__ = "slide_show_images"

    title = Column(db.String(80), nullable=False)
    image_filename = Column(db.String(256), nullable=False)

    @property
    def image_url(self):
        return url_for('_uploads.uploaded_file', setname='images',filename=self.image_filename, _external=True)


    @property
    def image_path(self):
        from flask import current_app
        return os.path.join(current_app.config['UPLOADED_IMAGES_DEST'], self.image_filename)


class Seo(PkModel):
    __tablename__ = "seo"
    meta_tag = Column(db.String(80), nullable=False)
    title = Column(db.String(80), nullable=False)
    content = Column(db.String(256), nullable=False)


class Setting(PkModel):
    __tablename__ = "settings"
    name = Column(db.String(80), nullable=False)
    display_name = Column(db.String(80), nullable=False)
    value = Column(db.String(512), nullable=True)


# Schemas
class ModuleSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "description", "price", "support_price", "image_url")
        module = Module
