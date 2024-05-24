const axios = require('axios');
const config = require('./config');
const { DateTime } = require('luxon');

const name = workflow.user_variable.first || 'unknown';
const firebaseUrl = `${config.firebaseUrl}/users/${name}.json`;

const date_result = workflow.p_date;
console.log('date: ', date_result);

let currentDate;

if (date_result === 'Today') {
  currentDate = DateTime.now().toFormat('MM/dd/yyyy');
  console.log('The current date is:', currentDate);
} else {
  currentDate = DateTime.fromJSDate(workflow.input_period_date).toFormat('MM/dd/yyyy');
  console.log('another date', currentDate);
}

await axios.patch(firebaseUrl, { date: currentDate, duration: workflow.input_period_duration });
