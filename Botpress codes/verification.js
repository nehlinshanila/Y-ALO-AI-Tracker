const axios = require('axios');
const config = require('./config');

const firebaseUrl = `${config.firebaseUrl}/users.json`;

const enteredName = workflow.user_variable.first;
const userVariableExists = await axios
  .get(firebaseUrl)
  .then((response) => {
    const users = response.data;
    console.log('Response data', users);
    const userExists = users.hasOwnProperty(enteredName);
    console.log('user exists?: ', userExists);
    if (userExists) {
      console.log('Found the name');
      return true;
    } else {
      axios.patch(firebaseUrl, { Name: enteredName });
      console.log('Added the name to firebase');
      return false;
    }
  })
  .catch((error) => {
    console.error('Error checking user variable in Firebase:', error);
    return false;
  });
