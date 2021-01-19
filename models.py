class Game:
    def __init__(self):
        self.announcement = None
        self.roll_count = 0
        self.dice = []
        for i in range(5):
            dice = {}
            dice["ordinal_number"] = i
            dice["value"] = i%6+1
            self.dice.append(dice)
        self.form = {}
        self.form["columns"] = []
        for i in range(4):
            column = {}
            column["type"] = i
            column["boxes"] = []
            for j in range(13):
                box = {}
                box["type"] = j
                box["value"] = 0
                box["filled"] = 0
                box["available"] = 0
                column["boxes"].append(box)
            self.form["columns"].append(column)


    def __repr__(self):
        string = ""
        for d in self.dice:
            
            C='o '
            dice_string =  '-----\n|'+C[d["value"]<1]+' '+C[d["value"]<3]+'|\n|'+C[d["value"]<5]
            string += dice_string+C[d["value"]&1]+dice_string[::-1]
            string += "\n"
        string += "\n"
        for i in range(13):
            string += '| '
            for j in range(4):
                if self.form["columns"][j]["boxes"][i]["filled"]:
                    string += str(self.form["columns"]
                                  [j]["boxes"][i]["value"]) + ' | '
                else:
                    string += '- | '
            string += '</br>'
        return string

    def to_dict(self):
        return dict((key, value) for (key, value) in self.__dict__.items())
