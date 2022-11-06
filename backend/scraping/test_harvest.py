import harvest_flights as harv

if __name__ == "__main__":

    Airport = "YYC"

    arrivals = harv.harvest_data_arrivals(Airport)
    dep = harv.harvest_data_departures(Airport, None)

    arrivals.to_csv(f"./__data/test_harvest/{Airport}_arrivals.csv", index=False)
    dep.to_csv(f"./__data/test_harvest/{Airport}_dep.csv", index=False)