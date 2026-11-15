# README
## Description
### How to REQUEST data
Run ```npm install``` in terminal Run ```npm start``` to start server

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
