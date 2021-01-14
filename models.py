class Form:
    def __init__(self):
        self.value = 0
        self.filled = 0
        self.announcement = None
        self.columns = [Column(i+1) for i in range(4)]
        self.dice = [Dice(i+1) for i in range(5)]

    def __repr__(self):
        string = ""
        for i in range(13):
            string += '| '
            for j in range(4):
                if self.columns[j].boxes[i].filled:
                    string += str(self.columns[j].boxes[i].value) + ' | '
                else:
                    string += '- | '
            string += '</br>'
        return string

class Column:
    def __init__(self, column_type):
        self.column_type = column_type
        self.boxes = [Box(i+1) for i in range(13)]

    def __repr__(self):
        string = str(self.column_type)
        for i in self.boxes:
            string += str(i) + "\n"
        return string


class Box:
    def __init__(self, box_type):
        self.value = 0
        self.filled = 0
        self.available = 0
        self.box_type = box_type

    def __repr__(self):
        string = str(self.box_type) + ": " + str(self.value) + "(filled: " + str(self.filled) + ", available: " + str(self.available) + ")"
        return string


class Dice:
    def __init__(self, ordinal_number):
        self.ordinal_number = ordinal_number
        self.value = 6
    
    def __repr__(self):
        string = str(self.ordinal_number) + ": " + str(self.value)
        return string
