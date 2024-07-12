class Student:                          #definition of a new data type
    ...

def main():
    student = get_student()
    print(f"{student.name} from {student.house}")

def get_student():
    student = Student()                     #object or instance, a variable created from a class
    student.name = input("Name: ")         #attributes, property that allows you to sepcify values inside
    student.house = input("House: ")
    return student

if __name__ == "__main__":
    main()