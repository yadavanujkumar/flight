from pymongo import MongoClient

class DBManager:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="flight_booking"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.flights = self.db['flights']
        self.bookings = self.db['bookings']
        self.users = self.db['users']

    def close_connection(self):
        self.client.close()
