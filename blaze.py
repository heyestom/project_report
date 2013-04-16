import sys

class field:
  def __init__(self, colour):
    self.charge = "no charge"
    self.colour = colour
    self.border = "no border"
    self.division = "no division"


#########################################################################################################
#Look up tables for tinctures, furs, linetypes and partitions

tinctures_colours = {"azure":"blue" , "vert":"green", "sable":"black", "purpure":"purple", "gules":"red"}

tinctures_metals = {"or":"gold","argent":"silver"}

furs = {"ermine":"the ermine fur", "ermines":"the ermines fur", "erminois":"the erminois fur", "pean":"the pean fur", "vair":"the vair fur", "counter-vair":"the counter-vair fur","potent":"the potent fur", "counter-potent":"the counter potent fur" }

partition_types = {"fess":"halved horizontally", "pale":"halved vertically", "bend":"split diagonally from upper left to lower right", "bend sinister":"split diagonally from upper right to lower left", "saltire":"quatered diagonally like an x", "cross":"divided into four quarters like a +", "quarterly":"divided into four quarters like a +", "chevron":"divided like a chevron, a ^ shape", "pall":"divided into three parts in a Y shape", "pall reversed":"divided into three parts in an upside down Y shape"}

partition_sizes = {"fess":2, "pale":2, "bend":2 , "bend sinister":2 , "saltire":4, "cross":4, "quarterly":4, "chevron":2, "pall":3, "pall reversed":3}

partition_lines = {"wavy":"in a wavy pattern", "indented":"in a spikey pattern", "invected":"in a bumpy pattern", "sengrailed":"in an inverted bumpy pattern", "nebuly":"in a bloby pattern", "embattled":"in a square pattern", "dovetailed":"in a dovetail shape pattern","potenty":"in a T shaped pattern"}


#########################################################################################################

print "Attempting to parse: \"", sys.argv[1] , "\""

sentance = sys.argv[1]
#lexical analysis
words = sentance.split()


x = 0
for word in words:
  words[x] = word.lower()
  x+=1 

tokens = []
x=0
for word in words:
  if word == "bend":
    if words[x+1] == "sinister":
      tokens.append("bend sinister")
      words.pop(x+1)
    elif partition_lines.has_key(words[x+1]) and words[x+2] == "sinister":
      tokens.append("bend sinister")
      words.pop(x+2)
  elif word =="pall":
    if words[x+1] == "reversed":
      tokens.append("pall reversed")
      words.pop(x+1)
    elif partition_lines.has_key(words[x+1]) and words[x+2] == "reversed":
      tokens.append("pall reversed")
      words.pop(x+2)
    else:
      tokens.append("pall")
  elif word =="sinister" or word =="reversed":
    print "Error, sinister and reversed can only be applied to bend and pall respectivly."
    exit()
  else:
    tokens.append(word)
  x+=1 

print tokens


fields = []

x=0

division = ""

#find the number of colours stated
num_colours = 0
for token in tokens:
  if tinctures_colours.has_key(token):
    num_colours +=1
  elif tinctures_metals.has_key(token) :
    num_colours +=1

if num_colours == 0:
  print "Error, you must provide one tincture or fur at the very least."  
  exit()

number_of_fields = -1;
    
for token in tokens:
  if token == "parted" or token == "party":
    if tokens[x+1] != "per":
      print "Parsing error expecting parted/party \"per\"."
      exit()
  elif token == "per":
    # the next word needs to be a type of partition 
    if (partition_types.has_key(tokens[x+1])):
      division = partition_types[tokens[x+1]]
      #the next word could either be a line type of division or a colour
      if partition_lines.has_key(tokens[x+2]):
        division = division + " " + partition_lines[tokens[x+2]] 
  	tokens.pop(x+2)
      #if the number of colours stated is the same as the number expected all is good! :)
      if num_colours == partition_sizes[tokens[x+1]]:
        #print "Number of sections equals the number of colours declared." 
        tokens.pop(x+1)
      else:
        print "Error number of sections does not equal the number of colours declared."  
        print tokens[x+1] , "creates" , partition_sizes[tokens[x+1]], "sections."
        print "You provided",  num_colours
        exit()

    else:
      print tokens[x+1] , " is not a recognised division" 
      exit()
  elif partition_types.has_key(token):
    print "Error at: " , token
    print "You must state a partition with \"per\" before stating what type."
    exit()
  elif tinctures_colours.has_key(token) :
    fields.append(field(tinctures_colours[token]))
    number_of_fields+=1
  elif tinctures_metals.has_key(token):
    fields.append(field(tinctures_metals[token]))
    number_of_fields+=1
  elif furs.has_key(token):
    fields.append(field(tinctures_metals[token]))
    number_of_fields+=1


  x+=1

    
#print fields

print "\nA shield", division ,"\n" 


print "Field table:"

print '-'*40
for field in fields:
  print "|" , field.colour ,",", field.charge ,",", field.border , "|" 
  print '-'*40
