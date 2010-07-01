import os
from optparse import OptionParser
import ConfigParser


parser = OptionParser()
(options, args) = parser.parse_args()

path = str(args[1]) + "\sql"
path = path.replace('\\', '/')

updatelist = []

for elem in os.listdir(path):
    if elem.startswith('update_einsteinDB_'):
        updatelist.append(elem)


#filenum = 1
#while os.path.isfile(str(args[1]) + "\sql\\" +"update_einsteinDB_"+"0"*(3-len(str(filenum)))+str(filenum)+".txt"):
#    filenum+=1
#filenum-=1

fobj = open( str(args[2])+"\\update.bat", "w")

for elem in updatelist:
    fobj.write("\""+str(args[0]) +"\""+ " --user=" + str(args[3])+" --password="+ str(args[4]) +"< "+ "\""+ str(args[1]) + "\sql\\" +
               elem+"\"" + "\n" )#+ "pause" + "\n") 

fobj.close()

config = ConfigParser.RawConfigParser()
config.read(str(args[1])+'\GUI\einstein.ini')

#Set needed Configurations

config.set('DB','DBuser',str(args[3]))
config.set('DB','DBpass',str(args[4]))
config.set('DB','mysqlbin',str(args[0]))


iniFile = open(str(args[1])+'\GUI\einstein.ini','wb')

iniFile.write('[GUI]\n')
items = config.items('GUI')

for i in items:
    iniFile.writelines(str(i[0])+ ':'+str(i[1])+"\n")

iniFile.write('\n[DB]\n')
items = config.items('DB')
for j in items:
    iniFile.writelines(str(j[0])+ ':'+str(j[1])+"\n")

iniFile.close()
    
