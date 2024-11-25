from datetime import datetime
from helpers import lookup_package, greedy_delivery_algorithm

time_periods = [
    (datetime.strptime("8:35 AM", "%I:%M %p"), datetime.strptime("9:35 AM", "%I:%M %p")),
    (datetime.strptime("9:35 AM", "%I:%M %p"), datetime.strptime("10:25 AM", "%I:%M %p")),
    (datetime.strptime("12:03 PM", "%I:%M %p"), datetime.strptime("1:12 PM", "%I:%M %p"))
]

def display_truck_status(time_period, package_table):
    """
    O(N^2) time complexity
    Display the status of all packages loaded onto each truck during the given time period.
    """
    start_time, end_time = time_period
    print(f"Package status between {start_time.time()} and {end_time.time()}:\n")

    for i in range(1, 4):
        print(f"Truck {i}:")
        for id, package in package_table.items():
            if package.truck_id == i and (start_time.time() <= package.pickup_time.time() <= end_time.time()):
                print(f"Package: {package.package_id}, Status: {package.status}, Time: {package.pickup_time.time()}, Truck: {package.truck_id}, Delivered at: {package.drop_off_time.time()}")
        print("\n")

def display_package_at_time(time_period, package_table):
    """
    O(N^2) time complexity
    Display the status of all packages loaded onto each truck during the given time period.
    """
    start_time = time_period
    print(f"Package status for packages at {start_time.time()}:\n")

    for i in range(1, 4):
        print(f"Truck {i}:")
        for id, package in package_table.items():
            if package.truck_id == i and start_time.time == package.pickup_time.time():
                print(f"Package: {package.package_id}, Status: {package.status}, Truck: {package.truck_id}, Delivered at: {package.drop_off_time.time()} to {package.address}")
        print("\n")
