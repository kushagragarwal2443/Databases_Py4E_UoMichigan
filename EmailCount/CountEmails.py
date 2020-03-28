import sqlite3

datahandle=sqlite3.connect('EmailCount.sqlite')
cur=datahandle.cursor()

cur.execute('DROP TABLE IF EXISTS Counts')
cur.execute("CREATE TABLE COUNTS ( email VARCHAR(128), count INTEGER)")

filename=input("ENTER THE FILE NAME- ")
if(len(filename)<1):
    filename='mbox-short.txt'
filehandle=open(filename)

for line in filehandle:
    if not line.startswith('From '):
        continue
    email=line.split()[1]

    cur.execute('SELECT count FROM Counts WHERE email=?',(email,))
    row=cur.fetchone()

    if row is None:
        cur.execute('INSERT INTO Counts ( email,count) VALUES(?,1)',(email,))
    else:
        cur.execute('UPDATE Counts SET count=count+1 WHERE email=?',(email,))

datahandle.commit()
print("********************DATABASE*********************")
sqlstr="SELECT * FROM Counts"
cur.execute(sqlstr)
for row in cur:
    print(str(row[0]),row[1])

print("**************SORTED DATABASE********************")
sqlanswer="SELECT email,count FROM Counts ORDER BY count DESC"
for row in cur.execute(sqlanswer):
    print(str(row[0]), row[1])

cur.close()
