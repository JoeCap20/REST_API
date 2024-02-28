from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

#calling class Blueprint and passing the needed fields
blp = Blueprint("Items", "items", description="Operations on items")

#this is a decorator and calling the function and passing the string with id
@blp.route("/item/<string:item_id>")
#A class dor item
class Item(MethodView):
    #this is a decorator and calling the function
    @blp.response(200, ItemSchema)
    #This is just a GET function
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    #This is just a delete function
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted."}

    #this is a decorator and calling the function easy to manipluate data
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    #Put wants to execute an idempot request means runnin one or ten requests should result in the same state.
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            #these two lines below are how we update the item. This IF will now check if the item exists and needs to be updated or created
            #if the item exists we need price and name to be passed and if it doesnt we need price, name and store id to be passed.
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id, **item_data)
        
        #The problem is that if the item doesnt exist it should create and it if does exist then it should update it
        db.session.add(item)
        db.session.commit()

        return item

#this is a decorator and calling the function
@blp.route("/item")
#Another class that is calling a class 
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        #This will now return a list of items instead of an object
        return ItemModel.query.all()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)
        #Basic try and except for adding items if doesnt work give error
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting the item.")

        return item