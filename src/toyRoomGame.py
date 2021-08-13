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
   game.cmdPrint("'Mom, it's not fair! She was being mean to me, so why do I have to stay in my room and she can go play with her friends?', you ask.")
   game.cmdPrint()
   game.cmdPrint("Mom says, 'Just think about what you said. There are plenty of things to keep you busy in there while you cool down.'")
   game.cmdPrint()
   game.cmdPrint("[ToyRoom by Paul Wasson, August 2021. Developed with an interactive fiction engine written in Python that generates an AppleSoft basic game.]")
   game.cmdPrint()
   game.cmdPrint("You are in your bedroom. It's messy and you want to leave.",done)

   # Restart
   game.synonym("new","reset")
   game.synonym("new","restart")
   game.label(game.action("new ?game"))
   game.label(game.action("start ?over"))
   game.cmdGoto(game.start)

   # Help
   game.synonym("help","hint")
   game.label(game.action("help"))
   game.cmdPrint("Try using 2 word commands in upper case, like LOOK ROOM or SIT CHAIR. Sometimes you may need a longer sentence like OPEN DOOR WITH KEY or LOOK UNDER BED.")
   game.cmdPrint("Here are some word you can try: LOOK, SIT, STAND, GET, DROP, PUT, INVENTORY, OPEN, QUIT.",done)

   # Look
   game.synonym("look","examine")
   game.label(game.action("look ?room"))
   game.cmdPrint("You look around your bedroom. You see a desk with some homework on it and a chair.")
   game.cmdAltPrint("flagBed","There is a bed that is neatly made.","There is a bed that is unmade with the blanket half off of it.")
   game.cmdOr("flagTemp","flagClothes","flagClothesCloset")
   game.cmdIfPrint("flagTemp",0,"A pile of clothes cover part of the floor.")
   game.cmdIfPrint("flagToys",0,"A lot of toys are piled up in the corner of the room.")
   game.cmdPrint("There is also a toybox and a closet. There is one door but your not sure if you shouldn't leave yet.",done)
   game.cmdIfPrint("flagSit",1,"You are sitting in the chair.")
   game.cmdIfPrint("flagSleep",1,"You are lying in bed.")

   game.label(game.action("look clothes"))
   game.synonym("clothes","laundry")
   game.cmdIfPrint("flagClothesCloset",1,"The clothes are all neatly put away in the closet.",done)
   game.cmdAltPrint("flagClothesState","The clothes are all stacked and neatly folded.",
                                       "It is a random pile of clothes. At least they don't smell too bad.",done)

   game.synonym("bed","blanket")
   game.synonym("bed","pillow")
   game.label(game.action("look bed"))
   game.cmdAltPrint("flagBed","Your bed is very comfortable and is very neat with the pillows arranged nicely.",
      "You know how to make your bed, you just don't like to.",done)
   game.label(game.action("look under bed"))
   game.cmdPrint("You look under the bed and a Grue eats you. Game over!")
   game.cmdInsert('INPUT "Press RETURN to restart game> ";A$')
   game.cmdGoto(game.start)

   game.label(game.action("look door"))
   game.cmdPrint("Mom probably doesn't want you to leave yet.",done)

   game.synonym("chair","seat")
   game.label(game.action("look chair"))
   game.cmdPrint("It is a small desk chair.",done)

   game.label(game.action("look closet"))
   game.cmdAltPrint("flagClothesCloset","The closet is full of neatly stacked and hung up clothes.",
      "The closet looks sort of empty, like there should be more clothes in there.",done)

   game.label(game.action("look desk"))
   game.cmdPrint("It's a small desk with your homework on top.")
   game.cmdAltPrint("flagScrapbook","It seems a little wobbly.","There is something shoved under the desk to keep it from wobbling.",done)

   game.label(game.action("look under desk"))
   game.cmdSet("flagDesk")
   game.cmdAltPrint("flagScrapbook","There is nothing under the desk. The desk seems a little wobbly.","There is a scrapbook that was never started propping up a leg of the desk.",done)

   game.label(game.action("look under *"))
   game.cmdPrint("There is nothing interesting under that.",done)

   game.label(game.action("look homework"))
   game.cmdAltPrint("flagHomework","Your homework is all done. It was some of your best work and you think you will get a good grade.",
      "It's the homework that is due tomorrow that you told your mom you would do right away, but didn't.",done)

   game.label(game.action("look scrapbook"))
   game.label(game.action("read scrapbook"))
   game.cmdAltPrint("flagScrapbook","This is a scrapbook with 3 pages that you were going to finish for your sister, but never started it.",
      "You can't examine the scrapbook when it's holding up the desk.",done)

   game.label(game.action("look page"))
   game.label(game.action("look at page"))
   game.label(game.action("read page"))
   game.label(game.action("read scrapbook page"))
   game.cmdIfPrint("flagScrapbook",0,"You can't read a book you are not holding.",done)
   game.cmdPrint("What page of the scrapbook do you want to read?",done)

   game.synonym("1","one")
   game.label(game.action("look page 1"))
   game.label(game.action("look at page 1"))
   game.label(game.action("read page 1"))
   game.label(game.action("read scrapbook page 1"))
   game.cmdIfPrint("flagScrapbook",0,"It is hard to read a book that you are not holding.",done)
   game.cmdPrint("Page 1 says to draw a picture of your sister.",done)

   game.synonym("2","two")
   game.label(game.action("look page 2"))
   game.label(game.action("look at page 2"))
   game.label(game.action("read page 2"))
   game.label(game.action("read scrapbook page 2"))
   game.cmdIfPrint("flagScrapbook",0,"Page 2 of what? Maybe you should be holding a book.",done)
   game.cmdPrint("Page 2 wants you to write a poem of how your sister make you feel.",done)

   game.synonym("3","three")
   game.label(game.action("look page 3"))
   game.label(game.action("look at page 3"))
   game.label(game.action("read page 3"))
   game.label(game.action("read scrapbook page 3"))
   game.cmdIfPrint("flagScrapbook",0,"Get the scrapbook first.",done)
   game.cmdPrint("Page 3 says to paste a picture you and your sister together.",done)



   game.synonym("me","self")
   game.label(game.action("look me"))
   game.cmdPrint("You are an ordinary kid with an older sister. You are feeling a little calmer, but are still mad. [Try INVENTORY to see what you are carrying.]",done)

   game.label(game.action("look *"))
   game.cmdPrint("I don't see that!",done)

   # Make
   game.label(game.action("make bed"))
   game.label(game.action("make up bed"))
   game.cmdGosub("autoStand")
   game.cmdPrint("You make the bed like Mom taught you.")
   game.cmdSet("flagBed",done)

   # Do
   game.label(game.action("do homework"))
   game.cmdIfPrint("flagSit",0,"You can't do your homework standing up.",done)
   game.cmdAltPrint("flagHomework","It took a while, but it's already done.","You start working on the homework and get into a groove. It takes a while, but you get it all done.")
   game.cmdSet("flagHomework",done)

   game.label(game.action("do"))
   game.label(game.action("do *"))
   game.cmdPrint("Do what?",done)

   # Fold
   game.label(game.action("fold ?clothes"))
   game.cmdGosub("autoStand")
   game.cmdPrint("It takes a bit of time, but you fold up all the laundry.")
   game.cmdSet("flagClothesState",done)

   # Put
   game.label(game.action("put clothes"))
   game.label(game.action("put toys"))
   game.cmdPrint("[Try 'PUT ____ IN ____'.]",done)

   game.label(game.action("put scrapbook"))
   game.cmdPrint("[Try 'PUT ____ UNDER ____'.]",done)

   game.label(game.action("put *"))
   game.cmdPrint("I'm not sure what you are trying to put.",done)

   game.label(game.action("put clothes in closet"))
   game.cmdIfPrint("flagClothes",0,"You aren't carrying any clothes.",done)
   game.cmdIfPrint("flagClothesState",0,"You can't put unfolded clothes in the closet.",done)
   game.cmdSet("flagClothesCloset")
   game.cmdClr("flagClothes")
   game.cmdPrint("You arrange the clothes in the closet.",done)

   # Sit
   game.label(game.action("sit ?chair"))
   game.label(game.action("sit on chair"))
   game.label(game.action("sit in chair"))
   game.cmdAltPrint("flagSit","You are already sitting in the chair.","You sit on the chair.")
   game.cmdSet("flagSit",done)

   # Stand
   game.label(game.action("stand ?up"))
   game.label(game.action("get up"))
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
   game.cmdPrint("You move the chair around a bit, but decided it's fine where it is.",done)

   game.label(game.action("get clothes"))
   game.cmdIfPrint("flagClothesCloset",1,"The clothes are all put away, so you decide to just leave them alone.",done)
   game.cmdAltPrint("flagClothes","You are already holding the clothes.","You pick the clothes off the floor.")
   game.cmdSet("flagClothes",done)

   game.label(game.action("get homework"))
   game.cmdPrint("It's too many books and papers to hold all at once. You decide to just leave it on the desk.",done)

   game.label(game.action("get scrapbook"))
   game.cmdIfPrint("flagDesk",0,"What scrapbook?",done)
   game.cmdAltPrint("flagScrapbook","You got the scrapbook in your hand.","You pull the scrapbook out from under the desk.")
   game.cmdSet("flagScrapbook",done)

   game.label(game.action("get *"))
   game.cmdPrint("You can't get that!",done)

   # Drop
   game.label(game.action("drop"))
   game.cmdPrint("What do you want to drop?",done)

   game.label(game.action("drop clothes"))
   game.cmdAltPrint("flagClothes","You drop the clothes in a disorganized pile on the floor.","You are not holding any dirty clothes.")
   game.cmdClr("flagClothesState")
   game.cmdClr("flagClothes",done)

   game.label(game.action("drop scrapbook"))
   game.label(game.action("put scrapbook under desk"))
   game.cmdAltPrint("flagScrapbook","You shove the scrapbook back under the desk so it won't wobble.","You don't have the scrapbook.")
   game.cmdClr("flagScrapbook",done)

   game.label(game.action("drop *"))
   game.cmdPrint("You can't drop that!",done)

   # Inventory
   game.label(game.action("inventory"))
   game.cmdClr("flagTemp")
   game.cmdOr("flagTemp","flagClothes","flagScrapbook")
   game.cmdIfPrint("flagClothes",1,"You are holding some clothes.")
   game.cmdIfPrint("flagScrapbook",1,"You have the scrapbook that was under your desk.")
   game.cmdIfPrint("flagTemp",0,"You are not holding anything interesting.")
   game.cmdGoto()

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

