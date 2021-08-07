import textwrap

class GameGen:

   # class variable
   
   screenWidth = 80
   lineNumberWidth = 4

   # known labels
   prompt = "_prompt"
   start = "_start"
   actionList = "_actionlist"
   flagCount = "_flagCount"
   scanner = "_scanner"
   parser = "_parser"
   badParse = "_badparse"

   def __init__(self, comment, maxWords=4):
      self.maxWords = maxWords
      self.asLines = []
      self.asFlags = []
      self.asActions = []
      self.asLabel = {}
      self.actionTree = {}
      self.synonymList = {}
      self.cmdRem(comment)
      self.boilerPlate()

   def lineNumber(self,val):
      return (val+1)*1

   def label(self,ls):
      if (ls != ''):
         if ls in self.asLabel:
            print("REM * Warning: label {} redefined".format(ls))
         self.asLabel[ls] = self.lineNumber(len(self.asLines))
         #print("REM label {}={}".format(ls,self.asLabel[ls]))

   def labelStr(self,ls):
      return "%{}%".format(ls)

   def checkFlag(self,flag):
      if flag not in self.asFlags:
         self.asLabel[flag] = len(self.asFlags)
         self.asFlags.append(flag)
         #print("REM flag {}={}".format(flag,self.asLabel[flag]))

   def doCont(self,cont):
      if not cont:
         self.cmdGoto(self.prompt)

   def cmdInsert(self,line,cont=True):
      self.asLines.append(line)
      self.doCont(cont)

   def cmdPrint(self,line="",cont=True):
      if (line==""):
         self.asLines.append('?')
      else:
         wrapper = textwrap.TextWrapper(width=self.screenWidth-1)
         for line in wrapper.wrap(text=line):
            self.asLines.append('? "{}"'.format(line))
      self.doCont(cont)  

   def cmdRem(self,lines):
      for line in lines:
         self.asLines.append('REM * {}'.format(line))

   def cmdGoto(self,next=prompt):
      self.asLines.append('GOTO {}'.format(self.labelStr(next)))

   def cmdIfSetGoto(self,flag,next=prompt,cont=True):
      self.checkFlag(flag)
      self.asLines.append('IF F({}) GOTO {}'.format(self.labelStr(flag),self.labelStr(next)))
      self.doCont(cont)

   def cmdIfValGoto(self,flag,val,next=prompt,cont=True):
      self.checkFlag(flag)
      self.asLines.append('IF F({})={} GOTO {}'.format(self.labelStr(flag),val,self.labelStr(next)))
      self.doCont(cont)

   def cmdIfClrGoto(self,flag,next=prompt,cont=True):
      self.cmdIfValGoto(flag,0,next,cont)

   def cmdSet(self,flag,val=1,cont=True):
      self.checkFlag(flag)
      self.asLines.append('F({})={}'.format(self.labelStr(flag),val))
      self.doCont(cont)

   def cmdClr(self,flag,cont=True):
      self.cmdSet(flag,0,cont)

   def replaceVariables(self,line):
      cont = True
      while(cont):
         cont = False
         # first find variable
         start = line.find('%')
         end = line.find('%',start+1)
         if (start >= 0 and end >= start):
            var = line[start+1:end]
            if var in self.asLabel:
               svar = line[start:end+1]
               line = line.replace(svar,str(self.asLabel[var]))
               cont = True
            else:
               print("REM * Warning, variable {} undefined".format(var))
      return line

   def action(self,cmd):
      wordList = cmd.split()
      act = "." + "+".join(wordList)
      self.asActions.append(act)

      # Put into tree structure
      tree = self.actionTree
      for w in range(len(wordList)):
         word = wordList[w]
         opt = 0
         if (word[0] == '?'):
            word = word[1:]
            opt = 1
         if word not in tree:
            tree[word] = {}
         if word not in self.synonymList:
            self.synonymList[word] = [word]
         if (w == len(wordList)-1):
            tree[word]["!"] = act
         if (opt):
            tree["!"] = act
         tree = tree[word]

      return act

   def parseTree(self,tree,prefix,level=0):
      self.label(prefix)
      id=0
      final = self.badParse
      #breadth first
      for key in tree.keys():
         plabel = prefix + "." + str(id)
         id = id +1
         if (key == "*"):
            final = tree[key]["!"]
         elif (type(tree[key]) is dict):
            for word in self.synonymList[key]:
               self.cmdInsert('IF W$({}) = "{}" GOTO {}'.format(level,word.upper(),self.labelStr(plabel),plabel))
         else:
            self.cmdInsert('IF C={} THEN GOTO {}'.format(level,self.labelStr(tree[key])))
      self.cmdGoto(final)

      id=0
      for key in tree.keys():
         plabel = prefix + "." + str(id)
         id = id +1
         if (type(tree[key]) is dict):
            if (key != "*"):
               self.parseTree(tree[key],plabel,level+1)

   def synonym(self,base,word):
      if base not in self.synonymList:
         self.synonymList[base] = [base]
      self.synonymList[base].append(word)


   def generate(self):
      # Set final values
      self.asLabel[self.flagCount] = max(0,len(self.asFlags)-1)

      # Generate parser
      self.label(self.parser)
      self.parseTree(self.actionTree,"parse")

      # Dump program
      print("NEW")
      lineNum = 0;
      fmt = "{:<"+str(self.lineNumberWidth)+"} {}"
      for line in self.asLines:
         print(fmt.format(self.lineNumber(lineNum),self.replaceVariables(line)))
         lineNum+=1

   def boilerPlate(self):

      # Top of program
      self.cmdInsert('TEXT:NORMAL:? CHR$(4);"PR#3"')
      self.cmdInsert('DIM W$({}): DIM F({})'.format(self.maxWords,self.labelStr(self.flagCount)))
      self.cmdGoto(self.start)

      # Scanner
      self.label(self.scanner)
      self.cmdInsert('V=0: FOR I=S TO LEN (A$): IF MID$(A$,I,1)=" " THEN NEXT')
      self.cmdInsert('IF I > LEN (A$) THEN RETURN') 
      self.cmdInsert('S=I: FOR I=S TO LEN(A$): IF MID$(A$,I,1)<>" " THEN  NEXT') 
      self.cmdInsert('E=I-1: V=1:RETURN')

      # Prompt
      self.label(self.prompt)
      self.cmdInsert('FOR C=0 TO {}: W$(C)="": NEXT: I=FRE(0)'.format(self.maxWords))
      self.cmdInsert('INVERSE: ?"Command?";: NORMAL: INPUT " ";A$: S=1')
      self.cmdInsert('FOR C=0 TO {}: GOSUB {}: IF V THEN W$(C)=MID$(A$,S,E-S+1):S=E+1:NEXT'.format(self.maxWords,self.labelStr(self.scanner)))
      self.cmdGoto(self.parser)

      # Default message
      self.label(self.badParse)
      self.cmdPrint("Sorry, I don't understand. Please try a different command.",False)

      # Start of game
      self.label(self.start)

      # Reset state
      self.cmdInsert("FOR I=0 to {}: F(I)=0: NEXT".format(self.labelStr(self.flagCount)))

def main():

   done = False
   game = GameGen([
      "--------",
      "TOY ROOM",
      "--------",
      "Written by Paul Wasson, August 2021",
      "",
      "Generated from a python script. For more information, see:",
      "http://https://github.com/pmwasson/one-room-game",
      ""
      ])

   # Start of game
   game.cmdPrint("Welcome to TOY ROOM, a tiny interactive fiction game to test out parsing text in AppleSoft.",done)
   game.cmdPrint()
   game.cmdPrint("Your standing in a small room with a closed door.",done)

   # Restart
   game.synonym("new","reset")
   game.synonym("new","restart")
   game.label(game.action("new ?game"))
   game.label(game.action("start ?over"))
   game.cmdGoto(game.start)

   # Help
   game.synonym("help","hint")
   game.label(game.action("help"))
   game.cmdPrint("Try using 2 word commands in upper case, like LOOK ROOM or SIT CHAIR. You can try longer commands like OPEN DOOR WITH KEY, but it is not generally needed.")
   game.cmdPrint("Here are some word you can try: LOOK, SIT, STAND, GET, DROP, INVENTORY, OPEN, QUIT.",done)

   # Look
   game.synonym("look","examine")
   game.label(game.action("look ?room"))
   game.cmdPrint("The room is very small with a single door and a chair.",done)

   game.label(game.action("look door"))
   game.cmdPrint("It appears to be an ordinary locked door.",done)

   game.synonym("chair","seat")
   game.label(game.action("look chair"))
   game.cmdPrint("It is a pretty boring metal chair with a worn seat and uncomforable back support.")
   game.cmdIfSetGoto("flagKey")
   game.cmdIfClrGoto("flagSit")
   game.cmdPrint("There is a small key poking out from under the seat.",done)

   game.label(game.action("look key"))
   game.cmdIfClrGoto("flagSit","noLook")   
   game.cmdPrint("It is a small copper colored key.",done)

   game.synonym("me","self")
   game.label(game.action("look me"))
   game.cmdPrint("You seem ordinary.",done)

   game.label(game.action("look *"))
   game.label("noLook")
   game.cmdPrint("I don't see that!",done)

   # Sit
   game.label(game.action("sit ?chair"))
   game.label(game.action("sit on chair"))
   game.label(game.action("sit in chair"))
   game.cmdPrint("You sit on the chair but it is so uncomfortable that you decide to stand up again.")
   game.cmdSet("flagSit")
   game.cmdIfSetGoto("flagKey")
   game.cmdPrint("As you get up you see something poking out from under the seat.",done)

   game.label(game.action("sit *"))
   game.cmdPrint("I can't sit on that!",done)

   # Stand
   game.label(game.action("stand ?up"))
   game.cmdPrint("You are already standing.",done)

   # Get
   game.label(game.action("get key"))
   game.cmdIfSetGoto("flagKey","alreadyGet")
   game.cmdIfClrGoto("flagSit","noGet")
   game.cmdSet("flagKey")
   game.cmdPrint("You pick up the key.",done)

   game.label(game.action("get chair"))
   game.cmdPrint("The chair is too bulky to carry around.",done)

   game.label(game.action("get door"))
   game.cmdPrint("The door is affixed to the wall.",done)

   game.label(game.action("get *"))
   game.label("noGet")
   game.cmdPrint("You can't get that!",done)

   game.label("alreadyGet")
   game.cmdPrint("You already have that!",done)

   # Drop
   game.label(game.action("drop key"))
   game.cmdIfClrGoto("flagKey","noDrop")
   game.cmdClr("flagKey")
   game.cmdPrint("You drop the key and if falls back into the seat",done)

   game.label(game.action("drop *"))
   game.label("noDrop")
   game.cmdPrint(            "You can't drop that!",done)

   # Inventory
   game.label(game.action("inventory"))
   game.cmdIfClrGoto("flagKey","emptyInventory")
   game.cmdPrint("You have a key you found in the chair.",done)
   game.label("emptyInventory")
   game.cmdPrint("You are not carrying anything interesting.",done)

   # Open
   game.synonym("open","unlock")
   game.label(game.action("open ?door"))
   game.label(game.action("open door with key"))
   game.cmdIfSetGoto("flagKey","unlockedDoor")
   game.cmdPrint("You try to open the door, but it is locked.",done)
   game.label("unlockedDoor")
   game.cmdPrint("You try the key in the door lock and it fits. You open the door and leave the room. I wonder what happens next...")
   game.cmdPrint("")
   game.cmdPrint("Thanks for playing")
   game.cmdInsert("END")

   # Quit
   game.synonym("quit","finish")
   game.synonym("quit","end")
   game.label(game.action("quit ?game"))
   game.cmdPrint("Goodbye.")
   game.cmdInsert("END")

   # Generate game
   game.generate()

main()

