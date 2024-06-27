# Dashboard widget for displaying vizualizer settings
from textual.widgets import DataTable

class HydraDashboard(DataTable):
    ROWS = [
        ["HYDRA SETTINGS", "VALUE"],
        ["--------------", "-----"],
        ["Thresh", 3.00],
        ["Attack", 0.60]
    ]

    # Helper function to update the table widget
    def refreshDash(self):
        self.clear()
        self.add_rows(self.ROWS)

    # Getters
    def getCutoff(self):
        return self.ROWS[2][1]


    def getSmooth(self):
        return self.ROWS[3][1]


    # Setters
    def setCutoff(self, value):
        self.ROWS[2][1] = value


    def setSmooth(self, value):
        self.ROWS[3][1] = value
