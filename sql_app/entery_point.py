import os
import random

from tree_sort import tree_sort

unsortedList = []
sorted_list = []
1
while True:
    print("1. Add a numbers")
    print("2. Generate a random array")
    print("3. Sort the numbers")
    print("4. Save numbers to a file")
    print("5. Load numbers from a file")
    print("0. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_choice = input("Add numbers to: \n1. New array\n2. Existing array\nEnter your choice: ")

        if add_choice == "1":
            unsortedList = []
        elif add_choice == "2":
            if not sorted_list:
                print("No existing array found. Starting with a new array.")
                sorted_list = []
            else:
                print("Adding numbers to the existing array.")
        else:
            print("Invalid choice! Please enter a valid option.")

        while True:
            num = input("Enter a number (or 'q' to exit): ")
            if num.lower() == 'q':
                break
            try:
                num = float(num)
                unsortedList.append(num)
            except ValueError:
                print("Invalid input! Please enter a valid number.")

    elif choice == "2":
        while True:
            try:
                length = int(input("Enter the length of the array: "))
                if length <= 0:
                    raise ValueError
                break
            except ValueError:
                print("Invalid length! Please enter a positive integer.")

        minimum = float(input("Enter the minimum value: "))
        maximum = float(input("Enter the maximum value: "))

        unsortedList.extend(round(random.uniform(minimum, maximum), 1) for _ in range(length))
        print("Random array generated: ", unsortedList)

        add_choice = input("Do you want to add this randomly generated array to the existing array? (y/n): ")
        if add_choice.lower() == 'y':
            if not sorted_list:
                sorted_list.append(unsortedList)
                print("Adding the randomly generated array to the existing array.")
        elif add_choice.lower() == 'n':
            unsortedList.clear()
            print("Okay, the randomly generated array will not be added.")
        else:
            print("Invalid choice. Please enter 'y' or 'n'.")

    elif choice == "3":
        sorted_list = tree_sort(unsortedList)
        print("Sorted numbers:", sorted_list)

    elif choice == "4":
        file_name = input("Enter the file name to save (in .txt format): ")
        if not file_name.endswith(".txt"):
            file_name += ".txt"
        while os.path.exists(file_name):
            print("File already exists:", file_name)
            overwrite_choice = input("Do you want to overwrite it? (y/n): ")
            if overwrite_choice.lower() == "y":
                break
            else:
                file_name = input("Enter a new file name (in .txt format): ")
                if not file_name.endswith(".txt"):
                    file_name += ".txt"
        try:
            if not sorted_list:
                print("Please sort numbers before saving.")
            else:
                with open(file_name, "w") as file:
                    for number in sorted_list:
                        file.write(str(number) + "\n")
                print(f"The sorted numbers have been saved to '{file_name}'.")
        except IOError:
            print("Error saving the file!")

    elif choice == "5":
        file_name = input("Enter the file name to load (in .txt format): ")
        if not file_name.endswith(".txt"):
            file_name += ".txt"
        if not os.path.exists(file_name):
            print("File does not exist:", file_name)
        else:
            try:
                with open(file_name, 'r') as file:
                    unsortedList = [float(line.strip()) for line in file]
                print("Numbers loaded from", file_name)
            except IOError:
                print("Error loading the file!")
    elif choice == "0":
        break
    else:
        print("Invalid choice! Please enter a valid option.")