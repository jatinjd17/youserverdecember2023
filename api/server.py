import os
from flask import Flask,jsonify
from flask import request
from flask_cors import CORS
from googleapiclient.discovery import build
import random
import json
from bson import ObjectId, json_util
from flask_pymongo import PyMongo

API_KEY = os.environ.get('YOUTUBE_API_KEY')

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['MONGO_DBNAME'] = 'youtubeshoutoutapi'
app.config['MONGO_URI'] = os.environ.get('YOUTUBESERVER_MONGO_URI')
CORS(app)
cors = CORS(app, resources={
    r"/*": {
       "origins": "*"
    }
})
mongo = PyMongo(app)
channelinfocollection = mongo.db.channelinfo

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/getuser')
def example():
    # Retrieve the value of the 'param' parameter from the URL
    param_value = request.args.get('userid')

    # Check if the parameter is present in the URL
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    channeldetails = youtube.channels().list(
        part='snippet,contentDetails,statistics',
        id=param_value
    ).execute()

    channeldetailss = []

    for i in channeldetails['items']:
            channeldetailss.append({
                'channelname': i['snippet']['localized']['title'],
                'channeldescription': i['snippet']['localized']['description'],
                'channelthumbnail': i['snippet']['thumbnails']['medium']['url'],
        'subscriberscount':  i['statistics']['subscriberCount'],
        'totalvideos':  i['statistics']['videoCount'],
        'totalviews':  i['statistics']['viewCount'],
            })

    # return response

    youtube = build('youtube', 'v3', developerKey=API_KEY)
    response = youtube.search().list(
        part='snippet',
        channelId=param_value,
        type='video',
        maxResults=10  # You can adjust the number of results as needed
    ).execute()



    videos = []
    for item in response['items']:
        print(item)
        videos.append({
            'title': item['snippet']['title'],
            'video_id': item['id']['videoId'],
            'description': item['snippet']['description'],
            'thumbnailurl': item['snippet']['thumbnails']['medium']['url'],
        })
    dataa = {'channeldetails': channeldetailss, 'videodetails':videos }
    # Save data to JSON file
    # with open('data.json', 'w') as file:
    #         json.dump(dataa, file, indent=2)
    # channelinfocollection.delete_many({})
    sss = channelinfocollection.insert_one(dataa)

    # return {'channeldetails': channeldetailss, 'videodetails':videos }
    return 'Channel has been added to Shoutout wall. Please wait for sometime to reflect on stream.'

    if param_value:
        return f'The value of "param" is: {param_value}'
    else:
        return 'No parameter "param" provided in the URL.'
    

@app.route('/getdata')
def getdata():
    # Retrieve the value of the 'param' parameter from the URL
    # try:
    #     with open('data.json', 'r') as file:
    #         data = json.load(file)
    # except FileNotFoundError:
    #     data = {}
    # dataaa = channelinfocollection.find_one({})

    # ############### GET LATEST DOCUMENT FROM DB #####################
    latest_document = channelinfocollection.find_one(sort=[('_id', -1)])

    ################ CONVERT PY CURSOR DICT TO STRING JSON ###########
    latest_document_json = json_util.dumps(latest_document)

    ################ CONVERT STRING JSON TO JSON OBJECT ################
    getdatainjson = json.loads(latest_document_json)

    # print(type(latest_document_json))

    
    
    return getdatainjson

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)
