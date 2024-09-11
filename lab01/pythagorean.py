import math
if __name__ == "__main__":
    side1 = input("Please enter the length of side one: ")
    side2 = input("Please enter the length of side two: ")

    side1 = float(side1)
    side2 = float(side2)

    path = math.sqrt((side1 ** 2) + (side2 ** 2))
    print(f"The hypotenuse is: {path:.2}.")