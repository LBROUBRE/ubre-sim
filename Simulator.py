import Users
import Requests

from numpy import random

import matplotlib.pyplot as plt
import mplleaflet as mplleaflet
import matplotlib.lines as mlines

NUMBER_OF_GENERATIONS = 50

"""zones for random request making"""
zones = {
    "Redondela": {
        "size": 0,
        "relation": 345979
    },
    "Soutomaior": {
        "size": 0,
        "relation": 341377
    },
    "Pazos de Borbén": {
        "size": 0,
        "relation": 343651
    },
    "Fornelos de Montes": {
        "size": 0,
        "relation": 342037
    }
}


class Simulator:

    def __init__(self):
        self.users = []
        self.requests = []
        # We should clean the DB to avoid collisions

    def create_users(self, quantity):
        for i in range(quantity):
            new_user = Users.gen_rand_user(i)
            Users.add_user_db(new_user)
            self.users.append(new_user)
        print("Added %d users" % quantity)

    def create_request_per_user(self):
        for user in self.users:
            zone1 = random.choice(list(zones))
            poly1 = zones[zone1]["poly"]
            zone2 = random.choice(list(zones))
            poly2 = zones[zone2]["poly"]
            new_request = Requests.gen_rand_request(user, poly1, poly2)
            Requests.add_request_db(new_request)
            self.requests.append(new_request)
        print("Added %d requests" % len(self.users))

    def print_requests(self):
        plt.figure(figsize=(8, 6))
        fig = plt.figure()
        for request in self.requests:
            lat_origin = request.origin.x
            lon_origin = request.origin.y
            lat_destination = request.destination.x
            lon_destination = request.destination.y
            plt.plot(lon_origin, lat_origin, 'ro')
            plt.plot(lon_destination, lat_destination, 'bo')
            trajectory = mlines.Line2D([lon_destination, lon_origin], [lat_destination, lat_origin])
            plt.gca().add_line(trajectory)
        mplleaflet.show(fig=fig)


def get_relation_polygon(relation_id):
    from shapely.geometry import Point, Polygon
    import overpy
    api = overpy.Overpass()
    ret = api.query('[out:json];relation(%d);(._;>;);out body;' % relation_id)
    nodes = []
    for node in ret.nodes:
        coordinates = Point(node.lat, node.lon)
        nodes.append(coordinates)

    poly = Polygon(nodes)
    return poly


"""MAIN"""
zone = {}
for zone in zones:
    zones[zone]["poly"] = get_relation_polygon(zones[zone]["relation"])
simulator = Simulator()
simulator.create_users(NUMBER_OF_GENERATIONS)
simulator.create_request_per_user()
simulator.print_requests()
