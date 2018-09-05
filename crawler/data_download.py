import requests
import os
import sys
#select detination folder for data
folder = "id_data"

#Select the name of the target file for data retrieval
target_file = sys.argv[1]
print("Reading from: %s"%(target_file))

#Creates a file in a folder with the id as it's name and writes the data in it
def get_id_data (digit):
    id_file = open("/mnt/archive/asas_aasc/{}.txt".format(digit) , "w+")
    number = digit
    url = "http://www.astrouw.edu.pl/cgi-asas/asas_cgi_get_data?{},asas3".format(number)
    print ("downlaoding: %s"%(digit))
    data = requests.get(url).text
    id_file.write(data)
    id_file.close()

ids = open (target_file , "r")
for line in ids :
    line = str(line).strip("\n")
    if os.path.isfile("/mnt/archive/asas_aasc/{}.txt".format(line)):
        continue
    else:
        get_id_data(line)

ids.close()
