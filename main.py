from classes import Package, Truck
from datetime import datetime
import csv
from helpers import calculate_priority, get_note, greedy_delivery_algorithm, insert_package, user_interface

"""
Name: Zerryn Hogan
Student ID: 012207809
"""
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

dist_dict = read_distance()

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

# Call function for user to view package status or truck mileage
user_interface(read_packages(), read_distance(), trucks)

