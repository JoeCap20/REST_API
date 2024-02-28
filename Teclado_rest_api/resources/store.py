import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import StoreModel
from schemas import StoreSchema
#Calling class blueprinf and passing parameters
blp = Blueprint("stores", __name__, description="Operations on stores")

#this is a decorator and calling the function and passing in the parameters
@blp.route("/store/<string:store_id>")
#Creating class and passing the parameter
class Store(MethodView):
    #this is a decorator and calling the function and passing in the parameters
    @blp.response(200, StoreSchema)
    #just getting the store id
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store
    #Deleting the store id
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted"}

#this is a decorator and calling the function and passing in the parameters
@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        #A try and except for adding items if doesnt work give error
        try:
            db.session.add(store)
            db.session.commit()
        #Checking if the store exists throw an error
        except IntegrityError:
            abort(
                400, message="A store with that name already exists.",
            )
        #If the whole thing is having a probelm or if an input doesnt match
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the store.")

        return store