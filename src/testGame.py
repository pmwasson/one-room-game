from GameGen import GameGen

def main():

   done = False
   game = GameGen([
      "---------",
      "Game Test",
      "---------",
      "Written by Paul Wasson, August 2021",
      "",
      "Generated from a python script. For more information, see:",
      "http://https://github.com/pmwasson/one-room-game",
      ""
      ])

   # Start of game
   game.cmdPrint("Welcome to TOY ROOM, a tiny interactive fiction game to test out parsing text in AppleSoft.")
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

