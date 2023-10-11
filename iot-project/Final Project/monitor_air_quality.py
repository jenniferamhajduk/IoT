from serial import *
from sds011 import SDS011
import time
from datetime import datetime, date
import csv
from twilio.rest import Client

ser = Serial(port='/dev/ttyUSB0', baudrate=9600, parity=PARITY_NONE, stopbits=STOPBITS_ONE, bytesize=EIGHTBITS, timeout=1)
account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)

#Take Measurement
def takeMeasurement():

    today = date.today()
    current_time = datetime.now().strftime("%H:%M")

    data = []
    for index in range(0,10):
        datum = ser.read()
        data.append(datum)

    pmtwofive = int.from_bytes(b''.join(data[2:4]), byteorder='little')/10
    pmten = int.from_bytes(b''.join(data[4:6]), byteorder='little')/10

    text_message = "PM10 reading is: " + str(pmten) + " PM2.5 reading is: " + str(pmtwofive) + " This measurement was taken at: " + str(current_time)
    return(pmtwofive, pmten, text_message, today)

def saveResults(twofive, ten, day):

    with open('./results.csv', 'a', newline='\n') as r:
        writer = csv.writer(r)
        writer.writerow([twofive, ten, day])
        return

def sendTextMessage(text):
    message = client.messages \
    .create(
         body=text,
         from_ =  ,
         to = 
     )
    return(message.sid)

def main():

    while True:
        twopointfive, ten, text, day = takeMeasurement()
        saveResults(twopointfive, ten, day)
        sendTextMessage(text)
        time.sleep(60 * 60)

if __name__ == "__main__":
    main()
