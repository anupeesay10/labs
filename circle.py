import math


if __name__ == "__main__":
    radius = input("Please enter the radius of the circle: ")
    radius  = float(radius)

    area = math.pi * radius ** 2
    perimeter = 2 * math.pi * radius

    print(f"The circle with radius {radius:.2f} has an area of {area:.2f} and a perimeter of {perimeter:.2f}.")
