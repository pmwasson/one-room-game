import textwrap

def lineNumber(val):
   return (val+1)*10

def label(ls):
   if (ls != ''):
      if ls in asLabel:
         print("REM * Warning: label {} redefined".format(ls))
      asLabel[ls] = lineNumber(len(asLines))
      #print("REM label {}={}".format(ls,asLabel[ls]))

def labelStr(ls):
   return "%{}%".format(ls)

def checkFlag(flag):
   if flag not in asFlags:
      asLabel[flag] = len(asFlags)
      asFlags.append(flag)
      #print("REM flag {}={}".format(flag,asLabel[flag]))

def doCont(cont):
   if not cont:
      asLines.append('GOTO {}'.format(labelStr(prompt)))

def getUnique():
   asUnique = asUnique + 1
   return asUnique

def cmdInsert(line,cont=True):
   asLines.append(line)
   doCont(cont)

def cmdPrint(line,cont=True):
   if (line==""):
      asLines.append('?')
   else:
      wrapper = textwrap.TextWrapper(width=79)
      for line in wrapper.wrap(text=line):
         asLines.append('? "{}"'.format(line))
   doCont(cont)

def cmdIfSetGoto(flag,next,cont=True):
   checkFlag(flag)
   asLines.append('IF F({}) GOTO {}'.format(labelStr(flag),labelStr(next)))
   doCont(cont)

def cmdIfClrGoto(flag,next,cont=True):
   checkFlag(flag)
   asLines.append('IF F({})=0 GOTO {}'.format(labelStr(flag),labelStr(next)))
   doCont(cont)

def cmdSet(flag,cont=True):
   checkFlag(flag)
   asLines.append('F({})=1'.format(labelStr(flag)))
   doCont(cont)

def cmdClr(flag,cont=True):
   checkFlag(flag)
   asLines.append('F({})=0'.format(labelStr(flag)))
   doCont(cont)

def replaceVariables(line):
   cont = True
   while(cont):
      cont = False
      # first find variable
      start = line.find('%')
      end = line.find('%',start+1)
      if (start >= 0 and end >= start):
         var = line[start+1:end]
         if var in asLabel:
            svar = line[start:end+1]
            line = line.replace(svar,str(asLabel[var]))
            cont = True
         else:
            print("REM * Warning, variable {} undefined".format(var))
   return line

def action(cmd):
   wordList = cmd.split()
   act = "." + "+".join(wordList)
   asActions.append(act)

   #print("REM action: {}".format(" ".join(wordList)))
   # Put into tree structure

   tree = actionTree

   for w in range(len(wordList)):
      word = wordList[w]
      opt = 0
      if (word[0] == '?'):
         word = word[1:]
         opt = 1
      if word not in tree:
         tree[word] = {}
      if word not in synonymList:
         synonymList[word] = [word]
      if (w == len(wordList)-1):
         tree[word]["!"] = act
      if (opt):
         tree["!"] = act
      tree = tree[word]

   return act

def parseTree(tree,prefix,level=0):
   label(prefix)

   id=0
   final = badParse
   #breadth first
   for key in tree.keys():
      plabel = prefix + "." + str(id)
      id = id +1
      if (key == "*"):
         final = tree[key]["!"]
      elif (type(tree[key]) is dict):
         for word in synonymList[key]:
            cmdInsert('IF W$({}) = "{}" GOTO {}'.format(level,word.upper(),labelStr(plabel)))
      else:
         cmdInsert('IF C={} THEN GOTO {}'.format(level,labelStr(tree[key])))
   cmdInsert('GOTO {}'.format(labelStr(final)))

   id=0
   for key in tree.keys():
      plabel = prefix + "." + str(id)
      id = id +1
      if (type(tree[key]) is dict):
         if (key != "*"):
            parseTree(tree[key],plabel,level+1)

def synonym(base,word):
   if base not in synonymList:
      synonymList[base] = [base]
   synonymList[base].append(word)

def main():
   done = False

   #----------------
   # Game Start
   #----------------
   cmdInsert('REM -------------------------------------')
   cmdInsert('REM  TOY ROOM                           ')
   cmdInsert('REM -------------------------------------')
   cmdInsert('REM  Written by Paul Wasson, August 2021')
   cmdInsert('REM -------------------------------------')
   cmdInsert('? CHR$(4);"PR#3"')
   cmdInsert('DIM F({})'.format(labelStr(flagCount)))
   cmdPrint(            "Welcome to TOY ROOM, a tiny interactive fiction game to test out parsing text in AppleSoft.")
   cmdPrint(            "")
   cmdInsert("GOTO {}".format(labelStr(start)))

   #----------------
   # Scanner
   #----------------

   label(scanner)
   cmdInsert('V=0: FOR I=S TO LEN (A$): IF MID$(A$,I,1)=" " THEN NEXT')
   cmdInsert('IF I > LEN (A$) THEN RETURN') 
   cmdInsert('S=I: FOR I=S TO LEN(A$): IF MID$(A$,I,1)<>" " THEN  NEXT') 
   cmdInsert('E=I-1: V=1:RETURN')

   label(badParse)
   cmdPrint(            "Sorry, I don't understand. Please try a different command.",done)
   #----------------
   # Commands
   #----------------

   # Help
   synonym("help","hint")
   label(action("help"))
   cmdPrint(            "Try using 2 word commands in upper case, like LOOK ROOM or SIT CHAIR. You can try longer commands like OPEN DOOR WITH KEY, but it is not generally needed.")
   cmdPrint(            "Here are some word you can try: LOOK, SIT, STAND, GET, DROP, INVENTORY, OPEN, QUIT.",done)

   # Start
   label(action("new ?game"))
   label(action("start over"))
   cmdPrint(            "Starting the game over from the beginning...")
   cmdPrint(            "")
   cmdInsert("FOR I = 0 to {} : F(I)=0 : NEXT".format(labelStr(flagCount)))
   label(start)
   cmdPrint(            "Your standing in a small room with a closed door.",done)

   # Look
   synonym("look","examine")
   label(action("look ?room"))
   cmdPrint(            "The room is very small with a single door and a chair.",done)

   label(action("look door"))
   cmdPrint(            "It appears to be an ordinary locked door.",done)

   synonym("chair","seat")
   label(action("look chair"))
   cmdPrint(            "It is a pretty boring metal chair with a worn seat and uncomforable back support.")
   cmdIfSetGoto("flagKey",prompt)
   cmdIfClrGoto("flagSit",prompt)
   cmdPrint(            "There is a small key poking out from under the seat.",done)

   label(action("look key"))
   cmdIfClrGoto("flagSit","noLook")   
   cmdPrint(            "It is a small copper colored key.",done)

   synonym("me","self")
   label(action("look me"))
   cmdPrint(            "You seem ordinary.",done)

   label(action("look *"))
   label("noLook")
   cmdPrint("I don't see that!",done)

   # Sit
   label(action("sit ?chair"))
   cmdPrint(            "You sit on the chair but it is so uncomfortable that you decide to stand up again.")
   cmdSet("flagSit")
   cmdIfSetGoto("flagKey",prompt)
   cmdPrint(            "As you get up you see something poking out from under the seat.",done)

   label(action("sit *"))
   cmdPrint(            "I can't sit on that!",done)

   # Stand
   label(action("stand ?up"))
   cmdPrint(            "You are already standing.",done)

   # Get
   label(action("get key"))
   cmdIfSetGoto("flagKey","alreadyGet")
   cmdIfClrGoto("flagSit","noGet")
   cmdSet("flagKey")
   cmdPrint(            "You pick up the key.",done)

   label(action("get *"))
   label("noGet")
   cmdPrint(            "You can't get that!",done)

   label("alreadyGet")
   cmdPrint(            "You already have that!",done)

   # Drop
   label(action("drop key"))
   cmdClr("flagKey")
   cmdPrint(            "You drop the key and if falls back into the seat",done)

   label(action("drop *"))
   cmdPrint(            "You can't drop that!",done)

   # Inventory
   label(action("inventory"))
   cmdIfClrGoto("flagKey","emptyInventory")
   cmdPrint(            "You have a key you found in the chair.",done)
   label("emptyInventory")
   cmdPrint(            "You are not carrying anything interesting.",done)

   # Open
   synonym("open","unlock")
   label(action("open ?door"))
   label(action("open door with key"))
   cmdIfSetGoto("flagKey","unlockedDoor")
   cmdPrint(            "You try to open the door, but it is locked.",done)
   label("unlockedDoor")
   cmdPrint(            "You try the key in the door lock and it fits. You open the door and leave the room. I wonder what happens next...")
   cmdPrint(            "")
   cmdPrint(            "Thanks for playing")
   cmdInsert("END")

   # Quit
   synonym("quit","finish")
   synonym("quit","end")
   label(action("quit ?game"))
   cmdPrint(            "Goodbye.")
   cmdInsert("END")

   #----------------
   # Main input routine
   #----------------

   label(prompt)
   cmdInsert('INVERSE: ?"Command?";: NORMAL: INPUT " ";A$: S=1: C=0')
   cmdInsert('FOR C=0 TO 5: GOSUB {}: IF V THEN W$(C)=MID$(A$,S,E-S+1):S=E+1:NEXT'.format(labelStr(scanner)))

   # Fall into parse

   #----------------
   # Parse
   #----------------
   # Fill in needed values
   parseTree(actionTree,"parse")

   #----------------
   # Defines
   #----------------
   # Fill in needed values

   asLabel[flagCount] = len(asFlags)-1

   # Generate action list
   asLabel[actionList] = ",".join([str(asLabel[i]) for i in asActions])
   asLabel[helpString] = " ".join(["{}={}".format(i+1,asActions[i]) for i in range(len(asActions))])

   #----------------
   # Dump program
   #----------------
   print("NEW")
   lineNum = 0;
   for line in asLines:
      print("{:<5d} {}".format(lineNumber(lineNum),replaceVariables(line)))
      lineNum+=1


# Generate game
asLines = []
asFlags = []
asActions = []
asLabel = {}
actionTree = {}
synonymList = {}

# known labels
prompt = "_prompt"
wait = "_wait"
start = "_start"
actionList = "_actionlist"
helpString = "_help"
flagCount = "_flagCount"
scanner = "_scanner"
badParse = "_badparse"

main()