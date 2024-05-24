const axios = require('axios');
const config = require('./config');

const firebaseUrl = `${config.firebaseUrl}/users.json`;

try {
  const response = await axios.get(firebaseUrl);
  const users = response.data;
  const randomIndex = Math.floor(Math.random() * users.length);
  const randomUser = users[randomIndex];

  workflow.output_period_date = randomUser.input_period_date;

  console.log('Data fetched and stored successfully:', workflow.output_period_date);
} catch (error) {
  console.error('Failed to fetch data from Firebase:', error);
  workflow.errorMessage = 'Failed to fetch user data';
}
