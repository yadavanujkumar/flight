class FlightManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def add_flight(self, flight_id, origin, destination, seats):
        flight = {
            "flight_id": flight_id,
            "origin": origin,
            "destination": destination,
            "seats": seats,
            "available_seats": seats
        }
        return self.db_manager.flights.insert_one(flight)

    def get_all_flights(self):
        return list(self.db_manager.flights.find())

    def find_flight(self, flight_id):
        return self.db_manager.flights.find_one({"flight_id": flight_id})

    def book_seat(self, flight_id):
        flight = self.find_flight(flight_id)
        if flight and flight['available_seats'] > 0:
            # Reduce available seats by 1
            self.db_manager.flights.update_one(
                {"flight_id": flight_id},
                {"$inc": {"available_seats": -1}}
            )
            return True
        return False

    def get_flights_by_destination(self, destination):
         """Retrieve flights with the specified destination."""
         flights = list(self.db_manager.flights.find({"destination": destination}))
         return flights
