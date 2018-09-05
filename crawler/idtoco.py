cra=str(raw_input("start coordinate for right ascension"))
cd=str(raw_input("start coordinate dor declination"))
dra=str(raw_input("end coordinate for right ascension"))
dd=str(raw_input("end coordinate for declination (top-down)"))

if (len(dra)=!6 or len(cra)=!6):
	dra=str(raw_input("right ascension must have 6 characters"))
if (len (dd)=!5 or len(cd)=!5):
	dd=str(raw_input("declianation must have +/- and 4characters"))

dra=(int(dra[0:2]),int(dra[2:4]),int(dra[4:6]))
dd=(int(dd[0:3]),int(dd[3:5]))

cra=(int(cra[0:2]),int(cra[2:4]),int(cra[4:6]))
cd=(int(cd[0:3)],int(cd[3:5]))

id_list=[]

ids=open("final_2.txt","r")
for l in ids:
	l.strip("\n")
	lra=l[0:5]
	ld=[6:10]
	if (lra>=cra and lra<=dra):
		if( ld<=cd and ld>=dd ):
			id_list.append(l)
ids.close()
	
skypatch=open("newskypatch.txt","w+")
for item in id_list:
	skypatch.write(item+"\n")
close(skypatch)		

