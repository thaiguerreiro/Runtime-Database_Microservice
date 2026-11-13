const database = {};

// Creates or updates (overwrites) an items value in the database
function setItem(key, value) {
  // parameter validation
  if (isBadParameter(key) && isBadParameter(value))
    return { success: false, error: "bad parameters" };
  if (isBadParameter(key))
    return { success: false, error: "bad parameter: key" };
  if (isBadParameter(value))
    return { success: false, error: "bad parameter: value" };

  // set item key in databse to value
  database[key] = value;
  return { success: true };
}

// Removes the key and value of an item from the databse
function deleteItem(key) {
  // parameter validation
  if (isBadParameter(key))
    return { success: false, error: "bad parameter: key" };

  // Should we check for non existent keys and return false? it works without?
  // set item key in databse to value
  delete database[key];
  return { success: true };
}

// Returns the value of the item with the corrisponding key
function getItem(key) {
  // parameter validation
  if (isBadParameter(key))
    return { success: false, error: "bad parameter: key" };

  // get item's value matched with key
  if (!Object.hasOwn(database, key))
    return { success: false, error: "key does not exist" };
  value = database[key];
  return { success: true, data: value };
}

// this function is needed instead of just checking for !paramter
// in the functions above.  because the keys of 'false' and '0'
// would evaluate to false
const isBadParameter = (p) => p == undefined || p == null;