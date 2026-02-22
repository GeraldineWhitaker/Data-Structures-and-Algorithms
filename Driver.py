# Geraldine Whitaker
# This file is the main controller of the Grazioso Rescue Animal System. It manages user authentication,
# displays role-based menus, processes user input, and allows user to intake or reserve animals.

from typing import List
from Dog import Dog
from Monkey import Monkey
from Security import AuthSystem
from Algorithms import Algorithms

ALLOWED_SPECIES = Monkey.ALLOWED_SPECIES

# Current list of dogs
dog_list = [
    Dog("Spot", "German Shepherd", "male", 1, 25.6, "05-12-2019", "United States", "intake", False, "United States"),
    Dog("Rex", "Great Dane", "male", 3, 35.2, "02-03-2020", "United States", "Phase I", False, "United States"),
    Dog("Bella", "Chihuahua", "female", 4, 25.6, "12-12-2019", "Canada", "in service", True, "Canada")
]

# Current list of monkeys
monkey_list = [
    Monkey("George", "Macaque", "male", 1, 25.6, "05-12-2022", "United States", "intake", False, "United States", 12.5, 20.4, 27.6),
    Monkey("Lola", "Tamarin", "female", 3, 25.6, "08-15-2020", "United States", "in service", False, "United States", 12.5, 20.4, 27.6),
    Monkey("Yoda", "Squirrel Monkey", "male", 4, 25.6, "02-06-2019", "Canada", "intake", False, "Canada", 12.5, 20.4, 27.6)
]

# Implements multi criteria search and reservation and training status updates
alg = Algorithms(dog_list, monkey_list)


# Check that animal name is in either list
def animal_exists(name: str):
    return any(d.name.lower() == name.lower() for d in dog_list) or any(m.name.lower() == name.lower() for m in monkey_list)


# Check for valid input
def prompt_text(message: str):
    while True:
        value = input(message).strip()
        if value:
            return value
        print("Input cannot be empty. Try again.\n")


# Check that entered gender is either male or female
def prompt_gender():
    while True:
        gender = input("What is this animal's gender? (male/female): ").strip().lower()
        if gender in ("male", "female"):
            return gender
        print("Invalid gender. Enter 'male' or 'female'.\n")


# Check that entered value is an integer larger than 0
def prompt_int(message: str):
    while True:
        raw = input(message).strip()
        try:
            value = int(raw)
            if value < 0:
                print("Value cannot be negative.\n")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a whole number.\n")


# Check that entered value is a number larger than 0
def prompt_float(message: str):
    while True:
        raw = input(message).strip().replace(",", ".")
        try:
            value = float(raw)
            if value <= 0:
                print("Value must be greater than zero.\n")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a numeric value.\n")


# Check for valid date and format
def prompt_date(message: str):
    while True:
        value = input(message).strip()
        parts = value.split("-")

        # Check for MM-DD-YYYY structure
        if len(parts) != 3:
            print("Invalid date format. Use MM-DD-YYYY.\n")
            continue

        mm, dd, yyyy = parts

        # Check for digits
        if not (mm.isdigit() and dd.isdigit() and yyyy.isdigit()):
            print("Invalid date format. Use numbers like 05-12-2019.\n")
            continue

        # Check year length
        if len(yyyy) != 4:
            print("Invalid year. Use 4 digits (YYYY).\n")
            continue

        # Validate date
        m = int(mm)
        d = int(dd)
        if not (1 <= m <= 12 and 1 <= d <= 31):
            print("Invalid month/day. Use a real date like 02-03-2020.\n")
            continue

        y = int(yyyy)
        if y < 1970:
            print("Year must be 1971 or later.\n")
            continue

        return value


# Check that user entered y or n 
def prompt_yes_no(label: str):
    while True:
        raw = input(f"{label} (y/n): ").strip().lower()
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        print("Error: Please enter 'y' or 'n'.\n")


# Format and print table or display no animals found if search returns no matching animal 
def print_table(animals):
    if not animals:
        print("\nNo animals to display.\n")
        return

    print("\nName | Type/Species | Training Status | Reserved | Acquisition Country | In Service Country")
    print("-" * 95)

    for a in animals:
        if isinstance(a, Dog):
            type_or_species = a.breed
        elif isinstance(a, Monkey):
            type_or_species = a.species
        else:
            type_or_species = "Unknown"

        print(
            f"{a.name} | {type_or_species} | {a.training_status} | {a.reserved} | "
            f"{a.acquisition_country} | {a.in_service_country}"
        )
    print("")


# Print table for dogs using the search algorithm
def search_dogs():
    # Menu replacement: 
    results = alg.search(species_or_type="dog")
    print_table(results)


# Print table for monkeys using the search algorithm 
def search_monkeys():
    results = alg.search(species_or_type="monkey")
    print_table(results)


# Print table for unreserved animals using the search algorithm
def search_unreserved():
    results = alg.search(reserved=False)
    print_table(results)


# Display menu and questions for intaking a new dog 
def intake_new_dog():
    print("\n--- Intake a New Dog ---")

    name = prompt_text("What is the dog's name? ")
    if animal_exists(name):
        print("\nThis animal is already in our system.\n")
        return

    breed = prompt_text("What is the dog's breed? ")
    gender = prompt_gender()
    age = prompt_int("What is the dog's age? ")
    weight = prompt_float("What is the dog's weight? ")
    acquisition_date = prompt_date("What is the dog's acquisition date? (MM-DD-YYYY) ")
    acquisition_country = prompt_text("What is the dog's acquisition country? ")
    training_status = prompt_text("What is the dog's training status? (intake/Phase I/Phase II/Phase III/Phase IV/in service) ")
    in_service_country = prompt_text("What is the dog's in service country? ")
    reserved = False

    try:
        dog = Dog(
            name, breed, gender, age, weight, acquisition_date, acquisition_country,
            training_status, reserved, in_service_country
        )
        alg.add_animal(dog)
        print(f"\n{dog.name} has been added.\n")
    except ValueError as e:
        print(f"\nError: {e}\n")


# Display menu and questions for intaking a new monkey
def intake_new_monkey():
    print("\n--- Intake a New Monkey ---")

    name = prompt_text("What is the monkey's name? ")
    if animal_exists(name):
        print("\nThis animal is already in our system.\n")
        return

    species = prompt_text("What is the monkey's species? ")
    if species not in ALLOWED_SPECIES:
        print("\nWe do not accept this species.\n")
        return

    gender = prompt_gender()
    age = prompt_int("What is the monkey's age? ")
    weight = prompt_float("What is the monkey's weight? ")
    acquisition_date = prompt_date("What is the monkey's acquisition date? (MM-DD-YYYY) ")
    acquisition_country = prompt_text("What is the monkey's acquisition country? ")
    training_status = prompt_text(
        "What is the monkey's training status? (intake/Phase I/Phase II/Phase III/Phase IV/in service) ")
    in_service_country = prompt_text("What is the monkey's in service country? ")
    tail_length = prompt_float("What is the monkey's tail length? ")
    height = prompt_float("What is the monkey's height? ")
    body_length = prompt_float("What is the monkey's body length? ")
    reserved = False

    try:
        monkey = Monkey(
            name, species, gender, age, weight, acquisition_date, acquisition_country, training_status,
            reserved, in_service_country, tail_length, height, body_length
        )
        alg.add_animal(monkey)
        print(f"\n{monkey.name} has been added.\n")
    except ValueError as e:
        print(f"\nError: {e}\n")


# Display menu and questions for advancing training status 
def advance_training():
    print("\n--- Advance Training Status ---")
    name = prompt_text("Which animal's status would you like to update?: ")

    animal = alg.get_by_name(name)
    if not animal:
        print(f"\n{name} not found.\n")
        return

    # If already final state, display message that the animal cannot advance 
    if animal.training_status == "in service":
        print(f"\n{animal.name} is already 'in service' and cannot advance further.\n")
        return

    # If intake, ask for vet clearance and (if yes) advance to Phase I
    if animal.training_status == "intake":
        print(f"\n{animal.name} is currently in 'intake'.")
        cleared = prompt_yes_no("Has this animal received veterinary clearance?")
        if not cleared:
            print("\nCannot advance. Animal must be vet-cleared to begin training.\n")
            return
        
        try:
            before = animal.training_status
            animal.advance_training()
            after = animal.training_status
            print(f"\n{animal.name} is now vet-cleared and advanced from {before} to {after}.\n")
        except ValueError as e:
            print(f"\nError: {e}\n")
        return

    # Display status update 
    print(f"\nCurrent status: {animal.training_status}")
    print(f"Next status: {animal.next_training_status()}")

    if not prompt_yes_no(f"Advance {animal.name} to next status?"):
        print("\nNo changes made.\n")
        return

    try:
        before = animal.training_status
        animal.advance_training()
        after = animal.training_status
        print(f"\n{animal.name} advanced from {before} to {after}.\n")
    except ValueError as e:
        print(f"\nError: {e}\n")


# Print header and prompt user for animal to reserve then use algorithm to reserve by name
def reserve_animal_customer():
    print("\n--- Reserve an Animal ---")
    name = prompt_text("Enter the animal name you want to reserve: ")
    print("\n" + alg.reserve_by_name(name) + "\n")


# User can search based on type, breed/species, training status, reserved status, and location 
def search():

    print("\n--- Multi-Criteria Search ---")
    print("Leave any field blank to skip that filter.\n")

    species_or_type = input("Species/type (dog/monkey OR breed/species): ").strip()
    training_status = input("Training status: ").strip()
    reserved_raw = input("Reserved? (yes/no/blank): ").strip().lower()
    acquisition_country = input("Acquisition country: ").strip()
    in_service_country = input("In service country: ").strip()

    reserved = None
    if reserved_raw in ("yes", "y"):
        reserved = True
    elif reserved_raw in ("no", "n"):
        reserved = False

    results = alg.search(
        species_or_type=species_or_type if species_or_type else None,
        training_status=training_status if training_status else None,
        reserved=reserved,
        acquisition_country=acquisition_country if acquisition_country else None,
        in_service_country=in_service_country if in_service_country else None,
    )

    print_table(results)


# Print menu and prompt user for selection 
def admin_menu():
    choice = ""
    while choice.lower() != "q":
        print("\nRescue Animal System Menu (ADMIN)")
        print("[1] Intake a new dog")
        print("[2] Intake a new monkey")
        print("[3] Advance training status")
        print("[4] View all dogs")
        print("[5] View all monkeys")
        print("[6] View all unreserved animals")
        print("[7] Multi-criteria search")
        print("[q] Logout\n")

        choice = input("Enter a menu selection: ").strip()

        if choice == "1":
            intake_new_dog()
        elif choice == "2":
            intake_new_monkey()
        elif choice == "3":
            advance_training()
        elif choice == "4":
            search_dogs()
        elif choice == "5":
            search_monkeys()
        elif choice == "6":
            search_unreserved()
        elif choice == "7":
            search()
        elif choice.lower() == "q":
            print("\nLogging out...\n")
        else:
            print("\nInvalid choice. Try again.\n")


# Print menu and prompt user for selection 
def customer_menu():
    choice = ""
    while choice.lower() != "q":
        print("\nRescue Animal System Menu (CUSTOMER)")
        print("[1] View unreserved animals (search-powered)")
        print("[2] Multi-criteria search")
        print("[3] Reserve an animal")
        print("[q] Logout\n")

        choice = input("Enter a menu selection: ").strip()

        if choice == "1":
            search_unreserved()
        elif choice == "2":
            search()
        elif choice == "3":
            customer_reserve()
        elif choice.lower() == "q":
            print("\nLogging out...\n")
        else:
            print("\nInvalid choice. Try again.\n")


# Run security check before authorizing and displaying menu 
def main():
    auth = AuthSystem()
    user = auth.login_prompt()
    if not user:
        return

    if user.role == "admin":
        admin_menu()
    else:
        customer_menu()

    print("Thanks for using Grazioso Salvare.")


if __name__ == "__main__":
    main()
