if __name__ == "__main__":

    convert = input("Please enter an input: ")
    conv_list = convert.split()
    #print(conv_list)

    num = float(conv_list[0])
    unit = conv_list[1]

    if unit == 'in':
        final = num * 2.54
        print(f"{convert} = {final:.2f} cm.")

    elif unit == 'cm':
        final = num * 0.3937
        print(f"{convert} = {final:.2f} in.")

    elif unit == 'yd':
        final = num * 0.9144
        print(f"{convert} = {final:.2f} m.")

    elif unit == 'm':
        final = num * 1.09361
        print(f"{convert} = {final:.2f} yd.")

    elif unit == 'oz':
        final = num * 28.349523125
        print(f"{convert} = {final:.2f} g.")

    elif unit == 'g':
        final = num * 0.035274
        print(f"{convert} = {final:.2f} oz.")

    elif unit == 'lb':
        final = num * 0.45359237
        print(f"{convert} = {final:.2f} kg.")

    elif unit == 'kg':
        final = num * 2.20462
        print(f"{convert} = {final:.2f} lbs.")