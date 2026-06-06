from enum import Enum


class Destination(Enum):
    NYC = "New York"
    MIA = "Miami"


station1 = Destination("New York")
station2 = Destination.MIA

print(station1, station2)
print(station1.name, station1.value)
print(station2.name, station2.value)
