#Removed cv2 and Numpy libraries and using Scikit-Image library instead
from __future__ import print_function
from flask import Flask, make_response, jsonify, request
from flask_restful import Resource, Api
from skimage import io
import pyzbar.pyzbar as pyzbar


app = Flask(__name__)
api = Api(app)

def decode(im) : 
  # Find QR codes
  decodedObjects = pyzbar.decode(im)
     
  return decodedObjects

class myAPI(Resource):
    @api.representation('application/json')
    def post(self):
        # First, get the url param from request body
        json_data = request.get_json(force=True)
        url_val = json_data['url']

        # Second, read the resource in url
        try:
            im = io.imread(url_val)
            # Third, try to decode
            decodedObjects = decode(im)
            # If decode fails, it returns an empty array
            if(len(decodedObjects) > 0):
                return make_response(jsonify(data=decodedObjects[0][0], url=url_val, tag_res=True), 200)
            return make_response(jsonify(data=[], url=url_val, tag_res= False), 200)
        except:
            return make_response(jsonify(error='bad request'), 400)
    
    def get(self):
        return 'hello world!'

api.add_resource(myAPI, '/tag_req')

if __name__ == '__main__':
    app.run(debug=True)