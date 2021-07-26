from __future__ import print_function
import os.path
import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions

#PATHS TO CHANGE FOR YOUR OWN USAGE (ONLY GETS EVENTS ON WEEKENDS DUE TO CURRENT DESIGN)
#  line 128 you need a file called credentials.json in current folder.  getting credentials can be found here https://developers.google.com/workspace/guides/create-credentials?authuser=3 
#       follow the instructions, download as json and move into folder containing this script and rename to credentials.json
#  line 68,69, your mcdonalds accound login details
#  line 58, path to your geckodriver.exe

    
def main():
    # bool for if we want to check next weeks schedule aswell
    nextWeek = False
    for index in range(0,1):
        if index == 0:
            work = get_times(nextWeek)
            event_creation(work, nextWeek)
        else:
            nextWeek = True
            work = get_times(nextWeek)
            event_creation(work, nextWeek)
    # end for
        
def get_dates(day):

    # if the day we're getting dates for is a saturday, 1 = saturday. 
    if day == 1:
        # gets todays date and stores it as d
        d = datetime.date.today() 
        # if today isnt a saturday then...
        if d.weekday() != 5:                    #weekday = 0, monday. 6, sunday
            # while it isnt saturday keep adding days until it is
            while d.weekday() != 5:
                d += datetime.timedelta(1)
            
            
    else:
        d = datetime.date.today()
        if d.weekday() != 6:
            while d.weekday() != 6:
                d += datetime.timedelta(1)

    print(d, day)    
    return d
        
        
def get_times(nextWeek):
    options = FirefoxOptions()
    options.add_argument("--headless")
    browser = webdriver.Firefox(executable_path=r'YOUR PATH TO THE GECKODRIVER EXE', options=options)
    
    # get url of the website
    browser.get('https://www.peoplestuffuk.com/WFMMCDPRD/Login.jsp')
    
    #find the login sections of the website
    username = browser.find_element_by_name("txtUserID")
    password = browser.find_element_by_name("txtPassword")
    workTimes = []
    
    username.send_keys("YOUR USERNAME")
    password.send_keys("YOUR PASSWORD")
    
    browser.find_element_by_id("Login_span").click()
    
    # get date of next saturday
    saturday = get_dates(1)
    saturday = saturday.strftime("%Y%m%d")
    print("saturday" + saturday)

    # get date of next sunday 
    sunday = get_dates(2)
    sunday = sunday.strftime("%Y%m%d")
    print("sunday " + sunday)
    
    
    #get the path to the saturday and sunday work times on the website
    workXpath = '//*[@id="shift_'
    saturdayXpath = (workXpath + str(saturday) + '"]')
    sundayXpath = (workXpath + str(sunday) + '"]')

    
    
    saturdayWorkId = browser.find_element_by_xpath(saturdayXpath)
    workTimes.append(saturdayWorkId.text)
    # print(saturdayWork)

    sundayWorkId = browser.find_element_by_xpath(sundayXpath)
    workTimes.append(sundayWorkId.text)
    browser.close()
    # print(sundayWork)
    
    
    return workTimes
    

        
def event_creation(workTimes, nextWeek):
    SCOPES = 'https://www.googleapis.com/auth/calendar'

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorisation flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    #if no credentials for the user, let the user log in 
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES) 
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    


    SaturdayWork = False
    SundayWork = False
    
    for index in range(0,2):
        if not workTimes[index] == " ":
            workTimes[index] = workTimes[index].replace("-", "" )
            if index == 0:
                Saturday = workTimes[0]
                startSaturday = Saturday[1:6]
                startSaturday += ":00"
                endSaturday = Saturday[6:12]
                endSaturday += ":00"
                SaturdayWork = True
            else:
                Sunday = workTimes[1]
                startSunday = Sunday[1:6]
                startSunday += ":00"
                endSunday = Sunday[6:12]
                endSunday += ":00"
                SundayWork = True
        else:
            continue

    saturday = get_dates(1)
    sunday = get_dates(2)
    
    

    GMT_ON = '+00:00'
    for index in range(0,2):
        # add the details for the shifts and as events on google calendar for saturday
        if index == 0:
            if SaturdayWork:
                startSaturday = (str(saturday) + 'T' + str(startSaturday) + '%s')
                endSaturday = (str(saturday) + 'T' + str(endSaturday) + '%s')
                event = {
                    'summary': 'Work',
                    'start': {
                        'dateTime': (startSaturday) % GMT_ON,
                    },
                    'end': {
                        'dateTime': (endSaturday) % GMT_ON,
             
                    }
                }
            
                event = service.events().insert(calendarId='primary', body=event).execute()
                print ('Event created: %s' % (event.get('htmlLink')))
            
            else:
                continue
        # add the details for the shifts and as events on google calendar for sunday
        if index == 1:
            if SundayWork:
                startSunday = (str(sunday) + 'T' + str(startSunday) + '%s')
                endSunday = (str(sunday) + 'T' + str(endSunday) + '%s')
                event = {
                    'summary': 'Work',
                    'start': {
                        'dateTime': (startSunday) % GMT_ON,
                    },
                    'end': {
                        'dateTime': (endSunday) % GMT_ON,
             
                    }
                }
                
                event = service.events().insert(calendarId='primary', body=event).execute()
                print ('Event created: %s' % (event.get('htmlLink')))
    
if __name__ == '__main__':
    main()