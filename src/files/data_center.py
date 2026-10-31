import datetime
from pathlib import Path

import pandas as pd
from pyftg.models.character_data import CharacterData

class DataCenter():
    """
    Export class that transforms CharacterData information into a CSV.
    """
    def __init__(self):
        self.char_history = []

    def add_char_data(self, char_data: CharacterData):
        """
        Appends char_data to class attribute list.

        Args:
        char_data: CharacterData class instance
        """
        self.char_history.append(char_data)

    def export_data(self):
        """
        Exports class attributes to local data file.
        """
        now = datetime.datetime.now()
        file_prefix = now.strftime("%Y-%m-%d_%H-%M-%S")

        folder_path = Path(__file__).resolve().parent.parent / "round_data" / file_prefix
        folder_path.mkdir(parents=True, exist_ok=True)

        file_name = f"{file_prefix}.csv"
        full_output_path = folder_path / file_name

        df = pd.DataFrame(self.char_history)
        df.to_csv(full_output_path, index=False, encoding="utf-8")

        self._flush_data()

        return file_prefix

    def _flush_data(self):
        self.char_history = []

