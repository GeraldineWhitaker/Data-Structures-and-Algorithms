# Geraldine Whitaker
# This file contains the logic for:
# - Reservation rules
# - Training phase updates
# - Multi-criteria search


from typing import List, Dict, Optional
from RescueAnimal import RescueAnimal
from Dog import Dog
from Monkey import Monkey


class Algorithms:
    def __init__(self, dogs: List[Dog], monkeys: List[Monkey]):
        # store in memory lists
        self.dogs = dogs
        self.monkeys = monkeys

        # Dictionary index for quickly looking for animal
        self.name_index: Dict[str, RescueAnimal] = {}
        self.rebuild_index()

    # Rebuild the index to quickly find animals by name
    def rebuild_index(self):
        self.name_index.clear()
        for d in self.dogs:
            self.name_index[d.name.lower()] = d
        for m in self.monkeys:
            self.name_index[m.name.lower()] = m

    # Check if a name exists
    def name_exists(self, name: str):
        return name.strip().lower() in self.name_index

    # Return animal by name
    def get_by_name(self, name: str):
        return self.name_index.get(name.strip().lower())

    # If animal type is accepted and name is not already in system, add animal
    def add_animal(self, animal: RescueAnimal):
        key = animal.name.lower()
        if key in self.name_index:
            raise ValueError("This animal is already in our system")

        if isinstance(animal, Dog):
            self.dogs.append(animal)
        elif isinstance(animal, Monkey):
            self.monkeys.append(animal)
        else:
            raise ValueError("We do not currently except this animal type.")

        self.name_index[key] = animal

    # Reserve animal by name, display error message if animal is not found, already reserved, or not eligible
    def reserve_by_name(self, name: str):
        animal = self.get_by_name(name)
        if not animal:
            return f"{name} not found. Please try again."

        if animal.reserved:
            return f"{animal.name} is already reserved."

        if not animal.is_reservable():
            return f"{animal.name} is not eligible for reservation until it is in service."

        animal.reserved = True
        return f"{animal.name} has been reserved."

    # Advance training using animals name
    def advance_training(self, name: str):
        animal = self.get_by_name(name)
        if not animal:
            return f"{name} not found. Please try again."

        if animal.training_status == "in service":
            return f"{animal.name} is already 'in service' and cannot advance further."

        before = animal.training_status
        try:
            animal.advance_training()
        except ValueError as e:
            return f"Cannot advance training: {e}"

        after = animal.training_status
        return f"{animal.name} advanced from {before} to {after}."

    # Allows user to search using multiple filters at once
    def search(
            self, species_or_type: Optional[str] = None, training_status: Optional[str] = None,
            reserved: Optional[bool] = None, acquisition_country: Optional[str] = None,
            in_service_country: Optional[str] = None ) -> List[RescueAnimal]:
        results: List[RescueAnimal] = []
        all_animals: List[RescueAnimal] = self.dogs + self.monkeys

        sp = species_or_type.strip().lower() if isinstance(species_or_type, str) and species_or_type.strip() else None
        ts = training_status.strip() if isinstance(training_status, str) and training_status.strip() else None
        ac = acquisition_country.strip().lower() if isinstance(acquisition_country,
                                                               str) and acquisition_country.strip() else None
        isc = in_service_country.strip().lower() if isinstance(in_service_country,
                                                               str) and in_service_country.strip() else None

        for a in all_animals:
            if reserved is not None and a.reserved != reserved:
                continue
            if ts is not None and a.training_status != ts:
                continue
            if ac is not None and a.acquisition_country.lower() != ac:
                continue
            if isc is not None and a.in_service_country.lower() != isc:
                continue

            if sp is not None:
                if isinstance(a, Dog):
                    if sp != "dog" and sp != a.breed.lower():
                        continue
                if isinstance(a, Monkey):
                    if sp != "monkey" and sp != a.species.lower():
                        continue

            results.append(a)

        return results
