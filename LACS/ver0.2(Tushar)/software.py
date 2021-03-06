import MySQLdb
import time
import csv
import subprocess


def auth(uid):
    status = 0
    name = ""
    if len(uid)>=4:
        #Connecting to MySQLdb with user=root,pass=raspberry,database=local.
        r_db = MySQLdb.connect("localhost","root","raspberry","local")
        #Declaring cursor to execute query on SQL server.
        r_cursor = r_db.cursor()
        #Convering UID to key
        key = ''.join(str(x) for x in uid)
        #Query to be run
        query = "SELECT * FROM auth WHERE uid='%s'" % key        
        try:
            r_cursor.execute(query)
            data = r_cursor.rowcount
            status = int(data)
            #fetching flag after query
            if status == 0:
                #CASE-Not authenticated
                print "User not allowed.Please contact admin for registeration"
                #opening CSV file
                fileName="logs/auth.csv"
                fh = open(fileName,'aw')
                #Setting delimiter as space and declaring csv 
                writer=csv.writer(fh,delimiter=" ")
                line=[]
                #Adding uid to log
                line.append(''.join(key))
                line.append("Unauth")
                name="unauth"
                line.append("Unauth")
                #Adding timestamp to log
                time=subprocess.check_output("date +%s",shell=True).strip('\n')
                line.append(time)
                print line
                #Writing into csv logs
                writer.writerow(line)
                fh.close()

            elif status == 1:
                #CASE-authenticated
                fileName = "logs/auth.csv"
                #opening CSV file
                fh = open(fileName,'aw')
                #Setting delimiter as space and declaring csv 
                writer=csv.writer(fh,delimiter=" ")
                #Fetching NAME of person from database
                line=list(r_cursor.fetchone())[1:]
                #Appending to Log
                name=str(line[2])
                #Adding timestamp to log             
                time=subprocess.check_output("date +%s",shell=True).strip("\n")
                line.append(time)
                print line
                #Writing into csv file
                writer.writerow(line)
                fh.close()
        except:
            print "Error: Unable to Fetch Data From Local"
    return (status,name)



