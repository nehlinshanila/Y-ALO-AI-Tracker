const { DateTime } = require('luxon');
const axios = require('axios');
const config = require('./config');

const firebaseUrl = `${config.firebaseUrl}`;

const currentDate = DateTime.now().toFormat('MM/dd/yyyy');
console.log('The current date is:', currentDate);

const showDate = DateTime.fromFormat(currentDate, 'MM/dd/yyyy').plus({ days: 28 }).toFormat('MM/dd/yyyy');
console.log('Date after adding 28 days:', showDate);

workflow.show_date = showDate;

try {
  await axios.patch(firebaseUrl, {
    date: currentDate,
    duration: workflow.input_period_duration,
    show_date: showDate
  });
} catch (error) {
  console.error('Error executing action:', error.message);
}
