Description


How to REQUEST data
For adding an item
response = requests.post("https://runtime-databaseURL/save", json=data)
Delete an item
response = requests.delete(f"https://runtime-databaseURL/delete/{ID}")
For getting every item
response = requests.get(f"https://runtime-databaseURL/retrieve")
For getting a specific item
response = requests.get(f"https://runtime-databaseURL/retrieve/{ID}")


How to RECEIVE data


UML sequence diagram
