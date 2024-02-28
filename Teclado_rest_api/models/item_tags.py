from db import db


class ItemsTags(db.Model):
    #This is creating the table name
    __tablename__ = "items_tags"

    #These are all of the columns
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))