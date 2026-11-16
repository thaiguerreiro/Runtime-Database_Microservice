# README
## Description
A light database microservice that allows clients to save, retrieve, update, and delete data by keys through http requests.


### How to REQUEST data
Run ```npm install``` in terminal Run ```npm start``` to start server
import requests in client

Save Item
```javascript
response = requests.post(http://localhost:5001/items, json={
    "key": "key",
    "value": {"trait1": value, "trait2": value}
})
```
Retrieve item
```javascript
response = requests.get(f"http://localhost:5001/items/{key}")
```
Retrieve all items 
```javascript
response = requests.get("http://localhost:5001/items")
```
Delete item
```javascript
response = requests.delete(f"http://localhost:5001/items/{key}")
```

### How to RECEIVE data
store request's response into a variable as shown above. Http handles request/receive. 
###### (e.i., there is no special extra step you need to do to recieve the data, the program shown above handles it)


## UML sequence diagram
```
UML Sequence Diagram
Client                  Database_Microservice              Database
+-+                               |                           |
| |      POST /items              |                           |
| |   {key, value}                |                           |
| | ---------------------------> +-+                          |
| |                              | |                          |
| |                       Extract key and value               |
| |                              | |                          |
| |                       Validate parameters                 |
| |                              | |                          |
| |                       Call setItem(key, value)            |
| |                              | |                          |
| |                              | |    Store key and value   |
| |                              | |------------------------>+-+
| |                              | |                         | |
| |                              | |     Return success      | |
| |                              | |<------------------------+-+
| |                              | |                          |
| |                       Create JSON response                |
| |                              | |                          |
| |         HTTP 200 OK          | |                          |
| |      {"success": true}       | |                          |
| |<- - - - - - - - - - - - - - -+-+                          |
| |                               |                           |
| |                               |                           |
| |        GET /items/key         |                           |
| |----------------------------->+-+                          |
| |                              | |                          |
| |                         Extract key                       |
| |                              | |                          |
| |                       Validate parameter                  |
| |                              | |                          |
| |                        Call getItem(key)                  |
| |                              | |                          |
| |                              | |    Check if key exists   |
| |                              | |-----------------------> +-+
| |                              | |                         | |
| |                              | |    Return item value    | |
| |                              | |<------------------------+-+
| |                              | |                          |
| |                         Create JSON response              |
| |                              | |                          |
| |         HTTP 200 OK          | |                          |
| |{"success": true, "data": value}|                          |
| |<- - - - - - - - - - - - - - -+-+                          |
| |                               |                           |
| |                               |                           |
| |           GET /items          |                           |
| |----------------------------->+-+                          |
| |                              | |                          |
| |                       Call getAllItems()                  |
| |                              | |                          |
| |                              | |    Retrieve all items    |
| |                              | |------------------------>+-+
| |                              | |                         | |
| |                              | |    Return all items     | |
| |                              | |<------------------------+-+
| |                              | |                          |
| |                      Create JSON response                 |
| |                              | |                          |
| |         HTTP 200 OK          | |                          |
| | {"success": true, "data": {}}| |                          |
| |<- - - - - - - - - - - - - - -+-+                          |
| |                               |                           |
| |                               |                           |
| |      DELETE /items/key        |                           |
| |----------------------------->+-+                          |
| |                              | |                          |
| |                         Extract key                       |
| |                              | |                          |
| |                       Validate parameter                  |
| |                              | |                          |
| |                      Call deleteItem(key)                 |
| |                              | |                          |
| |                              | |    Check if key exists   |
| |                              | |-----------------------> +-+
| |                              | |                         | |
| |                              | |                Delete key and value
| |                              | |                         | |
| |                              | |      Return success     | |
| |                              | |<------------------------+-+
| |                              | |                          |
| |                      Create JSON response                 |
| |                              | |                          |
| |         HTTP 200 OK          | |                          |
| |      {"success": true}       | |                          |
| |<- - - - - - - - - - - - - - -+-+                          |
| |                               |                           |
+-+                               |                           |
```