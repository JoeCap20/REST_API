from db import db

class ItemModel(db.Model):
    __tablename__ = "items"

    #These lines below will be the titles of the columns
    id = db.Column(db.Integer, primary_key=True)
    #Take unique out, in order to have more than one of the same name and nullable to make sure its not empty
    name = db.Column(db.String, unique=False, nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False)
    store = db.relationship("StoreModel", back_populates="items")
    #This line below is new and added for tags
    tags = db.relationship("TagModel", back_populates="items", secondary="items_tags")
