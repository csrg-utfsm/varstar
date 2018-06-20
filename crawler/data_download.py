import requests

#Creates a file in a folder with the id as it's name and writes the data in it
def get_id_data (digit):
    id_file = open("./id_data/{}.txt".format(digit) , "w+")
    number = digit
    url = "http://www.astrouw.edu.pl/cgi-asas/asas_cgi_get_data?{},asas3".format(number)
    data = requests.get(url).text
    id_file.write(data)
    id_file.close()

#Select the name of the target file for data retrieval
target_file = "example.txt"

ids = open (target_file , "r")
for line in ids :
    line = str(line).strip("\n")
    get_id_data(line)

ids.close()
