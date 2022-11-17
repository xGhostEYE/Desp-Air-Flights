import add_airports
import connect_gdb as conGDB

def test_add_airport(city, code, gdb):
    add_airports.add_airport(city, code, gdb)
    

if __name__ == "__main__":
    testgdb = conGDB.connect_test_gdb()
