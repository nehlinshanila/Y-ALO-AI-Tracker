const axios = require('axios');
const config = require('./config');

const apiKey = config.googleApiKey;
const firebaseUrl = config.firebaseUrl;

async function findGynecologists(city) {
  const encodedCity = encodeURIComponent(city);
  const url = `https://maps.googleapis.com/maps/api/place/textsearch/json?query=gynecologists+in+${encodedCity}&key=${apiKey}`;

  try {
    const response = await axios.get(url);
    if (response.data.results.length > 0) {
      return response.data.results.map((place) => `${place.name}, located at ${place.formatted_address}`).join('\n');
    } else {
      return 'No gynecologists found in the specified area.';
    }
  } catch (error) {
    console.error('API request failed:', error);
    return 'Failed to fetch data. Please try again later.';
  }
}

const details = await findGynecologists(event.state.workflow.doctor);
const message = `Here are the gynecologists found in ${event.state.workflow.doctor}:\n${details}`;
const payloads = event.bp.cms.renderElement('builtin_text', { text: message, typing: true }, event);
event.bp.events.replyToEvent(event, payloads);
