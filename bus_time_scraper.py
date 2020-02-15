import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import sched, time

# Generates Python request using cURL data from FirstGroup website

cookies = {
    'FGRecentOpcos': '%7B%22%5C%2Fbristol-bath-and-west%22%3A%22Bristol%2C+Bath+and+the+West%22%7D',
    'SSESS86a0200f54bd0a2b1386bbbaa2dd96e1': 'E08TrBjvpSTnhgR8ymvxDS8nvDNGvx4g8AIswEDTx1w',
    '_gcl_au': '1.1.77503274.1581016824',
    '_ga': 'GA1.2.1400901066.1581016824',
    'has_js': '1',
    'geo_loc_warn': '1',
    'FGCookies': '1',
    '_fbp': 'fb.1.1581016991326.614263981',
    'FGBogoSurveyMini': 'i',
    'com.firstgroup.first.bus-smartbanner-closed': 'true',
    'idsession': '600147184',
    'geo_Bristol': '51.454513%2C-2.58791',
    '_gid': 'GA1.2.2039314023.1581526748',
    'geo_College_Green': '51.45174%2C-2.6008429',
    'geo_Clifton_Down': '51.4693402%2C-2.6259781',
    'geo_loc_state': '3',
    '_gat_UA-16282823-3': '1',
    'geo_Clifton_Down_Station': '51.4644699%2C-2.6126211',
    'current_loc': '51.4644699,-2.6126211',
    'AWSALB': '1cMxuwLH7ymOGJ9nb0NfAMfhbwNqBoxiVbJeI7kvUSUgOjnYYPJ7S5xAMNuNB7fv+q8qWjynUNCxupaSYIkGIFZ62PKs9k/yTW4VeUCjuZd0VrOr/qlnbQxUuzHt',
    'AWSALBCORS': '1cMxuwLH7ymOGJ9nb0NfAMfhbwNqBoxiVbJeI7kvUSUgOjnYYPJ7S5xAMNuNB7fv+q8qWjynUNCxupaSYIkGIFZ62PKs9k/yTW4VeUCjuZd0VrOr/qlnbQxUuzHt',
}

headers = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Sec-Fetch-Dest': 'empty',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Mobile Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://www.firstgroup.com',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Referer': 'https://www.firstgroup.com/bristol-bath-and-west/plan-journey/next-bus?location=Bristol',
    'Accept-Language': 'en-US,en;q=0.9',
}

data = {
  'stop': '0100BRP90990'
}

# Implements a general purpose event scheduler to collect data every 5 minutes

s = sched.scheduler(time.time, time.sleep)

# Main function to generate request and parse HTML data from network response

def main(sc):
	stop_name = "Clifton Down Station"
	print("Stop: ", stop_name)
	r = requests.post('https://www.firstgroup.com/getNextBus', headers=headers, cookies=cookies, data=data)
	now = datetime.now()
	time_requested = now.strftime("%H:%M:%S")
	print("Time Requested: ", time_requested, "\n")

# 	Parsing the network response into each service

	services = r.text.split('"times"')[1].split('{')
	services.pop(0)
	services.pop(-1)
	
# 	Generates CSV file to write data onto

	csv_file = open('Bus_Times.csv', 'a')
	csv_writer = csv.writer(csv_file)
	# csv_writer.writerow(['Time Requested', 'Service', 'Destination', 'Due'])
	
# 	A for loop which goes through the list of services and parses RTI data for each
	
	for i in services:
		service_number = i.split(',')[1].split(':')[1]
		service_number = service_number[1:-1]
		
		destination = i.split(':')[3]
		destination = destination[1:-7]
		
		time_due = i.split(',')[-4].split(':')[1]
		time_due = time_due[1:-1]
		
		print("Service:", service_number, ", Destination:", destination, ", Due:",time_due)
		
		csv_writer.writerow([time_requested, service_number, destination, time_due])
		
	csv_writer.writerow([])	
	csv_file.close()
	
# 	Begins time interval after function is called
	
	s.enter(120, 1, main, (sc,))
			
# if __name__ == "__main__":
# 	main()

# Continues to call function every 2 minutes until terminated
	
s.enter(120, 1, main, (s,))
s.run()