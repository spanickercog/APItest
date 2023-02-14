import paho.mqtt.client as mqtt
import ssl
import json
import requests
import time

#global t, section, prevsec, prevt
t = None
section = None
prevsec = None
prevt = 0
url = "https://cog-ams-control.pxsuite.app/api/public/1a8e44c8-3213-4287-8c70-289c40e20493/presentations/trigger-event"

headers = {
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2NzIzMTk0MjEsImlzcyI6ImNvZy1hbXMiLCJleHAiOjE2ODIzNDgyMjF9.3Mz2fACFHwFP4G5Z0_1lzz8CzxuVfaBqnlcjmNeplpE',
  'Content-Type': 'application/json'
}

host = "mqtt.cloud.pozyxlabs.com"
port = 443
topic = "63760b33be56a1d2bbb173ca"  # your mqtt topic
username = "63760b33be56a1d2bbb173ca"  # your mqtt username
password = "267ff0e8-2b7a-4bef-9bbf-78a9ba763638"  # your generated api key

def on_connect(client, userdata, flags, rc):
    print(mqtt.connack_string(rc))
    
# Callback triggered by a new Pozyx data packet
def on_message(client, userdata, msg):
    #print("Positioning update:", msg.payload.decode())
    pass_to_func_and_pub(msg.payload)

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed to topic!")

def pass_to_func_and_pub(data_to_pub):
    #print("Raw data: ", data_to_pub)
    
    global t, section, prevsec, prevt
    try:
        pos = None
        pos = json.loads(data_to_pub)
    except Exception as e:
        print("Couldn't parse raw data: %s" % data_to_pub, e)
    else:
        x = None
        
        for i in range(1,len(pos)):   
            #print(pos[i]['tagId'])
            if(pos[i]['tagId'] == '26495'):
                x = i
        if (x != None):
            #print("here")
            try:
                if(int(pos[i]['data']['coordinates']['x']) < 1155 and int(pos[i]['data']['coordinates']['x']) > -100 ):
                    if(int(pos[i]['data']['coordinates']['y']) < 4085):
                        print("Section 1")
                        section = 1
                        t = time.time()
                if(pos[i]['data']['coordinates']['x'] < 2655 and pos[1]['data']['coordinates']['x'] > 0):
                    if(pos[1]['data']['coordinates']['y'] < 1155 and pos[1]['data']['coordinates']['y'] > -200):
                        print("Section 2")
                        section = 2
                        t = time.time()
                if(pos[1]['data']['coordinates']['x'] < 5155 and pos[1]['data']['coordinates']['x'] > 2655):
                    if(pos[1]['data']['coordinates']['y'] < 1155 and pos[1]['data']['coordinates']['y'] > -200):
                        print("Section 3")
                        section = 3
                        t = time.time()
                if(pos[1]['data']['coordinates']['x'] < 7655 and pos[1]['data']['coordinates']['x'] > 5155):
                    if(pos[1]['data']['coordinates']['y'] < 1155 and pos[1]['data']['coordinates']['y'] > -200):
                        print("Section 4")
                        section = 4
                        t = time.time()
                if(pos[1]['data']['coordinates']['x'] < 7810 and pos[1]['data']['coordinates']['x'] > 6655):
                    if(pos[1]['data']['coordinates']['y'] < 4085 and pos[1]['data']['coordinates']['y'] > -100):
                        print("Section 5")
                        section = 5
                        t = time.time()
                
                if(section != None):
                    payload = json.dumps({
                        "state": True,
                        "triggerId": str(section),
                        "screenIds": [ 40 ]
                })
                

            except:
                print("NA")
            if(section != None):
                #print("Section not zero")
                if (t - prevt > 2):
                    #print(str(t) + " - " + str(prevt) + " Time enough")
                    #print("Previous :" + prevsec + "Now :" + section)
                    if(prevsec != section):
                        response = requests.request("POST", url, headers = headers, data = payload)
                        print("Trigger :" + str(section))
                        print(response.text)
                        time.sleep(0.5)
                    prevsec = section
                    prevt = t
            else:
                t = time.time()
        
client = mqtt.Client(transport = "websockets")
client.username_pw_set(username, password = password)

# sets the secure context, enabling the WSS protocol
client.tls_set_context(context=ssl.create_default_context())

# set callbacks
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.connect(host, port=port)
client.subscribe(topic)
time.sleep(2)

# works blocking, other, non-blocking, clients are available too.
client.loop_forever()