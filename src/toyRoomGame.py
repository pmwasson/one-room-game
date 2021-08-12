from GameGen import GameGen

def main():

   done = False
   game = GameGen([
      "--------",
      "TOY ROOM",
      "--------",
      "Written by Paul Wasson, August 2021",
      "",
      "Generated from a python script. For more information, see:",
      "https://github.com/pmwasson/one-room-game",
      ""
      ])

   # Start of game
   game.cmdPrint("'Mom, its not fair! She was being mean to me, so why do I have to stay in my room and she can go play with her friends?', you say.")
   game.cmdPrint()
   game.cmdPrint("Mom says, 'Just think about what you said. There are plenty of things to keep you busy in there while you cool down.'")
   game.cmdPrint()
   game.cmdPrint("You are in your bedroom. Its messy and you want to leave.",done)

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
   game.cmdPrint("Here are some word you can try: LOOK, SIT, STAND, GET, DROP, PUT, INVENTORY, OPEN, QUIT.",done)

   # Look
   game.synonym("look","examine")
   game.label(game.action("look ?room"))
   game.cmdPrint("You look around your bedroom. You see a desk with some homework on it and a chair.")
   game.cmdAltPrint("flagBed","There is a bed that is neatly made.","There is a bed that is unmade with the blanket half off of it.")
   game.cmdIfPrint("flagClothes",0,"A pile of clothes cover part of the floor.")
   game.cmdIfPrint("flagToys",0,"A lot of toys are piled up in the corner of the room.")
   game.cmdPrint("There is also a toybox, a dresser, and a closet. There is one door but your not sure if you shouldn't leave yet.",done)
   game.cmdIfPrint("flagSit",1,"You are sitting in the chair.")
   game.cmdIfPrint("flagSleep",1,"You are lying in bed.")

   game.label(game.action("look clothes"))
   game.synonym("clothes","laundry")
   game.cmdIfPrint("flagClothesGone",1,"I don't see the clothes here.")
   game.cmdIfSetGoto("flagClothesGone")
   game.cmdAltPrint("flagClothesState","The clothes are all stacked and neatly folded.",
                                       "It is a random pile of clothes. At least they don't smell too bad.",done)

   game.synonym("bed","blanket")
   game.synonym("bed","pillow")
   game.label(game.action("look bed"))
   game.cmdAltPrint("flagBed","Your bed is very comfortable and is very neat with the pillows arranged nicely.",
      "You know how to make your bed, you just don't like to.",done)
   game.label(game.action("look under bed"))
   game.cmdPrint("You look under the bed and a Grue eats you.  Game over!")
   game.cmdInsert('INPUT "Press RETURN to restart game> ";A$')
   game.cmdGoto(game.start)

   game.label(game.action("look door"))
   game.cmdPrint("Mom probably doesn't want you to leave yet.",done)

   game.synonym("chair","seat")
   game.label(game.action("look chair"))
   game.cmdPrint("It is a small desk chair.",done)

   game.synonym("me","self")
   game.label(game.action("look me"))
   game.cmdPrint("You are feeling a little calmer, but are still mad. (Try INVENTORY to see what you are carrying.)",done)

   game.label(game.action("look *"))
   game.cmdPrint("I don't see that!",done)

   # Make
   game.label(game.action("make bed"))
   game.label(game.action("make up bed"))
   game.cmdGosub("autoStand")
   game.cmdPrint("You make the bed like Mom taught you.")
   game.cmdSet("flagBed",done)

   # Fold
   game.label(game.action("fold ?clothes"))
   game.cmdGosub("autoStand")
   game.cmdPrint("It takes a bit of time, but you fold up all the laundry.")
   game.cmdSet("flagClothesState",done)

   # Put
   game.label(game.action("put *"))
   game.label(game.action("put away *"))
   game.cmdPrint("(Try 'PUT ____ IN ____).",done)
   game.label(game.action("put clothes in closet"))
   game.cmdIfPrint("flagClothes",0,"You aren't carrying any clothes.",done)
   game.cmdIfPrint("flagClothesState",0,"You can't put unfolded clothes in the closet.",done)
   game.cmdSet("flagClothesGone")
   game.cmdClr("flagCloses")
   game.cmdPrint("You arrange the clothes in the closet.",done)

   # Sit
   game.label(game.action("sit ?chair"))
   game.label(game.action("sit on chair"))
   game.label(game.action("sit in chair"))
   game.cmdAltPrint("flagSit","You are already sitting in the chair.","You sit on the chair.")
   game.cmdSet("flagSit",done)

   # Stand
   game.label(game.action("stand ?up"))
   game.cmdOr("flagTemp","flagSit","flagSleep")
   game.cmdAltPrint("flagTemp","You stand up.","You are already standing.")
   game.cmdClr("flagSit")
   game.cmdClr("flagSleep",done)

   game.label("autoStand")
   game.cmdIfPrint("flagSit",1,"You get up off the chair.")
   game.cmdIfPrint("flagSleep",1,"You get out of bed.")
   game.cmdClr("flagSit")
   game.cmdClr("flagSleep")
   game.cmdInsert("RETURN")

   # Sleep
   game.label(game.action("sleep"))
   game.label(game.action("sleep in bed"))
   game.label(game.action("get in bed"))
   game.label(game.action("lie down"))
   game.cmdPrint("You get into your bed and try to sleep, but you can't seem to get comfortable.")
   game.cmdClr("flagBed")
   game.cmdSet("flagSleep",done)

   # Get
   game.label(game.action("get"))
   game.cmdPrint("Want do you want to get?",done)

   game.label(game.action("get bed"))
   game.cmdPrint("The bed is too big to pick up.",done)

   game.label(game.action("get desk"))
   game.cmdPrint("The desk is too heavy to move.",done)

   game.label(game.action("get chair"))
   game.cmdPrint("You move the chair around a bit, but decided its fine where it is.",done)

   game.label(game.action("get clothes"))
   game.cmdAltPrint("flagClothes","You are already holding the clothes.","You pick the clothes off the floor.")
   game.cmdSet("flagClothes",done)

   game.label(game.action("get *"))
   game.cmdPrint("You can't get that!",done)

   # Drop
   game.label(game.action("drop"))
   game.cmdPrint("What do you want to drop?",done)

   game.label(game.action("drop clothes"))
   game.cmdAltPrint("flagClothes","You drop the clothes in a disorganized pile on the floor.","You are not holding any dirty clothes.")
   game.cmdClr("flagClothesState")
   game.cmdClr("flagClothes",done)

   game.label(game.action("drop *"))
   game.cmdPrint("You can't drop that!",done)

   # Inventory
   game.label(game.action("inventory"))
   game.cmdClr("flagTemp")
   game.cmdOr("flagTemp","flagClothes","flagClothes")
   game.cmdIfPrint("flagClothes",1,"You are holding some clothes.")
   game.cmdIfPrint("flagTemp",0,"You are not holding anything interesting.",done)

   # Open
   game.label(game.action("open door"))
   game.label(game.action("exit ?room"))
   game.synonym("exit","leave")
   game.cmdGosub("autoStand")
   game.cmdPrint("You crack open the door and peek out into the hallway. Mom says, 'I can hear the door. You can't come out yet.' So you slowly close the door and go back in the room.",done)

   # Quit
   game.synonym("quit","finish")
   game.synonym("quit","end")
   game.label(game.action("quit ?game"))
   game.label(game.action("bye"))
   game.label(game.action("goodbye"))
   game.cmdPrint("Goodbye.")
   game.cmdInsert("END")

   # Generate game
   game.generate()

main()

