from random import randrange

stream = ""



for i in range(2,10):
 streamlen = 10**i
 for _ in range(streamlen):
  char = randrange(0, 27)
  if (char == 26):
   stream+=" "
  else:
   stream+=chr(ord('a')+char)
	

 words = stream.split()

 lens = [len(x) for x in words]

 print(f"Stream len: {streamlen}, avg word length {sum(lens) / len(lens)}")


