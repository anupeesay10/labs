class Caesar:

    def __init__(self):
        self.key = 0

    def set_key(self, num):
        self.key = num % 26

    def get_key(self):
        return self.key

    def encrypt(self, plaintext):
        plaintext = plaintext.lower()
        first_list = []
        second_list = []
        final = ""
        for i in plaintext:
            if i == " ":
                first_list.append(32)

            elif ord(i) in range(97, 123):
                j = ord(i) + self.key
                if j > 122:
                    j = 97 + (j - 123)
                first_list.append(j)

            else:
                j = ord(i) + self.key
                first_list.append(j)

        #return first_list

        for k in first_list:
            l = chr(k)
            second_list.append(l)
        #return second_list

        for m in second_list:
            final += m

        return final


    def decrypt(self, ciphertext):
        third_list = []
        fourth_list = []
        final2 = ""

        for i in ciphertext:
            if i == " ":
                third_list.append(32)

            elif ord(i) in range(97, 123):
                j = ord(i) - self.key
                if j < 97:
                    j = 122 - (96 - j)
                third_list.append(j)

            else:
                j = ord(i) - self.key
                third_list.append(j)


        for k in third_list:
            l = chr(k)
            fourth_list.append(l)
        #return second_list

        for m in fourth_list:
            final2 += m

        return final2


if __name__ == "__main__":
    cipher = Caesar()
    key = int(input("Please enter the key: "))
    cipher.set_key(key)
    #print(cipher.get_key())

    string = input("Please enter the string that you would like to encrypt: ")
    encrypted = cipher.encrypt(string)
    print(encrypted)

    dec = int(input("Would you like to decrypt (Enter 1 for yes or 2 for no)?: "))
    if dec == 1:
        print(cipher.decrypt(encrypted))
    else:
        print("Have a nice day.")

    #print(cipher.decrypt())