from flask import Flask, request

app = Flask(__name__)

#In most rest API's the data is stored in a databse but now we will store it in a python list

stores = [
    {
        "name": "My Store",
        "items":[
            {
                "name": "Chair",
                "price": 15.99
            },
            {
                "name": "Table",
                "price": 59.99
            }
        ]
    }
]

#Later we will make dynamic allowing users to add data to this list
#This will be our first endpoing that will return this data when the client requests it
#The endpoint is the /store and the function associated with it is the def  get_scores function
#This below is what allows us to do a GET request
@app.get("/store") #http://127.0.0.1:5000/store
def get_stores():
    return{"stores": stores}

#JSON is just a long string whose contents are in a specific format

#This code below will allow us to do a POST request
@app.post("/store")
def create_store():
    request_data = request.get_json()
    new_store = {"name": request_data["name"], "items": []}
    stores.append(new_store)
    return new_store, 201 #201 is the return status code which will return "Created" 200 means "OK"

#sending data throught the URL
@app.post("/store/<string:name>/item")
def create_item(name):
    request_data = request.get_json()
    for store in stores:
        if store["name"] == name:
            new_item = {"name": request_data["name"], "price": request_data["price"]}
            store["items"].append(new_item)
            return new_item, 201
    return{"message": "Store not found"}, 404

@app.get("/store/<string:name>")
def get_store(name):
    for store in stores:
        if store["name"] == name:
            return store
    return {"message": "Store not found"}, 404

@app.get("/store/<string:name>/item")
def get_item_in_store(name):
    for store in stores:
        if store["name"] == name:
            return {"items": store["items"]}
    return {"message": "Store not found"}, 404