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
   game.cmdPrint("Here are some words you can try: LOOK, SIT, STAND, GET, DROP, PUT, INVENTORY, OPEN, QUIT.",done)

   # Look
   game.synonym("look","examine")
   game.label(game.action("look ?room"))
   game.cmdPrint("You look around your bedroom. You see a desk with some homework on it and a chair.")
   game.cmdAltPrint("flagWindow","There is an open window which lets in a slight breeze.","There is a closed window on the wall opposite the door.")
   game.cmdAltPrint("flagBed","There is a bed that is neatly made.","There is a bed that is unmade with the blanket half off of it.")
   game.cmdOr("flagTemp","flagClothes","flagClothesCloset")
   game.cmdIfPrint("flagTemp",0,"A pile of clothes cover part of the floor.")
   game.cmdOr("flagTemp","flagToys","flagToybox")
   game.cmdIfPrint("flagTemp",0,"A lot of toys are piled up in the corner of the room.")
   game.cmdPrint("There is also a toybox and a closet. There is one door but you're not sure if you should leave yet.",done)
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
   game.cmdPrint()
   game.cmdPrint("[You got the Zork ending! But there are other ways to finish the game.]")
   game.cmdPrint()
   game.cmdGoto("quit")

   game.label(game.action("look door"))
   game.cmdPrint("Mom probably doesn't want you to leave yet.",done)

   game.synonym("chair","seat")
   game.label(game.action("look chair"))
   game.cmdPrint("It is a small desk chair.",done)

   game.label(game.action("look closet"))
   game.label(game.action("look in closet"))
   game.cmdAltPrint("flagClothesCloset","The closet is full of neatly stacked and hung up clothes.",
      "The closet looks sort of empty, like there should be more clothes in there.",done)

   game.label(game.action("look toybox"))
   game.cmdAltPrint("flagToybox","The toybox is almost overflowing it has so many toys in it.",
      "The toybox is mostly empty.",done)

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
   game.cmdAltPrint("flagScrapbook","This is a scrapbook with 3 pages that you were going to finish for your sister, but never started.",
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
   game.cmdAltPrint("flagPage1","Page 1 has a picture you drew of you and your sister.","Page 1 says to draw a picture of your sister.",done)

   game.label(game.action("draw ?picture"))
   game.label(game.action("draw sister"))
   game.label(game.action("draw picture of sister"))
   game.cmdIfPrint("flagSit",0,"You can't draw a picture standing up.",done)
   game.cmdIfPrint("flagScrapbook",0,"You think about drawing a picture of your sister, but can't find any paper.",done)
   game.cmdIfPrint("flagPage1",1,"You want to redo a picture of your sister so you paste a blank page over the previous drawing.")
   game.cmdPrint("You draw a nice picture of you and your sister on page 1 of the scrapbook.")
   game.cmdSet("flagPage1",done)

   game.synonym("2","two")
   game.label(game.action("look page 2"))
   game.label(game.action("look at page 2"))
   game.label(game.action("read page 2"))
   game.label(game.action("read scrapbook page 2"))
   game.cmdIfPrint("flagScrapbook",0,"Page 2 of what? Maybe you should be holding a book.",done)
   game.cmdAltPrint("flagPage2","Page 2 has a poem you wrote about your sister. It seems a little corny, but maybe she will like it.",
      "Page 2 instructs you to write a poem of how your sister makes you feel.",done)

   game.label(game.action("write ?poem"))
   game.cmdIfPrint("flagSit",0,"You can't write a poem standing up.",done)
   game.cmdIfPrint("flagScrapbook",0,"You feel like writing something, but don't have any paper.",done)
   game.cmdIfPrint("flagPage2",1,"You come up with a new idea and erase the previous poem.")
   game.cmdPrint("You don't feel like a good writer, but you make up a nice poem for your sister on page 2 of the scrapbook.")
   game.cmdSet("flagPage2",done)

   game.synonym("3","three")
   game.label(game.action("look page 3"))
   game.label(game.action("look at page 3"))
   game.label(game.action("read page 3"))
   game.label(game.action("read scrapbook page 3"))
   game.cmdIfPrint("flagScrapbook",0,"Get the scrapbook first.",done)
   game.cmdAltPrint("flagPage3","Page 3 has the picture you found of you and your sister laughing.",
      "Page 3 says to paste a photo of you and your sister together.",done)

   game.label(game.action("paste ?photo"))
   game.cmdIfPrint("flagScrapbook",0,"Not sure where you would paste a photo.",done)
   game.cmdIfPrint("flagSit",0,"You can't paste a photo standing up.",done)
   game.cmdIfPrint("flagPage3",1,"You decide you don't like the photo you found and take it out.")
   game.cmdPrint("You dig through your desk drawer and find a good photo of you and your sister. You paste it onto page 3 of the scrapbook.")
   game.cmdSet("flagPage3",done)

   game.label(game.action("look photo"))
   game.cmdAltPrint("flagPage3","The photo shows shows you and your sister on a family vacation, laughing.","There are some photos in your desk.",done)

   game.label(game.action("get photo"))
   game.cmdPrint("You decide to leave the photos in your desk.",done)

   game.synonym("toys","toy")
   game.label(game.action("look toys"))
   game.cmdPrint("There are many toys of superheroes in various poses and some cars.",done)

   game.label(game.action("look window"))
   game.label(game.action("look out window"))
   game.cmdAltPrint("flagScrapbook","You lean out of the open window and see the ground below you.",
      "You look out the closed window and see your backyard.",done)

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
   game.cmdPrint("It takes a bit of time, but you fold all the laundry.")
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

   game.label(game.action("put clothes in *"))
   game.cmdPrint("Clothes don't go in there.",done)

   game.label(game.action("put toys in toybox"))
   game.cmdIfPrint("flagToys",0,"You aren't holding any toys.",done)
   game.cmdSet("flagToybox")
   game.cmdClr("flagToys")
   game.cmdPrint("You put all the toys in the toybox.",done)

   game.label(game.action("put toys in *"))
   game.cmdPrint("Toys don't go in there.",done)

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
   game.cmdPrint("You get into your bed and try to sleep, but you are not tired.")
   game.cmdClr("flagBed")
   game.cmdSet("flagSleep",done)

   # Play
   game.label(game.action("play"))
   game.label(game.action("play toys"))
   game.label(game.action("play with toys"))
   game.cmdClr("flagToys")
   game.cmdClr("flagToybox")
   game.cmdPrint("You arrange the toys in the corner of the room and play with them for a while. Pow! Zaroooom!",done)

   game.label(game.action("play *"))
   game.cmdPrint("Play with what?",done)

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
   game.cmdAltPrint("flagClothes","You are already holding the clothes.","You pick the clothes up off the floor.")
   game.cmdSet("flagClothes",done)

   game.label(game.action("get toys"))
   game.cmdAltPrint("flagToys","You already are holding the toys.","You grab the toys.")
   game.cmdClr("flagToybox")
   game.cmdSet("flagToys",done)

   game.label(game.action("get homework"))
   game.cmdPrint("It's too many books and papers to hold all at once. You decide to just leave it on the desk.",done)

   game.label(game.action("get scrapbook"))
   game.cmdIfPrint("flagDesk",0,"What scrapbook?",done)
   game.cmdAltPrint("flagScrapbook","You have the scrapbook in your hand.","You pull the scrapbook out from under the desk.")
   game.cmdSet("flagScrapbook",done)

   game.label(game.action("get window"))
   game.cmdPrint("You can't get a window, but you might be able to open or close it.",done)

   game.label(game.action("get *"))
   game.cmdPrint("You can't get that!",done)

   # Drop
   game.label(game.action("drop"))
   game.cmdPrint("What do you want to drop?",done)

   game.label(game.action("drop clothes"))
   game.cmdAltPrint("flagClothes","You drop the clothes in a disorganized pile on the floor.","You are not holding any clothes.")
   game.cmdClr("flagClothesState")
   game.cmdClr("flagClothes",done)

   game.label(game.action("drop scrapbook"))
   game.label(game.action("put scrapbook under desk"))
   game.cmdAltPrint("flagScrapbook","You shove the scrapbook back under the desk so it won't wobble.","You don't have the scrapbook.")
   game.cmdClr("flagScrapbook",done)

   game.label(game.action("drop toys"))
   game.cmdAltPrint("flagToys","You drop the toys in the corner of the room.","You are not holding the toys.")
   game.cmdClr("flagToys",done)

   game.label(game.action("drop *"))
   game.cmdPrint("You can't drop that!",done)

   # Inventory
   game.label(game.action("inventory"))
   game.cmdOr("flagTemp","flagClothes","flagScrapbook")
   game.cmdOr("flagTemp","flagTemp","flagToys")
   game.cmdIfPrint("flagClothes",1,"You are holding some clothes.")
   game.cmdIfPrint("flagScrapbook",1,"You have the scrapbook that was under your desk.")
   game.cmdIfPrint("flagToys",1,"You are holding the toys that were on the floor.")
   game.cmdIfPrint("flagTemp",0,"You are not holding anything interesting.")
   game.cmdGoto()

   # Close
   game.label(game.action("close window"))
   game.cmdAltPrint("flagWindow","You slam the window shut.",
                                 "The window is already closed.")
   game.cmdClr("flagWindow",done)

   # Open
   game.label(game.action("open closet"))
   game.cmdPrint("It is one of those closets that is always sort of opened.",done)


   game.label(game.action("open door"))
   game.label(game.action("exit ?room"))
   game.synonym("exit","leave")
   game.cmdGosub("autoStand")
   game.cmdPrint("You crack open the door and peek out into the hallway.")
   game.cmdAnd("flagTemp","flagBed","flagHomework")
   game.cmdAnd("flagTemp","flagTemp","flagClothesCloset")
   game.cmdAnd("flagTemp","flagTemp","flagToybox")
   game.cmdIfSetGoto("flagTemp","gameWin1")

   game.cmdAnd("flagTemp","flagScrapbook","flagPage1")
   game.cmdAnd("flagTemp","flagTemp","flagPage2")
   game.cmdAnd("flagTemp","flagTemp","flagPage3")
   game.cmdIfSetGoto("flagTemp","gameWin2")

   game.cmdPrint("Mom says, 'I can hear the door. You can't come out yet.' You slowly close the door and go back in the room.",done)

   game.label(game.action("open window"))
   game.cmdGosub("autoStand")
   game.cmdAltPrint("flagWindow","The window is already opened.",
                                 "It sticks a little, but you are able to open the window.")
   game.cmdSet("flagWindow",done)

   game.label(game.action("open"))
   game.cmdPrint("What do you want to open?",done)

   game.label(game.action("open *"))
   game.cmdPrint("Don't know how to open that.",done)


   # Good-boy ending
   game.label("gameWin1")
   game.cmdPrint("Mom looks around the room and starts to smile. 'Bed made, homework done, everything put away! Come here and give me a hug. You walk out of the room feeling proud.")
   game.cmdPrint()
   game.cmdPrint("[You got the good-boy ending! But there are other ways to finish the game.]")
   game.cmdPrint()
   game.cmdGoto("quit")

   # Forgiveness ending
   game.label("gameWin2")
   game.cmdPrint("Your sister is standing outside of your room. You say, 'I'm sorry' and hand her the scrapbook.")
   game.cmdPrint("She looks at it and spends a long time looking at the picture of the both of you laughing. She says, 'Oh, I can't stay mad at you, come here!', and gives you a big hug.")
   game.cmdPrint()
   game.cmdPrint("[You got the forgiveness ending! But there are other ways to finish the game.]")
   game.cmdPrint()
   game.cmdGoto("quit")

   # Hobo ending
   game.label(game.action("exit window"))
   game.label(game.action("climb window"))
   game.label(game.action("climb out window"))
   game.cmdGosub("autoStand")
   game.cmdIfPrint("flagWindow",0,"You can't exit through a closed window.",done)
   game.cmdPrint("You climb out the window and jump down to the grass below. You climb over the back fence and head out. Glancing back once over your shoulder you vow to never return to a home that treated you so unfairly.")
   game.cmdPrint()
   game.cmdPrint("[You got the hobo ending! But there are other ways to finish the game.]")
   game.cmdPrint()
   game.cmdGoto("quit")

   # Quit
   game.synonym("quit","finish")
   game.synonym("quit","end")
   game.label(game.action("quit ?game"))

   game.label("quit")
   game.cmdPrint("Thanks for playing. Type RUN to play again. Goodbye.")
   game.cmdInsert("END")

   # Generate game
   game.generate()

main()

