# Geraldine Whitaker
# This file extends the RescueAnimal class to include monkey-specific attributes

from RescueAnimal import RescueAnimal


# List of allowed monkey species 
class Monkey(RescueAnimal):
    ALLOWED_SPECIES = ["Capuchin", "Guenon", "Marmoset", "Squirrel Monkey", "Tamarin", "Macaque"]

    def __init__(
        self,
        name: str,
        species: str,
        gender: str,
        age: int,
        weight: float,
        acquisition_date: str,
        acquisition_country: str,
        training_status: str,
        reserved: bool,
        in_service_country: str,
        tail_length: float,
        height: float,
        body_length: float
    ):
        # Store monkey-specific variable
        self.species = species
        self.tail_length = tail_length
        self.height = height
        self.body_length = body_length

        # Initialize the shared RescueAnimal variables
        super().__init__(
            name=name,
            gender=gender,
            age=age,
            weight=weight,
            acquisition_date=acquisition_date,
            acquisition_country=acquisition_country,
            training_status=training_status,
            reserved=reserved,
            in_service_country=in_service_country
        )

        # Validate species is not empty and is on the allowed species list
        self.species = self.species.strip()
        if not self.species:
            raise ValueError("Species cannot be empty.")
        if not any(self.species.lower() == s.lower() for s in self.ALLOWED_SPECIES):
            raise ValueError("Species must be one of: " + ", ".join(self.ALLOWED_SPECIES))

        # Validate all measurements are greater than 0
        if self.tail_length <= 0:
            raise ValueError("Tail length must be greater than 0.")
        if self.height <= 0:
            raise ValueError("Height must be greater than 0.")
        if self.body_length <= 0:
            raise ValueError("Body length must be greater than 0.")
