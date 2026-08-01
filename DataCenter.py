import datetime
import os

class DataCenter():
    def __init__(self):
        self.action_history = []

    def add_action(self, action: str):
        self.action_history.append(action)

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