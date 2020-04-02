class User:
    
    def __init__(self, dni, name, last_name, email, age, tlf):
        self.dni = dni
        self.name = name
        self.last_name = last_name
        self.email = email
        self.age = age
        self.tlf = tlf
        self.requests = []

    def as_json(self):
        return {
            "dni": self.dni,
            "age": self.age,
            "email": self.email,
            "last_name": self.last_name,
            "name": self.name,
            "tlf": self.tlf,
            "requests": self.requests
        }


def gen_rand_user(user_id):
    from numpy import random
    dni = f"{user_id:08d}{'TRWAGMYFPDXBNJZSQVHLCKE'[user_id%23]}"
    name = "sim_user_"+str(user_id)
    last_name = "Smith_"+str(user_id)
    email = "smith_"+str(user_id)+"@ubre.com"
    age = random.randint(16,100)
    def n(): return random.randint(0,9)
    tlf = f"6{n()}{n()}{n()}{n()}{n()}{n()}{n()}{n()}"
    return User(dni, name, last_name, email, age, tlf)


def add_user_db(user):
    import requests as req
    url = "http://127.0.0.1:8000/movility/users/"
    data = user.as_json()
    response = req.post(url, data=data)
    if response.status_code == 201:
        return True
    else:
        return False
