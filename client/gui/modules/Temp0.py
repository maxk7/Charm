from textual.widgets import Label
from datetime import datetime
import random

class Tempo(Label):
    timeArray = []

    def addTime(self):
        self.timeArray.append(datetime.now())
        self.tempo = 0

    def solveTempo(self):
        duration = self.timeArray[7] - self.timeArray[0]
        self.tempo = 420 / duration.total_seconds()
        return self.tempo

    def updateWidget(self):
        numberTaps = len(self.timeArray)

        if len(self.timeArray) <= 7:
            self.update(''.join([random.choice(["♪", "♫"]) for _ in range(0, numberTaps)]) + "‧"*(8-numberTaps) + "  ‧ ")

        if numberTaps == 8:
            tempo = str(round(self.solveTempo()))
            self.update(''.join([random.choice(["♪", "♫"]) for _ in range(0, 8)]) + " "*(4-len(tempo)) + tempo)
            self.timeArray.clear()

    def tap(self):
        self.addTime()
        self.updateWidget()
