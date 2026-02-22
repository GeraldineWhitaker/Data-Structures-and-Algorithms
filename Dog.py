# Geraldine Whitaker
# This file extends the RescueAnimal class to include dog-specific attributes
from RescueAnimal import RescueAnimal


class Dog(RescueAnimal):
    def __init__(
        self,
        name: str,
        breed: str,
        gender: str,
        age: int,
        weight: float,
        acquisition_date: str,
        acquisition_country: str,
        training_status: str,
        reserved: bool,
        in_service_country: str
    ):
        # Store dog-specific variable
        self.breed = breed

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

        # Validate breed is not empty
        self.breed = self.breed.strip()
        if not self.breed:
            raise ValueError("Breed cannot be empty.")
