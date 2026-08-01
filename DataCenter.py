import datetime
import os
from pyftg.models.character_data import CharacterData

class DataCenter():
    def __init__(self):
        self.char_history = []

    def add_char_data(self, char_data: CharacterData):
        self.char_history.append(char_data)

    def export_data(self):
        """
        Exports class attributes to local data file.
        """
        now = datetime.datetime.now().replace(microsecond=0)
        date = now.date()
        time = now.time()

        file_prefix = str(date) + "_" + str(time)

        os.makedirs("reports", exist_ok=True)
        os.makedirs(os.path.join("reports", file_prefix))