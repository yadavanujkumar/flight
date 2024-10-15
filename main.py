
import tkinter as tk
from tkinter import messagebox
from db_manager import DBManager
from flight_manager import FlightManager
from user_manager import UserManager
from tkinter import simpledialog

class FlightBookingApp:
    def __init__(self, root):
        self.db = DBManager()
        self.flight_manager = FlightManager(self.db)
        self.user_manager = UserManager(self.db)
        self.root = root
        self.root.title("Flight Booking System")
        self.root.geometry("400x400")
        
        # Create a container frame for all pages
        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)

        # Create the different pages
        self.pages = {}
        for Page in (HomePage, FlightPage, UserPage):
            page_name = Page.__name__
            frame = Page(parent=self.container, controller=self)
            self.pages[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_page("HomePage")

    def show_page(self, page_name):
        """Show a frame for the given page name."""
        frame = self.pages[page_name]
        frame.tkraise()

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="Welcome to the Anuj ka Flight Booking System", font=("Helvetica", 16)).pack(pady=20)

        tk.Button(self, text="Manage Flights", command=lambda: controller.show_page("FlightPage")).pack(pady=10)
        tk.Button(self, text="Manage Users", command=lambda: controller.show_page("UserPage")).pack(pady=10)

class FlightPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Flight Management", font=("Helvetica", 14)).grid(row=0, column=0, columnspan=2, pady=10)

        # Flight ID Input
        tk.Label(self, text="Flight ID:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_flight_id = tk.Entry(self)
        self.entry_flight_id.grid(row=1, column=1, padx=5, pady=5)

        # Origin Input
        tk.Label(self, text="Origin:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_origin = tk.Entry(self)
        self.entry_origin.grid(row=2, column=1, padx=5, pady=5)

        # Destination Input
        tk.Label(self, text="Destination:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.entry_destination = tk.Entry(self)
        self.entry_destination.grid(row=3, column=1, padx=5, pady=5)

        # Seats Input
        tk.Label(self, text="Seats:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.entry_seats = tk.Entry(self)
        self.entry_seats.grid(row=4, column=1, padx=5, pady=5)

        # Add Flight Button
        tk.Button(self, text="Add Flight", command=self.add_flight).grid(row=5, column=0, columnspan=2, pady=10)

        # View Flights Button
        tk.Button(self, text="View All Flights", command=self.view_flights).grid(row=6, column=0, columnspan=2, pady=10)

        # Back Button
        tk.Button(self, text="Back to Home", command=lambda: self.controller.show_page("HomePage")).grid(row=7, column=0, columnspan=2, pady=10)

    def add_flight(self):
        flight_id = self.entry_flight_id.get()
        origin = self.entry_origin.get()
        destination = self.entry_destination.get()
        seats = self.entry_seats.get()

        if flight_id and origin and destination and seats.isdigit():
            self.controller.flight_manager.add_flight(flight_id, origin, destination, int(seats))
            messagebox.showinfo("Success", "Flight added successfully!")
        else:
            messagebox.showerror("Error", "Please enter valid flight details.")

    def view_flights(self):
        flights = self.controller.flight_manager.get_all_flights()
        flight_info = "\n".join(
            f"Flight ID: {flight['flight_id']}, Origin: {flight['origin']}, "
            f"Destination: {flight['destination']}, Available Seats: {flight['available_seats']}"
            for flight in flights
        )
        messagebox.showinfo("Available Flights", flight_info or "No flights available.")

class UserPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="User Management", font=("Helvetica", 14)).grid(row=0, column=0, columnspan=2, pady=10)

        # User ID Input
        tk.Label(self, text="User ID:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_user_id = tk.Entry(self)
        self.entry_user_id.grid(row=1, column=1, padx=5, pady=5)

        # User Name Input
        tk.Label(self, text="User Name:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_user_name = tk.Entry(self)
        self.entry_user_name.grid(row=2, column=1, padx=5, pady=5)

        # Add User Button
        tk.Button(self, text="Add User", command=self.add_user).grid(row=3, column=0, columnspan=2, pady=10)

        # Book Flight Button
        tk.Button(self, text="Book Flight", command=self.prompt_for_destination).grid(row=4, column=0, columnspan=2, pady=10)

        # View User Bookings Button
        tk.Button(self, text="View User Bookings", command=self.view_user_bookings).grid(row=5, column=0, columnspan=2, pady=10)

        # Back Button
        tk.Button(self, text="Back to Home", command=lambda: self.controller.show_page("HomePage")).grid(row=6, column=0, columnspan=2, pady=10)

    def add_user(self):
        user_id = self.entry_user_id.get()
        user_name = self.entry_user_name.get()

        if user_id and user_name:
            self.controller.user_manager.add_user(user_id, user_name)
            messagebox.showinfo("Success", "User added successfully!")
        else:
            messagebox.showerror("Error", "Please enter a valid User ID and Name.")

    def prompt_for_destination(self):
        """Ask the user for their desired destination and check for available flights."""
        user_id = self.entry_user_id.get()

        if not user_id:
            messagebox.showerror("Error", "Please enter a valid User ID.")
            return

        # Prompt the user to enter the desired destination.
        destination = tk.simpledialog.askstring("Destination", "Enter the destination you want to travel to:")

        if destination:
            # Check for available flights to the entered destination.
            available_flights = self.controller.flight_manager.get_flights_by_destination(destination)
            if available_flights:
                self.select_flight_to_book(user_id, available_flights)
            else:
                messagebox.showinfo("No Flights", f"No available flights to {destination}.")
        else:
            messagebox.showerror("Error", "Please enter a valid destination.")

    def select_flight_to_book(self, user_id, available_flights):
        """Allow the user to select a flight from available options."""
        flight_list = "\n".join(
            f"{idx + 1}. Flight ID: {flight['flight_id']}, Origin: {flight['origin']}, "
            f"Available Seats: {flight['available_seats']}"
            for idx, flight in enumerate(available_flights)
        )
        selection_prompt = f"Available flights to the destination:\n\n{flight_list}\n\nEnter the flight number to book:"

        flight_choice = tk.simpledialog.askinteger("Choose Flight", selection_prompt)

        if flight_choice and 1 <= flight_choice <= len(available_flights):
            selected_flight = available_flights[flight_choice - 1]['flight_id']
            self.book_flight(user_id, selected_flight)
        else:
            messagebox.showerror("Error", "Invalid selection. Please try again.")

    def book_flight(self, user_id, flight_id):
        """Book the selected flight for the user."""
        success = self.controller.user_manager.book_flight(user_id, flight_id)
        if success:
            messagebox.showinfo("Success", "Flight booked successfully!")
        else:
            messagebox.showerror("Error", "Failed to book flight. No seats available or flight not found.")

    def view_user_bookings(self):
        user_id = self.entry_user_id.get()

        if user_id:
            bookings = self.controller.user_manager.get_user_bookings(user_id)
            booking_info = "\n".join(f"Flight ID: {booking['flight_id']}" for booking in bookings)
            messagebox.showinfo("User Bookings", booking_info or "No bookings found for this user.")
        else:
            messagebox.showerror("Error", "Please enter a valid User ID.")

if __name__ == '__main__':
    root = tk.Tk()
    app = FlightBookingApp(root)
    root.mainloop()
