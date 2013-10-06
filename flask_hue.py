import hue
import json
from time import strftime
from flask import Flask, request

app = Flask(__name__)

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

@app.route('/debug', methods=['GET', 'PUT', 'POST', 'DELETE'])
def debug():
    if request.method == 'GET':
        print "handle GET"
        return ""
        
    if request.method == 'PUT':
        print "handle PUT"
        return ""

    if request.method == 'POST':
        print "handle POST"
        return ""
        
    if request.method == 'DELETE':
        print "handle DELETE"
        return ""


@app.route('/api', methods=['POST'])
def api():
    print "handle POST api"
    request_body = json.loads(request.form.keys()[0])
    hue.users[request_body["username"]] = {}
    hue.users[request_body["username"]]['devicetype'] = request_body["devicetype"]
    create_date = strftime("%Y-%m-%dT%H:%M:%S")
    hue.users[request_body["username"]]['create date'] = create_date
    hue.users[request_body["username"]]['last use date'] = create_date
    return "[{\"success\":{\"username\": \"" + request_body["username"] + "\"}}]"
        
@app.route('/api/<username>', methods=['GET'])    
def api_user(username):
    # if name in hue.users, else unauthorized
    print "Handle GET api"
    hue.full_state.config.whitelist = hue.users
    return json.dumps(todict(hue.full_state))
    
@app.route('/api/<username>/lights', methods=['GET'])  
def api_lights(username):
    print "Handle GET light_collection"
    return json.dumps(todict(hue.full_state.lights))

@app.route('/api/<username>/lights/<int:light_id>', methods=['GET', 'PUT'])
def api_light(username, light_id):
    if request.method == 'GET':
        print "Handle GET light"
        return json.dumps(todict(hue.full_state.lights[light_id]))
        
    if request.method == 'PUT':
        print "Handle PUT light"
        request_body = json.loads(request.data) 
        hue.full_state.lights[light_id].name = request_body['name']
        return json.dumps({'success': {'/lights/' + light_id + '/name': hue.full_state.lights[light_id].name}})

@app.route('/api/<username>/config', methods=['GET'])  
def api_config(username):
    print "Handle GET api_config"
    hue.full_state.config.whitelist = hue.users
    return json.dumps(todict(hue.full_state.config))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1234, debug=True)