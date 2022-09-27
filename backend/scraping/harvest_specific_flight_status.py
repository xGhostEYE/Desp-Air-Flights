from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import date

Airline_code = 'AC'
Flight_number = '8073'
today = date.today()
Date = today.strftime("%d")
Month = today.strftime("%m")
Year = today.strftime("%Y")

print()
# url = "https://www.flightstats.com/v2/flight-tracker/"+Airline_code + \
#     "/"+Flight_number+"?year="+Year+"&month="+Month+"&date="+Date
url = "https://www.flightstats.com/v2/flight-tracker/AC/8073?year=2022&month=09&date=06&flightId=1108574561"
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
# departure_location = soup.find('div', attrs={'class':'text-helper__TextHelper-sc-8bko4a-0 efwouT'})
# arrival_location = soup.findNext('div', attrs={'class':'text-helper__TextHelper-sc-8bko4a-0 efwouT'})
# flight_status = soup.find('div', attrs={'class':'text-helper__TextHelper-sc-8bko4a-0 feVjck'})
# arrival_time = soup.find('div', attrs={'class':'text-helper__TextHelper-sc-8bko4a-0 kbHzdx'})
# departure_time = soup.findNext('div', attrs={'class':'text-helper__TextHelper-sc-8bko4a-0 kbHzdx'})
# arrival_time_actual = soup.findNext('div', attrs={'class':'text-helper__TextHelper-sc-8bko4a-0 kbHzdx'})
# departure_time_actual = soup.findNext('div', attrs={'class':'text-helper__TextHelper-sc-8bko4a-0 kbHzdx'})
# departure_terminal = soup.find('div', attrs={'class':'ticket__TGBValue-sc-1rrbl5o-16 hUgYLc text-helper__TextHelper-sc-8bko4a-0 kbHzdx'})
# departure_gate = soup.findNext('div', attrs={'class':'ticket__TGBValue-sc-1rrbl5o-16 hUgYLc text-helper__TextHelper-sc-8bko4a-0 kbHzdx'})
# arrival_terminal = soup.findNext('div', attrs={'class':'ticket__TGBValue-sc-1rrbl5o-16 hUgYLc text-helper__TextHelper-sc-8bko4a-0 kbHzdx'})
# arrival_gate = soup.findNext('div', attrs={'class':'ticket__TGBValue-sc-1rrbl5o-16 hUgYLc text-helper__TextHelper-sc-8bko4a-0 kbHzdx'})

# print("departure_location: ",departure_location.get_text())
# print("arrival_location: ",arrival_location.get_text())
# print("flight_status: ",flight_status.get_text())
# print("arrival_time: ",arrival_time.get_text())
# print("departure_time: ",departure_time.get_text())
# print("arrival_time_actual: ",arrival_time_actual.get_text())
# print("departure_time_actual: ",departure_time_actual.get_text())
# print("departure_terminal: ",departure_terminal.get_text())
# print("departure_gate: ",departure_gate.get_text())
# print("arrival_terminal: ",arrival_terminal.get_text())
# print("arrival_gate: ",arrival_gate.get_text())
