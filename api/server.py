from flask import Flask
from flask import request
from flask_cors import CORS
from googleapiclient.discovery import build
import random
import json
API_KEY = 'AIzaSyAkvMQ8nlZtIHAlxBWzFXQNJ3oGF9ULAp0'

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
    with open('data.json', 'w') as file:
            json.dump(dataa, file, indent=2)

    return {'channeldetails': channeldetailss, 'videodetails':videos }

    if param_value:
        return f'The value of "param" is: {param_value}'
    else:
        return 'No parameter "param" provided in the URL.'
    

@app.route('/getdata')
def getdata():
    # Retrieve the value of the 'param' parameter from the URL
    try:
        with open('data.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}
    return data

if __name__ == '__main__':
    app.run(debug=True, port=5000)
