#Sets starting and finishing coordinates for id extraction
cra=str(input("start coordinate for right ascension"))
cd=str(input("start coordinate for declination(right-to-left)"))
dra=str(input("end coordinate for right ascension"))
dd=str(input("end coordinate for declination (top-down)"))

if (len(dra)!=6 or len(cra)!=6):
	print("right ascension must have 6 characters")
	cra=str(input("start coordinate for right ascension"))
	dra=str(input("end coordinate for right ascension"))
if (len (dd)!=5 or len(cd)!=5):
	print("declination mus have +/- followed by 4 characers")
	dra=str(input("starting coordinate for declination"))
	dd=str(input("ending coordinate fordecliantion"))
	

dra=(int(dra[0:2]),int(dra[2:4]),int(dra[4:6]))
dd=(int(dd[0:3]),int(dd[3:5]))

cra=(int(cra[0:2]),int(cra[2:4]),int(cra[4:6]))
cd=(int(cd[0:3]),int(cd[3:5]))

#makes a new file "newslypatch.txt" with all the ids inside the selected region
id_list=[]

ids=open("final_2.txt","r")
for l in ids:
	l.strip("\n")
	lra=(int(l[0:2]),int(l[2:4]),int(l[4:6]))
	ld=(int(l[0:3]),int(l[3:5]))
	if (lra>=cra and lra<=dra):
		if( ld<=cd and ld>=dd ):
			print(l)
			id_list.append(l)
ids.close()

print("now writing file")
	
skypatch=open("newskypatch.txt","w+")
for item in id_list:
	skypatch.write(item+"\n")
skypatch.close()	

