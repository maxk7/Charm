# Dashboard widget for displaying vizualizer settings
from textual.widgets import DataTable
class ToggleDashboard(DataTable):
    symbEnabled, symbDisabled = "▣", "☐"

    ROWS = [
        ["EXTENSIONS", ""],
        ["----------", ""],
        ["Hdra3xtend", symbEnabled],
    ]

    # Helper function to update the table widget
    def refreshDash(self):
        self.clear()
        self.add_rows(self.ROWS)

    # Getters
    def getTestMethod(self):
        return self.ROWS[2][1]

    # Setters
    def setTestMethod(self, value):
        self.ROWS[2][1] = value
