import json

print ("Interface Status")

print ("================================================================================")

print ("DN                                                 Description           Speed    MTU  ")

print ("-------------------------------------------------- --------------------  ------  ------")

with open("sample-data.json", "r") as file:
    data = json.load(file)
    for i in  data ['imdata']:
        print (f"{i['l1PhysIf']['attributes']['dn']}                              {i['l1PhysIf']['attributes']['speed']}   {i['l1PhysIf']['attributes']['mtu']}")