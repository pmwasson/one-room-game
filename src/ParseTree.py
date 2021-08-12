class Node:
    def __init__(self, data, parent=None):
        self.child = {}
        self.data = data
        if parent is not None:
            parent.child[data] = 


def main():


    room = ""

    sentences = [
        "look under %noun",
        "look in %noun",
        "look %noun",
        "look",
    ]


    sentences = [
        "look",
        "look %noun",
        "look under %noun",
    ]



    verb = ["look","get","drop","put"]
    lookMod = ["under"]

    noun = ["room","chair","clothes","messy clothes","folded clothes"]
    root = Node("parse")
    look = Node("look",root)
    room = Node("room")
    Node("room",look)

    root.child["look"] = Node("look")
    root.child["look"].child[""]


main()