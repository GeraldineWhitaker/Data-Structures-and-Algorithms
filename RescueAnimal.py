# Geraldine Whitaker
# This file is stores the attributes and validation logic for all rescue animals

from dataclasses import dataclass
from typing import ClassVar, List


@dataclass
class RescueAnimal:

    # Allowed training statuses for validation
    ALLOWED_STATUSES: ClassVar[List[str]] = [
        "intake", "Phase I", "Phase II", "Phase III", "Phase IV", "in service"
    ]

    # Defines transitions for training status
    UPDATE_STATUS: ClassVar[dict[str, str]] = {
        "intake": "Phase I",
        "Phase I": "Phase II",
        "Phase II": "Phase III",
        "Phase III": "Phase IV",
        "Phase IV": "in service",
        "in service": "in service"
    }

    # Shared variables for dog and monkey
    name: str
    gender: str
    age: int
    weight: float
    acquisition_date: str
    acquisition_country: str
    training_status: str
    reserved: bool
    in_service_country: str

    def __post_init__(self):

        # Validate Name is not empty
        self.name = self.name.strip()
        if not self.name:
            raise ValueError("Name cannot be empty.")

        # Validate gender is not empty and is either "male" or "female"
        self.gender = self.gender.strip().lower()
        if not self.gender:
            raise ValueError("Gender cannot be empty.")
        if self.gender not in ("male", "female"):
            raise ValueError("Gender must be 'male' or 'female'.")

        # Validate age is an integer that is greater than 0
        if not isinstance(self.age, int) or self.age <= 0:
            raise ValueError("Age must be a greater than 0.")

        # Validate weight is either an integer or float that is greater than 0
        if not isinstance(self.weight, (int, float)) or float(self.weight) <= 0:
            raise ValueError("Weight must be greater than 0.")
        self.weight = float(self.weight)

        # Validate acquisition date format (MM-DD-YYYY)
        self.acquisition_date = self.acquisition_date.strip()
        if not self.valid_date(self.acquisition_date):
            raise ValueError("Acquisition date must be in MM-DD-YYYY format.")

        # Validate acquisition country is not empty
        self.acquisition_country = self.acquisition_country.strip()
        if not self.acquisition_country:
            raise ValueError("Acquisition country cannot be empty.")

        # Validate training status is one of the allowed statuses
        self.training_status = self.training_status.strip()
        if self.training_status not in self.ALLOWED_STATUSES:
            raise ValueError(
                "Training status must be one of: " + ", ".join(self.ALLOWED_STATUSES)
            )

        # Validate in-service country is not empty
        self.in_service_country = self.in_service_country.strip()
        if not self.in_service_country:
            raise ValueError("In service country cannot be empty.")

        # Validate reserved status
        if not isinstance(self.reserved, bool):
            raise ValueError("Reserved must be True or False")

    # Only animals in service and not already reserved are eligible to be reserved
    def is_reservable(self):
        return self.training_status == "in service" and self.reserved is False

    # Returns the next state in training
    def next_training_status(self):
        return self.UPDATE_STATUS.get(self.training_status, self.training_status)

    # Advance training to next state and considers veterinary clearance
    def advance_training(self):
        if self.training_status == "in service":
            raise ValueError("Animal is already in service and cannot advance further.")

        self.training_status = self.next_training_status()

    @staticmethod
    # Ensures that acquisition date is valid and in correct format
    def valid_date(value: str):
        parts = value.split("-")
        if len(parts) != 3:
            return False
        mm, dd, yyyy = parts
        if not (mm.isdigit() and dd.isdigit() and yyyy.isdigit()):
            return False
        if len(yyyy) != 4:
            return False
        m = int(mm)
        d = int(dd)
        y = int(yyyy)
        return 1 <= m <= 12 and 1 <= d <= 31 and y > 1970
