from flask import Flask
from flask import request
from flask_cors import CORS
import random
import json

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={
    r"/*": {
       "origins": "*"
    }
})

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/getuser')
def example():
    # Retrieve the value of the 'param' parameter from the URL
    param_value = request.args.get('userid')

    # Check if the parameter is present in the URL
    if param_value:
        return f'The value of "param" is: {param_value}'
    else:
        return 'No parameter "param" provided in the URL.'

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)
