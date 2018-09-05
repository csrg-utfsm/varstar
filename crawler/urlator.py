ids = open("newskypatch.txt","r" )
urls = open("skypatchdata.txt","w+")
for l in ids:
	line = l.strip("\n")
	urls.write("http://www.astrouw.edu.pl/cgi-asas/asas_cgi_get_data?{},asas3\n".format(line))
	
ids.close()
urls.close()
