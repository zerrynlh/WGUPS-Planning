from datetime import datetime, timedelta
from classes import Truck
import csv
from classes import Package

def calculate_priority(deadline):
    """O(1) time complexity"""
    # Assign priority based on delivery deadline
    priority = 0
    if deadline == "10:30 AM":
        priority += 1
    elif deadline == "EOD":
        priority += 5
    
    return priority

def get_note(the_note):
    """O(1)"""
    if the_note == None:
        return None
    else:
        return str(the_note)
    
def insert_package(package_table, package):
    """ O(1) time complexity """
    package_table[package.package_id] = package

def lookup_package(package_table, package_id):
    """ O(1) time complexity """
    result = package_table.get(package_id, "Package not found")
    print(result)
    
def find_package(pk_table, target_id):
    """O(1)"""
    try:
        the_pkg = pk_table[target_id]
        return the_pkg.get_pickup_status()
    except KeyError:
        return None
    
def load_packages(truck, the_queue):
    """O(N) complexity"""
    for package_id, package in the_queue.items():

        if truck.get_num_packages() >= 16:
            break
        if package.check_status() == "At hub":
            # Address update for package 9
            if package.package_id == 9 and truck.current_time >= datetime.strptime("10:20 AM", "%I:%M %p"):
                package.address == "401 S State St"
                package.zip_code == 84111

            # Constraints
            if package.note and "Can only be on truck 2" in package.note and truck.truck_id != 2:
                continue
            if package.note and "Delayed on flight" in package.note and truck.current_time < datetime.strptime("9:05 AM", "%I:%M %p"):
                # Delay package until 9:05 AM
                continue
            if package.package_id == 9 and truck.current_time < datetime.strptime("10:20 AM", "%I:%M %p"):
                # Defer package #9 until 10:20AM for correct address
                continue
            if package.package_id in [13, 14, 15, 16, 18, 19, 20, 36, 38] and truck.truck_id != 2:
            # Ensure packages are delivered together and for packages that can only be on truck 2
                continue

            # Load package onto truck
            if truck.get_num_packages() < 16:
                cur_truck_time = truck.current_time
                package.pickup_time = cur_truck_time
                package.truck_id = truck.truck_id
                truck.load_package(package)
                truck.delivered += 1

            #print(f"""Loading package {package.package_id} onto truck {truck.truck_id} at {cur_truck_time.time()}""")
    
# Select next package using greedy approach based on priority then distance   
def select_next_package(truck, dist_table):
    """O(N) complexity"""
    current_location = truck.get_location()
    nearest_package = None
    min_distance = float('inf')
    highest_priority = float('inf')

    for package in truck.packages:
        package = package[2]
        # Account for blank values
        try:
            distance = dist_table[current_location][package.address]
        except KeyError:
            pass

        if distance == "":
            distance = dist_table[package.address][current_location]
        
        # Convert str from dictionary
        distance = float(distance)

        # First, check if the package has a higher priority (lower priority value)
        if package.priority < highest_priority:
            highest_priority = package.priority
            nearest_package = package
            min_distance = distance
        # If priorities are equal, choose the package with the shortest distance
        elif package.priority == highest_priority and distance < min_distance:
            nearest_package = package
            min_distance = distance

    return nearest_package

def deliver_package(truck, package, dist_table, package_table):
    """O(1) complexity, all constant time operations and no loops"""
    # Account for blank values
    try:
        distance = dist_table[truck.current_location][package.address]
    except KeyError:
        pass

    if distance == "":
        distance = dist_table[package.address][truck.current_location]
    
    distance = float(distance)
    
    # Simulate delivery time
    travel_time = round(distance / truck.speed, 2)
    truck.set_time(timedelta(hours=travel_time))
    truck.traveled += distance

    #Update package status in hast table
    cur_time = truck.current_time
    package_table[package.package_id].set_dropoff_time(cur_time)
    package_table[package.package_id].set_status("Delivered")

    truck.drop_off_package(package, cur_time)
    truck.set_location(package.address)

    #print(f"""Truck {truck.truck_id} delivered package {package.package_id} to {package.address} at {truck.current_time.time()}.""")

def greedy_delivery_algorithm(package_queue, distance_table, trucks, start_time = None, end_time = None):
    """Process consist of:
        O(N) for first loop
        O(N^2) for second loop
        O(N) for the third loop
        O(N) for the 4th and 5th while loop
        Making this function O(N^2) time complexity"""
    
    # Get time input from UI
    if start_time and end_time:
        trucks = [
        Truck(1, datetime.strptime("8:00 AM", "%I:%M %p")),
        Truck(2, datetime.strptime("8:00 AM", "%I:%M %p")),
        Truck(3, datetime.strptime("8:00 AM", "%I:%M %p")),
    ]
        try:
            start_time_obj = datetime.strptime(start_time, "%I:%M %p").time()
            end_time_obj = datetime.strptime(end_time, "%I:%M %p").time()
        except ValueError:
        # Handle incorrect input format
            print("Invalid time format. Please enter a time in the format 'HH:MM AM/PM'.")

    # Load packages onto trucks
    for truck in trucks[:2]:
        load_packages(truck, package_queue)

    # If a time was entered, store packages not on trucks for printing status
    on_truck = []

    # Deliver packages using a greedy approach
    for truck in trucks[:2]:
        while truck.packages and truck.traveled < 140:
            # Greedy selection logic based on distance
            if end_time and truck.current_time.time() > end_time_obj:
                break

            # Check if query_time is reached for the current truck
            if start_time and end_time and start_time_obj <= truck.current_time.time() <= end_time_obj:
                for i, j, pkg in truck.packages:
                    print(f"Package: {pkg.package_id}, Status: {pkg.status}, Truck: {pkg.truck_id}, Delivered at: {pkg.drop_off_time.time() if pkg.drop_off_time else 'Not delivered'}, Deadline: {pkg.deadline}, Address: {pkg.address}")
                    on_truck.append(pkg.package_id) # Add package ID to list of picked up packages
                break  # Stop this truck's deliveries, but continue with the other trucks

            # If it is past 9:05 AM and packages 6 and 25 are at the HUB, return to the hub
            if truck.current_time >= datetime.strptime("9:05 AM", "%I:%M %p") and (find_package(package_queue, 6) == False or find_package(package_queue, 25) == False):
                if truck.truck_id == 2:
                    truck.return_to_hub(truck.current_location, distance_table)
                    load_packages(truck, package_queue)
            # If it is past 10:20 AM and package 9 is at the hub, return to HUB
            if truck.current_time >= datetime.strptime("10:20 AM", "%I:%M %p") and find_package(package_queue, 9) == False:
                if truck.truck_id == 2:
                    truck.return_to_hub(truck.current_location, distance_table)
                    load_packages(truck, package_queue)
            next_package = select_next_package(truck, distance_table)
            deliver_package(truck, next_package, distance_table, package_queue)
        # Return to hub if no packages on the truck
        truck.return_to_hub(truck.current_location, distance_table)

    # Get most recent truck that returned
    truck_time = datetime.strptime("5:00 PM", "%I:%M %p")
    for truck in trucks[:2]:
        if truck.current_time < truck_time:
            truck_time = truck.current_time

    # Set truck 3's depart time to most recent truck's arrival
    truck_3_depart_time = datetime.combine(datetime.today(), truck_time.time())
    truck_3 = trucks[2]
    truck_3.current_time = truck_3_depart_time

    # Begin loading truck 3
    if not trucks[0].packages and trucks[1].packages:
        load_packages(truck_3, package_queue)

    while truck_3.packages:
        if end_time and trucks[2].current_time.time() > end_time_obj:
            break

        if start_time and end_time and start_time_obj <= trucks[2].current_time.time() <= end_time_obj:
            for i, j, pkg in truck_3.packages:
                print(f"Package: {pkg.package_id}, Status: {pkg.status}, Truck: {pkg.truck_id}, Delivered at: {pkg.drop_off_time.time() if pkg.drop_off_time else 'Not delivered'}, Deadline: {pkg.deadline}, Address: {pkg.address}")
                on_truck.append(pkg.package_id) # Add package ID to list of picked up packages

        next_package = select_next_package(truck_3, distance_table)
        deliver_package(truck_3, next_package, distance_table, package_queue)

    # If a time was entered and there are remaining packages that are not on trucks, print them
    if start_time and end_time:
        for id, pkg in package_queue.items():
            if id not in on_truck:
                print(f"Package: {pkg.package_id}, Status: {pkg.status}, Truck: {pkg.truck_id}, Delivered at: {pkg.drop_off_time.time() if pkg.drop_off_time else 'Not delivered'}, Deadline: {pkg.deadline}, Address: {pkg.address}")
        return

    truck_3.return_to_hub(truck_3.current_location, distance_table)

    print("Remaining packages to deliver:", (sum(i.get_num_packages() for i in trucks)))
    print("Final truck stats:")
    for truck in trucks:
        print(truck)

# CLI to view package status and truck mileage
def user_interface(package_table, trucks):
    while True:
        print("\n1. Look up package")
        print("2. View total truck mileage")
        print("3. Check package status at a specific time")
        print("4. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            package_id = int(input("Enter package ID: "))
            lookup_package(package_table, package_id)
        elif choice == "2":
            print('\n')
            total_miles = round(sum(truck.traveled for truck in trucks), 2)
            print(f"Total truck mileage: {total_miles}")
        elif choice == "3":
            # Reinitialize trucks without affecting main state
            new_trucks = [
                    Truck(1, datetime.strptime("8:00 AM", "%I:%M %p")),
                    Truck(2, datetime.strptime("8:00 AM", "%I:%M %p")),
                    Truck(3, datetime.strptime("8:00 AM", "%I:%M %p")),
                ]
            
            while True:
                start_input = input("Enter a start time (e.g., 10:00 AM): ")
                try:
                    start = datetime.strptime(start_input, "%I:%M %p").time()
                    break
                except ValueError:
                    print("Please enter a valid start time.")

            while True: 
                end_input = input("Enter an end time (e.g., 12:00 PM): ")
                try:
                    end = datetime.strptime(end_input, "%I:%M %p").time()
                    break
                except ValueError:
                    print("Please enter a valid end time.")
                
            print(f"Package status between {start_input} and {end_input}")
            #Rerun simulation using time arguments and new package table and distance dictionary each time
            greedy_delivery_algorithm(read_packages(), read_distance(), new_trucks, start_input, end_input)
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

def read_distance():
    # Read in distance table
    with open ('distance_table.csv') as dist_table:
        """O(N^2) complexity"""
        dist_file = csv.reader(dist_table)

        # Read the header rows and extract just the address
        locations = [i.split('\n')[1].strip() for i in next(dist_file)[1:]]

        # Initialize distance matrix
        dist_dict = {loc: {} for loc in locations}
        
        # Populate the distance matrix
        for row in dist_file:
            # Split column locations by space to obtain address
            current_location = row[0].replace(",", "").split("\n")[0].strip()
            distances = []
            for value in row[1:]:
                if value is not None:
                    distances.append(value)
            dist_dict[current_location] = dict(zip(locations, distances))

    # Correct address in dictionary
    dist_dict['5383 South 900 East #104'] = dist_dict.pop('5383 S 900 East #104')

    return dist_dict

def read_packages():
    # Initialize hash table for packages
    package_table = {}

    with open('package_file.csv') as package_file:
        """O(N) complexity"""
        csv_reader = csv.reader(package_file)
        # Skip first empty row
        next(csv_reader, None)
        for row in csv_reader:
            # Create Package object
            new_package = Package(int(row[0]), row[1], row[2], row[3], int(row[4]), 
                                row[5], float(row[6]), calculate_priority(row[5]), get_note(row[7]))
            insert_package(package_table, new_package)

    print(f"{len(package_table)} packages read.")

    return package_table