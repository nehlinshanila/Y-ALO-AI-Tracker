const axios = require('axios');
const config = require('./config');

const firebaseUrl = `${config.firebaseUrl}/users`;
const duration = workflow.input_period_duration;

const name = workflow.user_variable.first || 'unknown';

const data = {
  Name: name,
  Duration: duration,
  StartDate: '',
  EndDate: ''
};

await axios.patch(`${firebaseUrl}/${name}.json`, data);
