#OOP practicing with Bro code

from car import Car

car_1 = Car("Tesla","Model 3", "2023", "Red")
car_2 = Car("Chevrolet", "Camaro", "2024", "Red")

print(car_1.make)
print(car_1.model)
print(car_1.year)
print(car_1.color)

print(car_2.model,car_2.make,car_2.year,car_2.color)

car_1.drive()
car_1.stop()
car_2.drive()
car_2.stop()