import textwrap

def label(ls):
   if (ls != ''):
      if ls in asLabel:
         print("REM * Warning: label {} redefined".format(ls))
      asLabel[ls] = len(asLines)
      print("REM {}={}".format(ls,asLabel[ls]))

def labelStr(ls):
   return "%{}%".format(ls)

def checkFlag(flag):
   if flag not in asFlags:
      asLabel[flag] = len(asFlags)-1
      asFlags.append(flag)
      print("REM {}={}".format(flag,asLabel[flag]))

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

def action(cmd):
   wordList = cmd.split()
   act = "." + "+".join(wordList)
   asActions.append(act)
   return act

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

def main():
   done = False


   #----------------
   # Game Start
   #----------------
   cmdInsert('REM Written by Paul Wasson, August 2021')
   cmdInsert('? CHR$(4);"PR#3"')
   cmdInsert('DIM F({})'.format(labelStr(flagCount)))
   cmdPrint(            "Welcome to ESCAPE ROOM, an entire text adventure for the Apple computer with only a single room. Try to escape!")
   cmdPrint(            "")
   cmdInsert("GOTO {}".format(labelStr(start)))

   #----------------
   # Commands
   #----------------

   # Help
   label(action("help"))
   label(action("hint"))
   cmdPrint(            "Valid commands: {}".format(labelStr(helpString)),done)

   # Start
   label(action("new ?game"))
   label(action("start over"))
   cmdPrint(            "Starting the game over from the beginning...")
   cmdPrint(            "")
   cmdInsert("FOR I = 0 to {} : F(I)=0 : NEXT".format(labelStr(flagCount)))
   label(start)
   cmdPrint(            "Your standing in a small room with a closed door.",done)

   # Look
   label(action("look ?room"))
   cmdPrint(            "The room is very small with a single door and a chair.",done)

   label(action("look door"))
   cmdPrint(            "It appears to be an ordinary locked door.",done)

   label(action("look chair"))
   cmdPrint(            "It is a pretty boring metal chair with a worn seat and uncomforable back support.")
   cmdIfSetGoto("flagKey",prompt)
   cmdIfClrGoto("flagSit",prompt)
   cmdPrint(            "There is a small key poking out from under the seat.",done)

   label(action("look key"))
   cmdIfClrGoto("flagSit","noLook")   
   cmdPrint(            "It is a small copper colored key.",done)

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

   # Open
   label(action("open ?door"))
   cmdIfSetGoto("flagKey","unlockedDoor")
   cmdPrint(            "You try to open the door, but it is locked.",done)
   label("unlockedDoor")
   cmdPrint(            "You try the key in the door lock and it fits. You open the door and leave the room. I wonder what happens next...")
   cmdInsert("END")

   # Quit
   label(action("quit"))
   cmdPrint(            "Goodbye.")
   cmdInsert("END")

   #----------------
   # Main input routine
   #----------------

   label(prompt)
   cmdInsert('INVERSE : ?"Command?"; : NORMAL : INPUT " ";C')
   cmdInsert('ON C GOTO {}'.format(labelStr(actionList)))
   cmdPrint(            "Sorry, but I don't understand. Try a different command.")
   cmdInsert('GOTO {}'.format(labelStr(prompt)))

   #----------------
   # Defines
   #----------------
   # Fill in needed values

   asLabel[flagCount] = len(asFlags)-2

   # Generate action list
   asLabel[actionList] = ",".join([str(asLabel[i]) for i in asActions])
   asLabel[helpString] = " ".join(["{}={}".format(i+1,asActions[i]) for i in range(len(asActions))])

   # Dump program
   print("NEW")
   lineNum = 0;
   for line in asLines:
      print("{:<5d} {}".format(lineNum,replaceVariables(line)))
      lineNum+=1


# Generate game
asLines = [];
asFlags = ['flagDummy']  # applesoft arrays start with 1
asActions = [];
asLabel = {};

# known labels
prompt = "_prompt"
wait = "_wait"
start = "_start"
actionList = "_actionlist"
helpString = "_help"
flagCount = "_flagCount"

main()