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
      "http://https://github.com/pmwasson/one-room-game",
      ""
      ])

   # Start of game
   game.cmdPrint("'Mom, its not fair! She was being mean to me, so why do I have to stay in my room and she can go play with her friends?'")
   game.cmdPrint()
   game.cmdPrint("'Just think about what you said. There are plenty of things to keep you busy in there while you cool down.'")
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
   game.cmdPrint("Here are some word you can try: LOOK, SIT, STAND, GET, DROP, INVENTORY, OPEN, QUIT.",done)

   # Look
   game.synonym("look","examine")
   game.label(game.action("look ?room"))
   game.cmdPrint("The room is messy with an unmade bed and piles of clothes on the floor. There is also a toybox, a dresser, a closet, and a desk with a chair. There is one door but you shouldn't leave yet.",done)

   game.label(game.action("look clothes"))
   game.cmdPrint("Just a bunch of dirty clothes. At least they don't smell too bad.",done)

   game.label(game.action("look door"))
   game.cmdPrint("Mom probably doesn't want you to leave yet.",done)

   game.synonym("chair","seat")
   game.label(game.action("look chair"))
   game.cmdPrint("It is a small desk chair.",done)

   game.synonym("me","self")
   game.label(game.action("look me"))
   game.cmdPrint("You are feeling a little calmer, but are still mad. (Try INVENTORY to see what you are carrying.)",done)

   game.label(game.action("look *"))
   game.label("noLook")
   game.cmdPrint("I don't see that!",done)

   # Sit
   game.label(game.action("sit ?chair"))
   game.label(game.action("sit on chair"))
   game.label(game.action("sit in chair"))
   game.cmdAltPrint("flagSit","You are already sitting in the chair.","You sit on the chair.")
   game.cmdSet("flagSit",done)

   # Stand
   game.label(game.action("stand ?up"))
   game.cmdAltPrint("flagSit","You stand up.","You are already standing.")
   game.cmdClr("flagSit",done)

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
   game.cmdAltPrint("flagClothes","You are already holding some of the dirty clothes.","You pick up some of the dirty clothes off the floor, but there are more.")
   game.cmdSet("flagClothes",done)

   game.label(game.action("get *"))
   game.cmdPrint("You can't get that!",done)

   # Drop
   game.label(game.action("drop"))
   game.cmdPrint("What do you want to drop?",done)

   game.label(game.action("drop clothes"))
   game.cmdAltPrint("flagClothes","You drop the dirty clothes on the floor.","You are not holding any dirty clothes.")
   game.cmdClr("flagClothes",done)

   game.label(game.action("drop *"))
   game.cmdPrint("You can't drop that!",done)

   # Inventory
   game.label(game.action("inventory"))
   game.cmdAltPrint("flagClothes","You are holding some dirty clothes.","You are not carrying anything interesting.",done)

   # Open
   game.label(game.action("open door"))
   game.cmdPrint("You crack open the door and peek out into the hallway. Mom says 'I can hear the door. You can't come out yet.' So you slowly close the door and go back in the room.",done)

   # Quit
   game.synonym("quit","finish")
   game.synonym("quit","end")
   game.label(game.action("quit ?game"))
   game.cmdPrint("Goodbye.")
   game.cmdInsert("END")

   # Generate game
   game.generate()

main()

