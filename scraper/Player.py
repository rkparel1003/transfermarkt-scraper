
'''
    Object that encapsulates all of a players data.
    Player's data is retrieved from the table of players on club pages.
'''

class Player():
    def __init__(self, number: str, name: str, position: str, dob: str, nationalities: str, value: str):
        self.number = number
        self.name = name
        self.position = position
        self.dob = dob
        self.nationalities = nationalities
        self.value = value

    def __str__(self) -> str:
        return f"{self.number}, {self.name}, {self.position}, {self.dob}, {self.nationalities}, {self.value}"