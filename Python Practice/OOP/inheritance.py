class Animal:
    alive = True

    def eat(self):
        print("This animal is eating")

    def sleep(self):
        print("This animal is sleeping")

#Child class Rabbit will inheir attributes and methods of parent class Animal
class Rabbit(Animal):
    def jump(self):
        print("This rabbit can jump")
class Fish(Animal):
    def swim(self):
        print("This Fish can swim")
class Hawk(Animal):
    def fly(self):
        print("This hawk can fly")

rabbit = Rabbit()
fish = Fish()
hawk = Hawk()

print(rabbit.alive)
rabbit.eat()
fish.sleep()
rabbit.jump()
fish.swim()
hawk.fly()
