# McDonalds Shifts to Calendar Events
Gets shift start and end data from Mcdonalds shift website and adds as events to google calendar. Uses Selenium to scrape the data from the website and the google calendar api to add to your calendar.

(only works for saturday and sunday, can easily be expanded for all days of the week)

## Usage
- install all the required python modules. pip commands for google api here  
https://developers.google.com/calendar/api/quickstart/python    
- get credentials from google, saved as credentials.json with get_times.py. instructions found here:
https://developers.google.com/workspace/guides/create-credentials   
- change specific lines specified at start of get_times.py file