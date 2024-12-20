from datetime import datetime, timedelta
import heapq

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
        self.status = "At hub"
        self.pickup_time = None
        self.truck_id = "No truck assigned"

    def set_pickup_status(self, pickup_status):
        self.picked_up = pickup_status

    def set_dropoff_time(self, time):
        self.drop_off_time = time
        self.delivered = True
        self.status = "Delivered"

    def set_status(self, status):
        self.status = status

    def check_status(self):
        return self.status
    
    def get_pickup_status(self):
        return self.picked_up
    
    def delivered_at(self):
        if self.delivered == True:
            return self.drop_off_time.time()
        else:
            return "Not yet delivered"
            
    def __repr__(self):
        return f"""
                    ID: {self.package_id} 
                    Address: {self.address}, {self.city}, {self.state}, {self.zip_code}
                    Delivery deadline: {self.deadline} 
                    Weight: {self.weight}
                    Note: {self.note}
                    Status: {self.check_status()}
                    Loaded at: {self.pickup_time.time() if self.pickup_time else 'Not yet loaded'}
                    Delivered at: {self.delivered_at()}
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
            package.set_pickup_status(True)
            package.set_status("En route")
            heapq.heappush(self.packages, (package.priority, package.package_id, package))
        else:
            print(f"Truck {self.truck_id} is at full capacity. Cannot load more packages.")

    def drop_off_package(self, package, drop_off_time: datetime):
        temp_heap = []
            
        while self.packages:
            priority, package_id, pkg = heapq.heappop(self.packages)
            if pkg == package:
                pkg.set_dropoff_time(drop_off_time)
                pkg.set_status("Delivered")
            else:
                heapq.heappush(temp_heap, (priority, package_id, pkg))

        self.packages = temp_heap

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

        #if self.delivered > 0:
            #print(f"Truck {self.truck_id} returned to the HUB at {self.current_time.time()}")
        #else:
            #print(f"Truck {self.truck_id} remains at the HUB.")

    def __repr__(self):
        return f"""
                    ID: {self.truck_id} 
                    Current location: {self.current_location}
                    Miles traveled: {round(self.traveled, 2)}
                    Packages delivered: {self.delivered}
                    Remaining packages: {self.get_num_packages()}
                """
