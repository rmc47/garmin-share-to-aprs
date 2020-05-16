import xml.etree.ElementTree as ET
import requests
import datetime
import aprs
import aprslib
import configparser

config = configparser.ConfigParser()
config.read("garmin-share-to-aprs.ini")

url = "https://share.garmin.com/Feed/Share/" + config['mapshare']['user']
password = config['mapshare']['password']
callsign = config['aprs']['callsign']
passcode = config['aprs']['passcode']

r = requests.get(url, auth=('anything', password))

kmlTree = ET.fromstring(r.text)
ns = {"gis":"http://www.opengis.net/kml/2.2"}
coordinates = kmlTree.findall("./gis:Document/gis:Folder/gis:Placemark[1]/gis:Point/gis:coordinates",ns)[0].text
extendedData = kmlTree.findall("./gis:Document/gis:Folder/gis:Placemark[1]/gis:ExtendedData",ns)[0]

velocity = float(extendedData.findall("./gis:Data[@name='Velocity']/gis:value",ns)[0].text[:-4])
course = float(extendedData.findall("./gis:Data[@name='Course']/gis:value",ns)[0].text[:-7])
latitude = float(extendedData.findall("./gis:Data[@name='Latitude']/gis:value",ns)[0].text)
longitude = float(extendedData.findall("./gis:Data[@name='Longitude']/gis:value",ns)[0].text)
altitude = float(extendedData.findall("./gis:Data[@name='Elevation']/gis:value",ns)[0].text.split()[0])
position_time = datetime.datetime.strptime(extendedData.findall("./gis:Data[@name='Time UTC']/gis:value",ns)[0].text, "%m/%d/%Y %I:%M:%S %p").replace(tzinfo=datetime.timezone.utc)

print (latitude)
print (longitude)
print (altitude)
print (velocity)
print (course)
print (position_time)

position_age = datetime.datetime.now(datetime.timezone.utc) - position_time
print ("Age: {}s".format(position_age.total_seconds() ))

if (position_age.total_seconds() < 120):
        frame = aprs.PositionFrame(lat=latitude,lng=longitude,source=bytearray(callsign),destination=b"APRS,TCPIP*",path="",table=b'/',symbol=b'(',comment=b"via Iridium",ambiguity=0)
        frameText = frame.__repr__()

        ais = aprslib.IS(callsign, passwd=passcode)
        ais.connect()
        ais.sendall(frameText)

        print (frameText)
else:
        print ("Packet older than threshold")
