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

   def wrapPrint(self,line):
      if (line==""):
         return('?')
      else:
         wrapper = textwrap.TextWrapper(width=self.screenWidth-1)
         return ":".join(['? "{}"'.format(line) for line in wrapper.wrap(text=line)])

   def cmdPrint(self,line="",cont=True):
      self.asLines.append(self.wrapPrint(line))
      self.doCont(cont)  

   def cmdRem(self,lines):
      for line in lines:
         self.asLines.append('REM * {}'.format(line))

   def cmdGoto(self,next=prompt):
      self.asLines.append('GOTO {}'.format(self.labelStr(next)))

   def cmdGosub(self,next):
      self.asLines.append('GOSUB {}'.format(self.labelStr(next)))

   def cmdReturn(self):
      self.asLines.append('RETURN')

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

   def cmdSetVal(self,flag,val=1,cont=True):
      self.checkFlag(flag)
      self.asLines.append('F({})={}'.format(self.labelStr(flag),val))
      self.doCont(cont)

   def cmdSet(self,flag,cont=True):
      self.cmdSetVal(flag,1,cont)

   def cmdClr(self,flag,cont=True):
      self.cmdSetVal(flag,0,cont)

   def cmdExp(self,flag1,flag2,exp,flag3,cont=True):
      self.checkFlag(flag1)
      self.checkFlag(flag2)
      self.checkFlag(flag3)
      self.asLines.append('F({})=F({}) {} F({})'.format(self.labelStr(flag1),self.labelStr(flag2),exp,self.labelStr(flag3)))
      self.doCont(cont)

   def cmdAnd(self,flag1,flag2,flag3,cont=True):
      self.cmdExp(flag1,flag2,"AND",flag3,cont)

   def cmdOr(self,flag1,flag2,flag3,cont=True):
      self.cmdExp(flag1,flag2,"OR",flag3,cont)

   def cmdAltPrint(self,flag,trueLine,falseLine,cont=True):
      self.checkFlag(flag)
      self.asLines.append('IF F({}) THEN {}'.format(self.labelStr(flag),self.wrapPrint(trueLine)))
      self.asLines.append('IF F({})=0 THEN {}'.format(self.labelStr(flag),self.wrapPrint(falseLine)))
      self.doCont(cont)

   def cmdIfPrint(self,flag,value,line,cont=True):
      self.checkFlag(flag)
      self.asLines.append('IF F({})={} THEN {}'.format(self.labelStr(flag),value,self.wrapPrint(line)))
      self.doCont(cont)

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
      self.cmdPrint("Sorry, I don't understand. Please try a different command or type HELP.",False)

      # Start of game
      self.label(self.start)

      # Reset state
      self.cmdInsert("HOME: FOR I=0 to {}: F(I)=0: NEXT".format(self.labelStr(self.flagCount)))
