class Transport:
    def __init__(self, brand, speed):
        self.brand = brand
        self.speed = speed

    def move(self):
        print(f"Transport is moving at {self.speed} km/h")

    def __str__(self):
        return f"Transport: {self.brand}, Speed: {self.speed}"


class Car(Transport):
    def __init__(self, brand, speed, seats):
        super().__init__(brand, speed)
        self.seats = seats

    def honk(self):
        print("Beep beep!")

    def move(self):
        print(f"Car {self.brand} is driving at {self.speed} km/h")

    def __str__(self):
        return f"Transport: {self.brand}, Speed: {self.speed}, Seats: {self.seats}"

    def __len__(self):
        return self.seats

    def __eq__(self, other):
        return self.speed == other.speed

    def __add__(self, other):
        return self.speed + other.speed


class Bike(Transport):
    def __init__(self, brand, speed, type):
        super().__init__(brand, speed)
        self.type = type

    def move(self):
        print(f"Bike {self.brand} is cycling at {self.speed} km/h")

    def __str__(self):
        return f"Transport: {self.brand}, Speed: {self.speed}, Type: {self.type}"


tr_1 = Transport("toyota", 90)
tr_2 = Transport('merc', 120)
car_1 = Car("hermit", 80, 5)
car_2 = Car('sss+', 80, 4)
bike_1 = Bike("AAA", 100, 'sport')
bike_2 = Bike('ninja', 130, 'road')

print(tr_1)
print(car_1)
print(bike_1)

car_1.move()
bike_1.move()
car_2.honk()

print(len(car_1))
print(car_1 == car_2)
print(car_1 + car_2)
print(bike_1 + car_1)

sp = [car_1, bike_1, tr_1]
for i in sp:
    i.move()
