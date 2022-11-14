for i in range(len(data_seperated)):
    booking_info = data_seperated[i].split('$')[0]
    time_departure = booking_info.split('–')[0]
    time_departure = time_departure.replace(' ','')
    in_time = datetime.strptime(time_departure, "%I:%M %p")
    out_time = datetime.strftime(in_time, "%H:%M")
    departure_time.append(out_time)
    time_arrival = booking_info.split(' ')[1]
    time_arrival_remaining = booking_info.split(' ')[2]
    timething = time_arrival[3:]+time_arrival_remaining[:2]
    in_time = datetime.strptime(timething, "%I:%M %p")
    out_time = datetime.strftime(in_time, "%H:%M")
    arrival_time.append(out_time)
    price = data_seperated[i].split('$')[1]
    price = price.split(' ')[0]
    prices.append('$'+price)
    airline = booking_info.split('nonstop')[0]
    print(airline)
    airline_remaining = airline.split(":", 2)[2]
    airlines.append(airline_remaining[5:])