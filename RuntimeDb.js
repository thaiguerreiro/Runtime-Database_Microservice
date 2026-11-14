const database = {};
const express = require("express");
const app = express();

app.use(express.json()); // Allows server to receive JSON

// Creates or updates (overwrites) an items value in the database
function setItem(key, value) {
  // set item key in database to value
  database[key] = value;
  return { success: true };
}

// Removes the key and value of an item from the databse
function deleteItem(key) {

  if (!Object.hasOwn(database, key))
    return { success: false, error: "key does not exist" };

  // set item key in database to value
  delete database[key];
  return { success: true };
}

// Returns the value of the item with the corresponding key
function getItem(key) {
  // get item's value matched with key
  if (!Object.hasOwn(database, key))
    return { success: false, error: "key does not exist" };

  value = database[key];
  return { success: true, data: value };
}

// Returns every item
function getAllItems() {
    return {
        success: true,
        data: database
    };
}

// this function is needed instead of just checking for !paramter
// in the functions above.  because the keys of 'false' and '0'
// would evaluate to false
const isBadParameter = (p) => p == undefined || p == null;


// ------------------------------- Communication pipeline -------------------------------


app.post("/items", (req, res) => {
    const { key, value } = req.body || {};

    // Parameter validation
    if (isBadParameter(key) && isBadParameter(value))
        return res.status(400).json({
            success: false,
            error: "bad parameters"
        });

    if (isBadParameter(key))
        return res.status(400).json({
            success: false,
            error: "bad parameter: key"
        });

    if (isBadParameter(value))
        return res.status(400).json({
            success: false,
            error: "bad parameter: value"
        });

    // Save item
    const result = setItem(key, value);
    res.json(result);
});


app.get("/items/:key", (req, res) => {
    const key = req.params.key;

    // Parameter validation
    if (isBadParameter(key))
        return res.status(400).json({
            success: false,
            error: "bad parameter: key"
        });

    // Retrieve item
    const result = getItem(key);

    if (!result.success)
        return res.status(404).json(result);

    res.json(result);
});


app.get("/items", (req, res) => {
    const result = getAllItems();
    res.json(result);
});


// Dekete an item
app.delete("/items/:key", (req, res) => {
    const key = req.params.key;

    // Parameter validation
    if (isBadParameter(key))
        return res.status(400).json({
            success: false,
            error: "bad parameter: key"
        });

    // Delete item
    const result = deleteItem(key);

    // If Item does not exist
    if (!result.success)
        return res.status(404).json(result);

    res.json(result);
});


app.listen(5001, () => {
    console.log("Database server running on port 5001");
});