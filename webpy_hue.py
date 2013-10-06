import web
import json
import hue
from time import strftime

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

'''
The hue api expects a username, we will accept any string here.
Each url of the api is bound to a class that handles the different http-methods.
'''
urls = (
    '/api/.*/lights',       'api_light_collection',
    '/api/.*/lights/new',   'api_light_collection',
    
    '/api/.*/lights/(\d+)', 'api_light',
    
    '/api/.*/config',       'api_config',
    #'/api/.*',              'api_config',
    
    '/api.*',               'api',
)

class api:
    def GET(self):
        print "Handle GET api"
        hue.full_state.config.whitelist = hue.users
        return json.dumps(todict(hue.full_state))

    def PUT(self):
        print "handle PUT api"
        return ""
        
    def POST(self):
        print "handle POST api"
        request_body = json.loads(web.data())
        hue.users[request_body["username"]] = {}
        hue.users[request_body["username"]]['devicetype'] = request_body["devicetype"]
        create_date = strftime("%Y-%m-%dT%H:%M:%S")
        hue.users[request_body["username"]]['create date'] = create_date
        hue.users[request_body["username"]]['last use date'] = create_date
        return "[{\"success\":{\"username\": \"" + request_body["username"] + "\"}}]"

class api_light_collection:
    def GET(self):
        print "Handle GET light_collection"
        return json.dumps(todict(hue.full_state.lights))

class api_light:
    def GET(self, id):
        print "Handle GET light"
        return json.dumps(todict(hue.full_state.lights[id]))
        
    def PUT(self, light_id):
        print "Handle PUT light"
        request_body = json.loads(web.data()) 
        hue.full_state.lights[light_id].name = request_body['name']
        return json.dumps({'success': {'/lights/' + light_id + '/name': hue.full_state.lights[light_id].name}})

class api_config:
    def GET(self):
        print "Handle GET api_config"
        hue.full_state.config.whitelist = hue.users
        return json.dumps(todict(hue.full_state.config))

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()