from flight_manager import FlightManager

class UserManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def add_user(self, user_id, name):
        user = {
            "user_id": user_id,
            "name": name
        }
        return self.db_manager.users.insert_one(user)

    def book_flight(self, user_id, flight_id):
        # Use FlightManager to handle seat booking
        flight_manager = FlightManager(self.db_manager)
        success = flight_manager.book_seat(flight_id)
        if success:
            # Create booking record if seat booking is successful
            booking = {
                "user_id": user_id,
                "flight_id": flight_id
            }
            self.db_manager.bookings.insert_one(booking)
            return True
        return False

    def get_user_bookings(self, user_id):
        return list(self.db_manager.bookings.find({"user_id": user_id}))
