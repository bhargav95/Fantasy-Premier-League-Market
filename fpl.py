import urllib
import re
import MySQLdb
from prettytable import PrettyTable


def statname(argument):
    switcher = {
        0: "id",
        1: "name",
        2: "club",
		3: "pos",
		4: "status",
		5: "selby",
		6: "price",
		7: "chgs",
		8: "unlocks",
		9: "delta"
    }
    return switcher.get(argument, "nothing")

site="http://www.fplstatistics.co.uk/Home/IndexWG?gridPriceData_inside="
#site="http://www.fplstatistics.co.uk/Home/IndexWG?gridPriceData_sort=unlockdt&gridPriceData_sortdir=DESC&gridPriceData_inside="
regex='<td class="text-align-center">(.*?)</td>'
regextarget='<div style=(?:"border: 1px solid blue; text-align: center">|"text-align: center">)(.+?)</div>'

pattern=re.compile(regex)
patterntarget=re.compile(regextarget)
#ppattern = re.compile(r'\&#163;(.*?)\m')
ppattern = re.compile(r'\$(.*?)\m')
stats={}
statlist=[]
targets=[]
x=0
pg=40

for i in range(1,pg):
	progess=((i+1)*100)/pg
	print "\b\b\b\b"+str(progess) + "%",
	url=site+""+str(i)
	html=urllib.urlopen(url)
	htmltext=html.read()
	titles=re.findall(pattern,htmltext)
	targets1=re.findall(patterntarget,htmltext)
	
	for items in targets1:
		targets.append(items)
	
	
	"""print titles"""
	y=0
	for j in titles:	
		stats[statname(y%10)]=j
		y+=1
		if y%10==0:
			stats['price']=re.sub(ppattern,r'\1',stats['price'])
			#print stats['price']
			#print stats
			stats['name']=stats['name'].replace("&#224;","a")
			stats['name']=stats['name'].replace("&#225;","a")
			stats['name']=stats['name'].replace("&#252;","u")
			stats['name']=stats['name'].replace("&#233;","e")
			stats['name']=stats['name'].replace("&#250;","u")
			stats['name']=stats['name'].replace("&#232;","e")
			stats['name']=stats['name'].replace("&#214;","O")
			stats['name']=stats['name'].replace("&#237;","i")
			stats['name']=stats['name'].replace("&#243;","o")
			stats['name']=stats['name'].replace("&#246;","o")
			stats['name']=stats['name'].replace("&#39;","\'")
			stats['target']=targets[x]
			if stats['delta']=="":
				stats['delta']="0"
			x+=1
			statlist.append(stats)
			stats={}

#for key in statlist:
	#print key

pt=PrettyTable(["ID","Name","Club","Price"])
pt.align["Name"]="l"
pt.align["Club"]="l"
pt.align["Price"]="r"
for i in statlist:
	pt.add_row([i['id'],i['name'],i['club'],i['price']])
"""print pt"""



# Open database connection
db = MySQLdb.Connect(host="127.0.0.1",port=3306,user="root",db='test')

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Drop table if it already exist using execute() method.
cursor.execute("DROP TABLE IF EXISTS FPLSTATS")

# Create table as per requirement
sql = """CREATE TABLE FPLSTATS (
         id  INTEGER(3) PRIMARY KEY,
         name  VARCHAR(20),
         club VARCHAR(25),  
         pos VARCHAR(1),
         status VARCHAR(1),
		 selby INTEGER(7),
		 price DECIMAL(5,1),
		 chgs INTEGER(2),
		 unlocks VARCHAR(30),
		 delta INTEGER(7),
		 target DECIMAL(5,1))""" # remember to add another double quote later (totally 3)

cursor.execute(sql)

for key in statlist:
	cursor.execute("""INSERT INTO FPLSTATS (id,name,club,pos,status,selby,price,chgs,unlocks,delta,target)
	values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
	(int(key['id']),key['name'],key['club'],key['pos'],key['status'],int(key['selby']),float(key['price']),int(key['chgs']),key['unlocks'],int(float(key['delta'])),float(key['target'])))

db.commit()
# disconnect from server
db.close()
