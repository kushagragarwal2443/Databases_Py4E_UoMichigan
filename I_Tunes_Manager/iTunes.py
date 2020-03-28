import sqlite3
import xml.etree.ElementTree as ET

datahandle=sqlite3.connect('iTunesDB.sqlite')
cur=datahandle.cursor()

#the following lines of code are SQL that removes existing tables and creates one with our specifications
cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;

CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY
        AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);
''')

#enter xml file to be parsed
fname="Library.xml"
parsedtext=ET.parse(fname)
dicti=parsedtext.findall('dict/dict/dict')
print("Number of Songs in the iTunes playlist is:",len(dicti))

#writing a function lookup to associate keys with their corresponding values

# <key>Track ID</key><integer>369</integer>
# <key>Name</key><string>Another One Bites The Dust</string>
# <key>Artist</key><string>Queen</string>
# so once we match key we need to extract text of succedding tag
def lookup(d, key):
    found=False
    for child in d:
        if found:
            return child.text
        if child.tag=='key' and child.text==key:
            found=True
    return None


#Now we will loop through the parsed xml and create entries into our tables
for entry in dicti:
    name=lookup(entry,'Name')
    artist=lookup(entry,'Artist')
    album=lookup(entry,'Album')
    length=lookup(entry,'Total Time')
    count=lookup(entry,'Play Count')
    rating=lookup(entry,'Rating')

    if name is None or album is None or artist is None:
        continue

    cur.execute('INSERT OR IGNORE INTO Artist(name) VALUES(?)',(artist,))
    cur.execute('SELECT id FROM Artist WHERE name=?',(artist,))
    artist_id=cur.fetchone()[0]

    cur.execute('INSERT OR IGNORE INTO Album(title, artist_id) VALUES (?,?)',(album,artist_id))
    cur.execute('SELECT id FROM Album WHERE title=?',(album,))
    album_id=cur.fetchone()[0]

    cur.execute('INSERT OR REPLACE INTO Track(title,album_id,len,rating,count) VALUES (?,?,?,?,?)',(name,album_id,length,rating,count))

cur.execute('SELECT Artist.name, Album.title, Track.title, Track.len, Track.count, Track.rating FROM Artist JOIN Album JOIN Track ON Artist.id=Album.artist_id AND Album.id=Track.album_id')
for row in cur:
    print(row[0],row[1],row[2],row[3],row[4],row[5])

datahandle.commit()
