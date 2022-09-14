from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import date

Airline_code = 'WS'
Flight_number = '289'
today = date.today()
Date = today.strftime("%d")
Month = today.strftime("%m")
Year = today.strftime("%Y")

# url = "https://www.flightstats.com/v2/flight-tracker/"+Airline_code + \
#     "/"+Flight_number+"?year="+Year+"&month="+Month+"&date="+Date
url = "https://www.flightstats.com/v2/flight-tracker/"+Airline_code+"/"+Flight_number+"?year=2022&month=9&date=12"
page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")


departure_location = ""
arrival_location = ""
flight_status = ""
arrival_time = ""
departure_time = ""
arrival_time_actual = ""
departure_time_actual = ""
departure_terminal = ""
departure_gate = ""
arrival_terminal = ""
arrival_gate = ""



divs = soup.findAll(class_="ticket__TicketCard-sc-1rrbl5o-7 WlxJD")
lis = list(soup.find_all('div', attrs={'class': 'ticket__TicketContent-sc-1rrbl5o-6 hiMpVc'})[0].parent.children)
for i in range(len(lis)):
    print(lis[i].get_text())

