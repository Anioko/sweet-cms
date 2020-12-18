import os

from flask import url_for

from mycms.admin.models import ModuleSchema
from mycms.database import PkModel, Column
from mycms.extensions import db, ma


class Cart(PkModel):
    __tablename__ = 'carts'
    session_id = Column(db.String(256))
    user_id = Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=True, default=None)
    step = Column(db.Integer, default=1)

    created_at = Column(db.DateTime, default=db.func.now())
    updated_at = Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    user = db.relationship("User", backref="cart")


class CartItem(PkModel):
    __tablename__ = 'cart_items'
    cart_id = Column(db.Integer, db.ForeignKey('carts.id', ondelete="CASCADE"), nullable=True,
                       default=None)
    product_id = Column(db.Integer, db.ForeignKey('modules.id', ondelete="CASCADE"))
    product_support = Column(db.Boolean, default=False)
    buyer_id = Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=True, default=None)
    created_at = Column(db.DateTime, default=db.func.now())
    updated_at = Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    cart = db.relationship("Cart", backref=db.backref("cart_items", lazy='joined'))
    buyer = db.relationship("User", backref="my_cart_items", primaryjoin="User.id == CartItem.buyer_id")
    product = db.relationship("Module", backref="cart_items")


class BrandInfo(PkModel):
    __tablename__ = 'brands'
    user_id = Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=True, default=None)
    name = Column(db.String(128), nullable=False)
    email = Column(db.String(128), nullable=False)
    image_filename = Column(db.String(256), nullable=False)
    site_link = Column(db.String(128), nullable=False)

    user = db.relationship("User", backref=db.backref("brand_info", uselist=False), uselist=False)

    @property
    def image_url(self):
        return url_for('_uploads.uploaded_file', setname='images', filename=self.image_filename, _external=True)

    @property
    def image_path(self):
        from flask import current_app
        return os.path.join(current_app.config['UPLOADED_IMAGES_DEST'], self.image_filename)


# Schemas
class CartItemSchema(ma.Schema):
    class Meta:
        model = CartItem
        fields = ("id", "product_id", "product_support", "created_at", "updated_at", "product", "product_support")
    product = ma.Nested(ModuleSchema)


class CartSchema(ma.Schema):
    class Meta:
        fields = ("is", "session_id", "user_id", "step", "created_at", "updated_at", "cart_items")

    cart_items = ma.Nested(CartItemSchema, many=True)
