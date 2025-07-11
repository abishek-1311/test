import requests

BASE_URL = "http://127.0.0.1:8065" 

def get_root():
    response = requests.get(f"{BASE_URL}/")
    print("GET / Response:")
    print(response.json())

def create_booking():
    customer_name = input("Enter customer name: ")
    vehicle_number = input("Enter vehicle number: ")
    service_type = input("Enter service type: ")
    booking_date = input("Enter booking date (YYYY-MM-DD): ")
    payload = {
        "customer_name": customer_name,
        "vehicle_number": vehicle_number,
        "service_type": service_type,
        "booking_date": booking_date
    }
    response = requests.post(f"{BASE_URL}/bookings/", json=payload)
    print("POST /bookings/ Response:")
    print(response.json())

def get_all_bookings():
    response = requests.get(f"{BASE_URL}/bookings/get-all/")
    print("GET /bookings/ Response:")
    print(response.json())

def get_booking_by_id():
    booking_id = input("Enter booking ID: ")
    response = requests.get(f"{BASE_URL}/bookings/{booking_id}")
    print(f"GET /bookings/{booking_id} Response:")
    if response.status_code == 200:
        print(response.json())
    else:
        print(response.json())

def update_booking():
    booking_id = input("Enter booking ID: ")
    print("Leave a field blank if you don't want to update it.")
    
    # Prompt the user for updates
    customer_name = input("Enter updated customer name: ").strip()
    vehicle_number = input("Enter updated vehicle number: ").strip()
    service_type = input("Enter updated service type: ").strip()
    booking_date = input("Enter updated booking date (YYYY-MM-DD): ").strip()
    
    # Dynamically construct the payload with only non-empty fields
    payload = {}
    if customer_name:
        payload["customer_name"] = customer_name
    if vehicle_number:
        payload["vehicle_name"] = vehicle_number
    if service_type:
        payload["service_type"] = service_type
    if booking_date:
        payload["booking_date"] = booking_date

    # Check if there's anything to update
    if not payload:
        print("No fields to update. Exiting.")
        return

    # Send the PUT request with the partial payload
    response = requests.put(f"{BASE_URL}/bookings/{booking_id}", json=payload)
    print(f"PUT /bookings/{booking_id} Response:")
    
    # Handle the response
    if response.status_code == 200:
        print("Booking updated successfully:", response.json())
    else:
        print("Error updating booking:", response.json())

def delete_booking():
    booking_id = input("Enter booking ID to delete: ")
    response = requests.delete(f"{BASE_URL}/bookings/{booking_id}")
    print(f"DELETE /bookings/{booking_id} Response:")
    if response.status_code == 204:  # No Content
        print("Booking deleted successfully.")
    else:
        try:
            print(response.json())
        except requests.exceptions.JSONDecodeError:
            print("No JSON response returned by the server.")

def main():
    while True:
        print("\n--- Vehicle Service Centre API ---")
        print("1. Get root response")
        print("2. Create a new booking")
        print("3. Get all bookings")
        print("4. Get a booking by ID")
        print("5. Update a booking")
        print("6. Delete a booking")
        print("7. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            get_root()
        elif choice == "2":
            create_booking()
        elif choice == "3":
            get_all_bookings()
        elif choice == "4":
            get_booking_by_id()
        elif choice == "5":
            update_booking()
        elif choice == "6":
            delete_booking()
        elif choice == "7":
            print("Exiting the application. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
