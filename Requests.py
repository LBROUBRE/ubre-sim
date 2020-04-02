class Request:

    def __init__(self, origin, destination, requested_departure_data, requested_arrival_data):
        self.origin = origin
        self.destination = destination
        self.requestedDepartureData = requested_departure_data
        self.requestedArrivalData = requested_arrival_data

    def as_json(self):
        return {
            "origin": self.origin,
            "destination": self.destination,
            "departure-data": self.requestedDepartureData,
            "arrival-data": self.requestedArrivalData
        }


def gen_rand_request(user, poly1, poly2):
    origin = gen_new_location(poly1)
    destination = gen_new_location(poly2)

    request_departure_data, request_arrival_data = gen_new_request_data()
    request = Request(origin, destination, request_departure_data, request_arrival_data)
    # user.add_request(request) TODO: users and request must be victualed somehow
    return request


def gen_new_location(poly):
    from shapely.geometry import Point
    from numpy import random
    min_x, min_y, max_x, max_y = poly.bounds

    point = None
    while point is None:
        random_point = Point([random.uniform(min_x, max_x), random.uniform(min_y, max_y)])
        if random_point.within(poly):
            point = random_point

    return point


def gen_new_request_data():
    return 0, 0


def add_request_db(request):
    import requests as req
    url = "http://127.0.0.1:8000/movility/requests/"
    data = request.as_json()
    response = req.post(url, data=data)
    if response.status_code == 201:
        return True
    else:
        return False


"""
plt.figure(figsize=(8, 6))
fig = plt.figure()
set_new_relation(341377, 1)
for x in range(20):
    new_point = gen_new_location(relations[341377]["poly"])
    plt.plot(new_point.y, new_point.x, 'ro')

mplleaflet.show(fig=fig)
"""
