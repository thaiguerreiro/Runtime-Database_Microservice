Description


How to REQUEST data
Run 'npm install' in terminal
Run 'npm start' to start server

Save Item
response = requests.post(http://localhost:5001/items, json={
    "key": "swoooord",
    "value": {"damage": 50, "rarity": "rare"}
})
Retrieve item
response = requests.get(f"http://localhost:5001/items/{id}")
Retrieve all items 
response = requests.get("http://localhost:5001/items")
Delete item
response = requests.delete(f"http://localhost:5001/items/{id}")


How to RECEIVE data


UML sequence diagram
