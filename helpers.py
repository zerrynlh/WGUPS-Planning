from datetime import datetime, timedelta
import heapq
from classes import Truck

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
    
def find_package(package_queue, target_id):
    """O(N)"""
    for priority, package_id, package in package_queue:
        if package_id == target_id:
            return True
    return False
    
def load_packages(truck, the_queue, current_time):
    """While loop is O(N) complexity"""
    # Place to store deferred packages
    deferred_packages = []

    while len(truck.packages) < 16 and the_queue:
        package_p, id, package = heapq.heappop(the_queue)

        # Address update for package 9
        if package.package_id == 9 and truck.current_time >= datetime.strptime("10:20 AM", "%I:%M %p"):
            package.address == "401 S State St"
            package.zip_code == 84111

        # Constraints
        if package.note and "Can only be on truck 2" in package.note and truck.truck_id != 2:
            # Reinsert package if not on truck 2
            if package not in [pkg[2] for pkg in deferred_packages]:
                deferred_packages.append((package_p, id, package))
                continue
        if package.note and "Delayed on flight" in package.note and truck.current_time < datetime.strptime("9:05 AM", "%I:%M %p"):
            # Delay package until 9:05 AM
            if package not in [pkg[2] for pkg in deferred_packages]:
                deferred_packages.append((package_p, id, package))
                continue
        if package.package_id == 9 and truck.current_time < datetime.strptime("10:20 AM", "%I:%M %p"):
            # Defer package #9 until 10:20AM for correct address
            if package not in [pkg[2] for pkg in deferred_packages]:
                deferred_packages.append((package_p, id, package))
                continue
        if package.package_id in [13, 14, 15, 16, 18, 19, 20, 36, 38] and truck.truck_id != 2:
            # Ensure packages are delivered together and for packages that can only be on truck 2
            if package not in [pkg[2] for pkg in deferred_packages]:
                deferred_packages.append((package_p, id, package))
                continue

        # Load package onto truck
        truck.load_package(package)
        truck.delivered += 1

        #print(f"""Loading truck {truck.truck_id}. Current packages: {truck.get_num_packages()}. 
              #Most recent package ID: {package.package_id}""")

    # Reinsert deferred packages 
    """O(log N)"""
    for package_p, id, package in deferred_packages:
        heapq.heappush(the_queue, (package_p, id, package))

        #print(f"""Loading truck {truck.truck_id} with deferred packages. Current packages: {truck.get_num_packages()}. 
              #Most recent package ID: {package.package_id}""")
    
def select_next_package(truck, dist_table):
    """O(N) complexity"""
    current_location = truck.get_location()
    nearest_package = None
    min_distance = float('inf')
    highest_priority = float('inf')

    for package in truck.packages:
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

def deliver_package(truck, package, dist_table):
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

    truck.drop_off_package(package, truck.current_time)
    truck.set_location(package.address)

    print(f"""Truck {truck.truck_id} delivered package {package.package_id} to {package.address} at {truck.current_time.time()}.""")

def greedy_delivery_algorithm(package_queue, distance_table):
    """Process consist of:
        O(N) for first loop
        O(N^2) for second loop
        O(N) for the third loop
        O(N) for the 4th and 5th while loop
        Making this function O(N^2) time complexity"""
    # Create trucks
    trucks = [Truck(1, datetime.strptime("8:00 AM", "%I:%M %p")),
              Truck(2, datetime.strptime("8:00 AM", "%I:%M %p"))]

    # Load packages onto trucks
    for truck in trucks:
        load_packages(truck, package_queue, truck.current_time)

    # Deliver packages using a greedy approach
    for truck in trucks:
        while truck.packages and truck.traveled < 140:
            # Greedy selection logic based on distance

            # If it is past 9:05 AM and packages 6 and 25 are at the HUB, return to the hub
            if truck.current_time >= datetime.strptime("9:05 AM", "%I:%M %p") and (find_package(package_queue, 6) or find_package(package_queue, 25)):
                if truck.truck_id == 2:
                    truck.return_to_hub(truck.current_location, distance_table)
                    load_packages(truck, package_queue, truck.current_time)
            # If it is past 10:20 AM and package 9 is at the hub, return to HUB
            if truck.current_time >= datetime.strptime("10:20 AM", "%I:%M %p") and find_package(package_queue, 9):
                if truck.truck_id == 2:
                    truck.return_to_hub(truck.current_location, distance_table)
                    load_packages(truck, package_queue, truck.current_time)
            next_package = select_next_package(truck, distance_table)
            deliver_package(truck, next_package, distance_table)

        # Return to hub if no packages on the truck
        truck.return_to_hub(truck.current_location, distance_table)

    # Get most recent truck that returned
    truck_time = datetime.strptime("5:00 PM", "%I:%M %p")
    for i in trucks:
        if i.current_time < truck_time:
            truck_time = i.current_time

    # Set truck 3's depart time to most recent truck's arrival
    truck_3_depart_time = datetime.combine(datetime.today(), truck_time.time())
    truck_3 = Truck(3, truck_3_depart_time)

    # Begin loading truck 3
    while package_queue:
        load_packages(truck_3, package_queue, truck_3.current_time)

    while truck_3.packages:
        next_package = select_next_package(truck_3, distance_table)
        deliver_package(truck_3, next_package, distance_table)

    truck_3.return_to_hub(truck_3.current_location, distance_table)

    print("Remaining packages:", len(package_queue))
    print("Final truck stats:")

    # Print final truck stats
    for a_truck in [trucks[0], trucks[1], truck_3]:
        print(a_truck)

