import requests
from bs4 import BeautifulSoup

def ask_for_ids():
    final_ids = set()
    for dec in range(-6*60*60,6*60*60,100):
        print("%d%%"%(100*(dec/(12*60*60)+0.5)))
        for ra in range(0,24*60*60,100):
            # RA segs
            ra_segs = ra
            ra1 = ra_segs//3600
            ra2 = (ra_segs//60)%60
            ra3 = ra_segs%60
            # DEC arcsegs
            dec_asecs = dec*360//24
            dec1 = dec_asecs//3600
            dec2 = (dec_asecs//60)%60
            dec3 = dec_asecs%60
            # Parameters
            pars = {
                'source':'asas3',
                'coo':'%d:%d:%d,%d:%d:%d'%(ra1,ra2,ra3,dec1,dec2,dec3),
                'equinox':'2000',
                'nmin':'1',
                'box':'3500',
                'submit':'Search',
            }
            r = requests.get('http://www.astrouw.edu.pl/cgi-asas/asas_cat_input',params=pars)
            soup = BeautifulSoup(r.text,'html.parser')
            print(soup.prettify())
            routes = [x.get('href') for x in soup.pre.pre.find_all('a')]
            ids = [x.split("/")[3].split(",")[0] for x in routes]
            final_ids.update(ids)
    return final_ids

if __name__=='__main__':
    #ids = ask_for_ids()
    ids = ["hello","how","are","you"]
    ids = sorted(list(ids))
    fil = open("ids.txt","w")
    for id in ids:
        fil.write(id+"\n")
    fil.close()

# curl 'http://www.astrouw.edu.pl/cgi-asas/asas_cat_input' -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0' -H 'Origin: http://www.astrouw.edu.pl' -H 'Upgrade-Insecure-Requests: 1' -H 'Content-Type: application/x-www-form-urlencoded' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'DNT: 1' -H 'Referer: http://www.astrouw.edu.pl/asas/i_aasc/aasc_form.php?catcrawlsrc=asas3' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: en-US,en;q=0.9,es;q=0.8' -H 'Cookie: 14cdf11341b0ef7b9fea6ea35afc243c=mn4h9crgqgshectt4dh33pifi7; asaswww=it7qqc0l919lpdor1h67boukn0' --data 'source=asas3&coo=5%3A26%3A50%2C-81%3A35%3A12&equinox=2000&nmin=4&box=15&submit=Search' --compressed
