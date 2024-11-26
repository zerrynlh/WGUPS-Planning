from classes import Truck
from datetime import datetime
from helpers import greedy_delivery_algorithm, user_interface, read_distance, read_packages

"""
Name: Zerryn Hogan
Student ID: 012207809
"""
# Read in distance matrix
dist_dict = read_distance()

# Load in packages
package_table = read_packages()

def create_trucks():
    # Initialize truck instances
    trucks = [
        Truck(1, datetime.strptime("8:00 AM", "%I:%M %p")),
        Truck(2, datetime.strptime("8:00 AM", "%I:%M %p")),
        Truck(3, datetime.strptime("8:00 AM", "%I:%M %p")),
    ]

    return trucks

trucks = create_trucks()

# Load trucks and deliver packages utilizing helper functions
greedy_delivery_algorithm(package_table, dist_dict, trucks)

print("\n")
print("User interface loading...")
# Call function for user to view package status or truck mileage
user_interface(package_table, trucks)