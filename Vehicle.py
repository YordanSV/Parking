

class Vehicle:
    def __init__(self, plate, vehicleType, make, model, color):
        self.plate = plate
        self.vehicleType = vehicleType
        self.make = make
        self.model = model
        self.color = color


# Herencia 

class Motorcycle(Vehicle):

    def __init__(self, plate, vehicleType, make, model, color):
        super().__init__(plate, vehicleType, make, model, color)
        self.hourlyRate = 5 #Precio por hora


class Car(Vehicle):
    def __init__(self, plate, vehicleType, make, model, color):
        super().__init__(plate, vehicleType, make, model, color)
        self.hourlyRate = 10 #Precio por hora

class Truck(Vehicle): #Clase camion

    def __init__(self, plate, vehicleType, make, model, color):
        super().__init__(plate, vehicleType, make, model, color)
        self.hourlyRate = 15 #Precio por hora
