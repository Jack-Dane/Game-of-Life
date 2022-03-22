
from gameOfLife.Views.view import View
from gameOfLife.Observers.observer import Observer


class PrintView(View, Observer):

    def notify(self, subject):
        self.clearScreen()
        self.printData(subject)

    def printData(self, subject):
        print("=" * subject.columns)
        for y in range(subject.rows):
            row = ""
            for x in range(subject.columns):
                row += str(subject.grid[y][x])
            print(row)
        print("=" * subject.columns)

    def clearScreen(self):
        for i in range(20):
            print()
