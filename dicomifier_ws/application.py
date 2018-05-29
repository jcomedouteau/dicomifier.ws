import json
import os
import subprocess

import werkzeug
import werkzeug.exceptions
import werkzeug.routing
import yaml

class Application(object):
    _instance = None
    
    @staticmethod
    def instance():
        if Application._instance is None:
            Application._instance = Application()
        return Application._instance
    
    def __init__(self):
        self.routes = werkzeug.routing.Map([
            werkzeug.routing.Rule(
                "/bruker2dicom", methods=["POST"], endpoint = self.bruker2dicom),
            werkzeug.routing.Rule(
                "/dicom2nifti", methods=["POST"], endpoint = self.dicom2nifti)
        ])
    
    def __call__(self, environ, start_response):
        routes = self.routes.bind_to_environ(environ)
        request = werkzeug.Request(environ)
        try:
            endpoint, arguments = routes.match()
            response = endpoint(request)
        except werkzeug.exceptions.HTTPException as e:
            response = e
        except Exception as e:
            response = werkzeug.exceptions.InternalServerError(str(e))
        return response(environ, start_response)
        
    def bruker2dicom(self, request):
        data = json.loads(request.get_data().decode())
        
        source = data.get("source")
        if source is None:
            raise werkzeug.exceptions.BadRequest("Missing source")
        if not os.path.isdir(source):
            raise werkzeug.exceptions.NotFound("No such directory: {}".format(source))
        
        destination = data.get("destination")
        if destination is None:
            raise werkzeug.exceptions.BadRequest("Missing destination")
        
        return self._run(["bruker2dicom", "convert", source, destination])
    
    def dicom2nifti(self, request):
        data = json.loads(request.get_data().decode())
        
        source = data.get("source")
        if source is None:
            raise werkzeug.exceptions.BadRequest("Missing source")
        if not os.path.isdir(source):
            raise werkzeug.exceptions.NotFound("No such directory: {}".format(source))
        
        destination = data.get("destination")
        if destination is None:
            raise werkzeug.exceptions.BadRequest("Missing destination")
        
        return self._run(["dicom2nifti", "-z", source, destination])
    
    def _run(self, *args):
        try:
            stdout = subprocess.check_output(*args, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            raise werkzeug.exceptions.InternalServerError(e.stdout)
        else:
            return werkzeug.Response(
                json.dumps({"output": stdout.decode()}), 200, 
                {"Content-Type": "application/json"})
