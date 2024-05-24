const moment = require('moment');

async function action(bp, event) {
  try {
    // Access the last period date from workflow variables
    const lastPeriodDateStr = event.state.session.sessionlastPeriodDate; // Correct variable access

    if (!lastPeriodDateStr) {
      throw new Error('Last period date not found in session variables.');
    }

    // Parse the date
    const lastPeriodDate = moment(lastPeriodDateStr, 'DD/MM/YYYY'); // Adjust the format to match your input

    if (!lastPeriodDate.isValid()) {
      throw new Error('Invalid date format. Please enter the date in DD/MM/YYYY format.');
    }

    // Calculate the estimated next period date
    const cycleLength = 28; // Typical cycle length in days
    const nextPeriodDate = lastPeriodDate.clone().add(cycleLength, 'days');
    const currentDate = moment();
    const daysLate = currentDate.diff(nextPeriodDate, 'days');

    let response = '';
    if (daysLate <= 0) {
      response = `Your next period is estimated to be on: ${nextPeriodDate.format('YYYY-MM-DD')}`;
    } else {
      response = `Your period is late by ${daysLate} days. Do you want to contact an OB-GYN?`;
    }

    // Send response to the user
    await bp.events.replyToEvent(event, [
      {
        type: 'text',
        text: response
      }
    ]);
  } catch (error) {
    // Log the error for debugging purposes
    console.error('Error in trackPeriod action:', error.message);

    // Respond with a generic error message
    await bp.events.replyToEvent(event, [
      {
        type: 'text',
        text: 'Sorry, an error occurred. Please try again later.'
      }
    ]);
  }
}

return action;
