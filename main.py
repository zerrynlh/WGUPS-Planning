from classes import Package
import heapq
import csv
from helpers import calculate_priority, get_note, greedy_delivery_algorithm

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

# Correct address
dist_dict['5383 South 900 East #104'] = dist_dict.pop('5383 S 900 East #104')

# Initialize min-heap for packages
package_queue = []

with open('package_file.csv') as package_file:
    """O(N) complexity"""
    csv_reader = csv.reader(package_file)
    next(csv_reader, None)
    for row in csv_reader:
        new_package = Package(int(row[0]), row[1], row[2], row[3], int(row[4]), 
                              row[5], float(row[6]), calculate_priority(row[5]), get_note(row[7]))
        
        # Tuple uses package ID to compare packages with same priority
        """O(log N)"""
        heapq.heappush(package_queue, (new_package.priority, new_package.package_id, new_package))

print(f"{len(package_queue)} packages read.")

# Load trucks and deliver packages
greedy_delivery_algorithm(package_queue, dist_dict)
