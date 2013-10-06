
def todict(obj, classkey=None):
    '''
    Helper function to recursively transform custom classes to python
    dictionaries. Taken from here:
    http://stackoverflow.com/questions/1036409/recursively-convert-python-object-graph-to-dictionary
    '''
    if isinstance(obj, dict):
        for k in obj.keys():
            obj[k] = todict(obj[k], classkey)
        return obj
    elif hasattr(obj, "__iter__"):
        return [todict(v, classkey) for v in obj]
    elif hasattr(obj, "__dict__"):
        data = dict([(key, todict(value, classkey)) 
            for key, value in obj.__dict__.iteritems() 
            if not callable(value) and not key.startswith('_')])
        if classkey is not None and hasattr(obj, "__class__"):
            data[classkey] = obj.__class__.__name__
        return data
    else:
        return obj

#web.header('Content-Type', 'application/json')

class State:
    '''
    The class State holds the properties of a lamp's state.
    See the developers' api description from philips for further information.
    '''
    def __init__(self):
        self.on  = False
        self.bri = 0
        self.hue = 0
        self.sat = 0
        self.xy  = [0.0, 0.0]
        self.ct  = 0
        self.alert = "none"
        self.effect = "none"
        self.colormode = "hs"
        self.reachable = True

class Light:
    '''
    The class Light holds the properties of a lamp including its State.
    '''
    def __init__(self):
        self.type = "DIY color light"
        self.name = "My diy light"
        self.modelid = "DIY-1337"
        self.swversion = "1337"
        self.pointsymbol = {
            "1": "none",
            "2": "none",
            "3": "none",
            "4": "none",
            "5": "none",
            "6": "none",
            "7": "none",
            "8": "none"
        }
        self.state = State()

class Group:
    '''
    Lights can be combined to Groups.
    "action" holds the last command that was sent to the group.
    '''
    def __init__(self):
        self.action = {
            "on" : True,
            "bri": 254,
            "hue": 33536,
            "sat": 144,
            "xy" : [0.0, 0.0],
            "ct" : 153,
            "effect": "none",
            "colormode": "xy"
        },
        self.lights = {}
        self.name = "My Group"

class Config:
    '''
    The class Config holds the properties of the bridge itself.
    '''
    def __init__(self):
        self.name = "Smartbridge"
        self.mac  = "b1:6b:00:b5:ba:be"
        self.dhcp = True
        self.ipaddress = "192.168.1.24:1234"
        self.netmask = "255.255.255.0"
        self.gateway = "192.168.1.1"
        self.proxyaddress = "none"
        self.proxyport = 0
        self.utc = "1970-01-01T00:00:01"
        self.whitelist = {}
        self.swversion = "1337"
        self.swupdate = {
            "updatestate": 0,
            "url": "",
            "text": "",
            "notify": False
        }
        self.linkbutton = True
        self.portalservices = False
    
class Schedule:
    '''
    The Schedule might be some timed action that the bridge sends to the lamps.
    '''
    def __init__(self):
        self.name = "My schedule",
        self.description = "",
        self.command = {
            "address": "/api/0/groups/0/action",
            "body": {
                "on": True
            },
            "method": "PUT"
        }
        self.time = "1970-01-01T00:00:00"
    
class FullState:
    '''
    THe combination of all the above containers.
    '''
    def __init__(self):
        self.lights = {}
        self.groups = {}
        self.config = Config()
        self.schedules = {}


'''
Create some default values
'''

users = {}
users["hue_hacker"] = {}
users["hue_hacker"]['devicetype'] = "generic device"
users["hue_hacker"]['create date'] = "2013-04-01T11:11:11"
users["hue_hacker"]['last use date'] = "2013-04-01T11:11:11"

light_1 = Light()
light_1.name = "Bedroom light"
full_state = FullState()
full_state.lights["1"] = light_1
