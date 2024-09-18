def make_set(data):
    data.sort()
    #print(data)
    result = []
    for item in data:
        if item not in result:
            result.append(item)
    print(result)

def is_set(data):
    data.sort()
    if not data:
        print("True")
    else:
        cur_val = data[0]
        for i in range(1, len(data)):
            if data[i] == cur_val:
                print("False")
                break
            else:
                cur_val = data[i]
        else:
            print("True")


def union(setA, setB):

    def is_set(data):
        data.sort()
        if not data:
            return ("Zero")
        else:
            cur_val = data[0]
            for i in range(1, len(data)):
                if data[i] == cur_val:
                    return ("False")
                else:
                    cur_val = data[i]
            else:
                return ("True")

    first = is_set(setA)
    second = is_set(setB)
    if first == "False" or second == "False":
        empty = []
        print(empty)
    elif first == "True" and second == "True":
        result = []
        result += setA
        for item in setB:
            if item not in result:
                result.append(item)
        print(result)
    elif first == "Zero" and second == "True":
        print(setB)
    elif first == "True" and second == "Zero":
        print(setA)

def intersection(setA, setB):
    if not setA or not setB:
        empty = []
        print(empty)
    else:
        def is_set(data):
            data.sort()
            if not data:
                return ("True")
            else:
                cur_val = data[0]
                for i in range(1, len(data)):
                    if data[i] == cur_val:
                        return ("False")
                    else:
                        cur_val = data[i]
                else:
                    return ("True")

        first = is_set(setA)
        second = is_set(setB)
        if first == "False" or second == "False":
            empty = []
            print(empty)
        elif first == "True" and second == "True":
            result = []
            for item in setA:
                if item in setB:
                    result.append(item)
            print(result)

if __name__ == "__main__":
    print("Select your option: ")
    prompt = """ 
    1. make_set(data)
    2. is_set(data)
    3. union(setA, setB)
    4. intersection(setA, setB) """

    option = input(prompt)
    print()

    if option in ('1', '2'):

        nums = input("Please enter a list of numbers separated by commas: ")

        """Get the list of numbers, and remove any trailing whitespaces: """
        num_list = []
        final_list = []
        for i in nums.split(','):
            i = i.strip()
            num_list.append(i)
        # print(num_list)

        """Remove any null characters: """
        for j in num_list[:]:
            if j == '':
                num_list.remove(j)
        # print(num_list)

        """Convert each character into an integer: """
        for k in num_list:
            k = int(k)
            final_list.append(k)
        print(f"Your list is: {final_list}")

        if option == '1':
            make_set(final_list)

        elif option == '2':
            is_set(final_list)

    elif option in ('3', '4'):
        nums1 = input("Enter your first list separated by commas: ")
        num_list1 = []
        final_list1 = []
        for i in nums1.split(','):
            i = i.strip()
            num_list1.append(i)
        # print(num_list)

        for j in range(len(num_list1)):
            if not num_list1[j]:
                del num_list1[j]

        # print(num_list)
        for k in num_list1:
            k = int(k)
            final_list1.append(k)
        print(f"Your first list is: {final_list1}")

        nums2 = input("Enter your second list separated by commas: ")
        num_list2 = []
        final_list2 = []
        for i in nums2.split(','):
            i = i.strip()
            num_list2.append(i)
        # print(num_list)

        for j in num_list2[:]:
            if not j:
                num_list2.remove(j)

        # print(num_list)
        for k in num_list2:
            k = int(k)
            final_list2.append(k)
        print(f"Your second list is: {final_list2}")

        if option == '3':
            union(final_list1, final_list2)

        elif option == '4':
            intersection(final_list1, final_list2)

    else:
        print("Invalid option. Please try again.")