from datetime import datetime, timedelta

class Package:
    """
    Class for a package
    'Deadline' attribute is the time package should be dropped off.
    'Drop_off_time' attribute is the time the package is actually dropped off.
    'Picked_up' attribute is the status for if a package is en route. False means package is still at the hub.
    """
    def __init__(self, package_id, address, city, state, zip_code, deadline, weight, priority, note=None):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.priority = priority
        self.note = note
        self.picked_up = False
        self.drop_off_time = None
        self.delivered = False

    def set_pickup_status(self, pickup_status):
        self.picked_up = pickup_status

    def set_dropoff_time(self, time):
        self.drop_off_time = time
        self.delivered = True

    def __repr__(self):
        return f"""
                    ID: {self.package_id} 
                    Address: {self.address}, {self.city}, {self.state}, {self.zip_code}
                    Deadline: {self.deadline} 
                    Weight: {self.weight}
                    Note: {self.note}
                """
    
    # Used to compare packages with the same priority rating
    def __lt__(self, other):
        return self.priority < other.priority

class Truck:
    """
    Class for delivery truck
    """
    def __init__(self, truck_id, depart_time: datetime = None):
        self.truck_id = truck_id
        self.current_time = depart_time
        self.speed = 18
        self.traveled = 0
        self.packages = []
        self.current_location = '4001 South 700 East'
        self.delivered = 0
    
    def get_num_packages(self):
        return len(self.packages)
    
    def load_package(self, package):
        if self.get_num_packages() < 16:
            self.packages.append(package)
            package.set_pickup_status(True)
        else:
            print(f"Truck {self.truck_id} is at full capacity. Cannot load more packages.")

    def drop_off_package(self, package, drop_off_time: datetime):
        if package in self.packages:
            package.set_dropoff_time(drop_off_time)
            self.packages.remove(package)
        else:
            print(f"Package {package.package_id} is not on Truck {self.truck_id}.")

    def set_location(self, loc):
        self.current_location = loc

    def set_time(self, time):
        self.current_time += time

    def get_location(self):
        return self.current_location
    
    def return_to_hub(self, cur_loc, dist_table):
        cur_loc = self.get_location()

        # Get distance from current location to HUB
        distance = float(dist_table[cur_loc]['4001 South 700 East'])

        # Simulate drive time back to hub
        travel_time = round(distance / self.speed, 2)
        self.set_time(timedelta(hours=travel_time))
        self.traveled += distance
        self.set_location('4001 South 700 East')

        print(f"Truck {self.truck_id} returned to the HUB at {self.current_time.time()}")

    def __repr__(self):
        return f"""
                    ID: {self.truck_id} 
                    Current location: {self.current_location}
                    Miles traveled: {round(self.traveled, 2)}
                    Packages delivered: {self.delivered}
                    Remaining packages: {self.get_num_packages()}
                """
