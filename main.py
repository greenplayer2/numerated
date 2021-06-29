import requests
from pytz import timezone
import datetime

def get_int(input):
    try:
        return int(input)
    except ValueError:
        return False

class MBTAScheduler():
    def __init__(self):
        self.current_step = 0 # mark which step of the process we're on
        print("Pulling data from MBTA...\n")
        routes_request = requests.get("https://api-v3.mbta.com/routes?filter[type]=0,1") # pull only Light and Heavy rail lines
        if routes_request.status_code != 200:
            raise Exception("Web service call to retrieve routes failed with a {} error code.".format(routes_request.status_code))
        try:
            route_json = routes_request.json()
        except Exception as e:
            "Route data could not be converted to JSON."
        self.routes = {}
        if len(route_json["data"]) == 0:
            raise Exception("No routes were returned from the web service!")
        for route in route_json["data"]:
            route_id = route["id"]
            route_name = route["attributes"]["long_name"]
            self.routes[route_id] = { # create a data structure that will contain all routes with their directions and stops
                "name": route_name,
                "directions": [],
                "stops": []
            }
            num_directions = len(route["attributes"]["direction_destinations"])
            assert num_directions == len(route["attributes"]["direction_names"]), "Mismatch between direction_destinations and direction_names for {} route!".format(route["long_name"])
            index = 0
            while index < num_directions:
                direction_name = route["attributes"]["direction_names"][index]
                direction_destination = route["attributes"]["direction_destinations"][index]
                self.routes[route_id]["directions"].append({
                    "name": direction_name,
                    "destination": direction_destination
                })
                index += 1

    def get_routes(self):
        return_text = "Please select a route:\n"
        index = 1
        self.route_array = []
        for route in self.routes:
            self.route_array.append(route)
            return_text += "\n" + (str(index) + ": " + route)
            index += 1
        return return_text

    def select_route(self):
        route_index = get_int(input("> "))
        num_routes = len(self.routes.keys())
        while route_index == False or route_index > num_routes or route_index < 1:
            print("Invalid selection.  Please try again.\n")
            route_index = get_int(input("> "))
        # subtract 1 from what they selected because Python uses a 0 based index
        self.route_selection = self.route_array[route_index - 1]
        # get stops for this route if we don't have them already
        if len(self.routes[self.route_selection]["stops"]) == 0:
            stops = requests.get("https://api-v3.mbta.com/stops?filter[route]={}&filter[direction_id]=0".format(self.route_selection))
            if stops.status_code != 200:
                raise Exception("Web service call to retrieve stops failed with a {} error code.".format(stops.status_code))
            try:
                stop_json = stops.json()
            except Exception as e:
                "Stop data could not be converted to JSON."
            if len(stop_json["data"]) == 0:
                raise Exception("No stops could be found for this route!")
            for stop in stop_json["data"]:
                stop_id = stop["id"]
                self.routes[self.route_selection]["stops"].append({
                    "name": stop["attributes"]["name"],
                    "id": stop_id
                })

        return_text = "\n\nPlease select your stop on the " + self.route_selection + " line:"
        index = 1
        for stop in self.routes[self.route_selection]["stops"]:
            return_text += "\n" + (str(index) + ": " + stop["name"])
            index += 1
        self.current_step = 1
        return return_text

    def select_stop(self):
        if self.current_step != 1:
            raise Exception("You must select a route before you can select a stop.")
        stop_index = get_int(input("> "))
        num_stops = len(self.routes[self.route_selection]["stops"])
        while stop_index == False or stop_index > num_stops or stop_index < 1:
            print("Invalid selection.  Please try again.\n")
            stop_index = get_int(input("> "))
        stop_index -= 1
        self.stop_selection_id = self.routes[self.route_selection]["stops"][stop_index]["id"]
        self.stop_selection_name = self.routes[self.route_selection]["stops"][stop_index]["name"]
        return_text = "\n\nPlease select a direction for the " + self.route_selection + " route starting from {} stop:".format(self.stop_selection_name)
        index = 1
        for direction in self.routes[self.route_selection]["directions"]: # print the menu for the stops
            return_text += "\n" + (str(index) + ": " + direction["name"] + " toward " + direction["destination"])
            index += 1
        self.current_step = 2
        return return_text

    def select_direction(self):
        if self.current_step != 2:
            raise Exception("You must select a stop before you can select a direction.")
        self.direction_index = get_int(input("> "))
        num_directions = len(self.routes[self.route_selection]["directions"])
        while self.direction_index == False or self.direction_index > num_directions or self.direction_index < 1:
            print("Invalid selection.  Please try again.\n")
            self.direction_index = get_int(input("> "))
        self.direction_index -= 1 # converting to 0 based index for Python
        self.direction_selection = self.routes[self.route_selection]["directions"][self.direction_index]["name"]
        direction_destination = self.routes[self.route_selection]["directions"][self.direction_index]["destination"]
        self.current_step = 3
        return "\n\nYou are taking the {} line {} toward {} from {}.".format(self.route_selection, self.direction_selection, direction_destination, self.stop_selection_name)

    def get_answer(self):
        if self.current_step != 3:
            raise Exception("You must select a destination before you can get the departure time.")
        tz = timezone('US/Eastern')
        now = datetime.datetime.now(tz)
        now_time = str(now.time())[0:5]
        # grab the schedule for this line
        schedule_url = "https://api-v3.mbta.com/schedules?filter[direction_id]={}&filter[route]={}&filter[stop]={}&filter[min_time]={}&sort=departure_time".format(self.direction_index, self.route_selection, self.stop_selection_id, now_time)
        schedules = requests.get(schedule_url)
        if schedules.status_code != 200:
            raise Exception("Web service call to retrieve stops failed with a {} error code.".format(schedules.status_code))
        try:
            schedule_json = schedules.json()
        except Exception as e:
            "Schedule data could not be converted to JSON."
        self.current_step = 0
        if len(schedule_json["data"]) == 0 or schedule_json["data"][0]["attributes"]["departure_time"] == None:
            return "No schedule data could be determined for this route!"
        # grab the first item in the returned schedule, since it is sorted by departure time ascending
        return "You need to be at {} stop at {}.".format(self.stop_selection_name, schedule_json["data"][0]["attributes"]["departure_time"][11:16])

    def print_route(self):
        print(self.select_route())

    def print_stop(self):
        print(self.select_stop())

    def print_direction(self):
        print(self.select_direction())

    def print_routes(self):
        print(self.get_routes())

    def print_answer(self):
        print(self.get_answer())

if __name__ == '__main__':
    try:
        MBTA = MBTAScheduler()
        MBTA.print_routes()
        MBTA.print_route()
        MBTA.print_stop()
        MBTA.print_direction()
        MBTA.print_answer()
    except Exception as e:
        print(str(e))