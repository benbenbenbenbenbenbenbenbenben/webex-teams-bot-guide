# Webex Teams Bot Guide

From the ground up create a fundamentals Webex Teams Bot that can GET and POST messages in a Webex room using Python.

## Requirements

* Postman
* Webex Bot and Token
* Python
* Ngrok

### Postman

1. Install Postman
2. Download Postman Collection
https://github.com/CiscoDevNet/postman-webex#teams-api
    1. Click > Run in Postman

### Webex Bot

1. Login to Webex Developer site https://developer.webex.com/my-apps
2. Create a Bot (Create a new App > Create a new Bot)
    1. Give your bot a name, username and description
    2. Copy the generated Access Token (store somewhere safe for later)
3. Add your Bot to a Webex Teams Space
    1. In Webex Teams click the + button and create a space
    2. Give your space a name and add your Bot (i.e. mybot@webex.bot)
    3. Click Create
    4. Say “Hello” if you want :)

### Python
1. Ensure you have Python version 3 installed (If not download and install)
```bash
$ python3 -V
```
2. In terminal window goto your working folder (Documents etc) create a Python 3 virtual environment using this command:
```bash
$ python3 -m venv bot
```
3. Now "activate" the environment
```bash
$ source bot/bin/activate
```
4. Install required packages (Flask a lightweight web app framework and requests a HTTP library)
```bash
$ pip install Flask requests
``` 

### Ngrok

Exposes your development environment to the Internet using a public URL so we can make use of Webhooks.
1. Signup for Free Ngrok Account https://ngrok.com/ and download Ngrok
2. Follow instructions in Ngrok to link authtoken 
3. Start Ngrok
```bash
$ ./ngrok http 5000
```
4. Copy the Ngrok Forwarding URL for later use (ie. https://353ffss.ngrok.io)

### File Structure
In a code editor (Visual Studio etc) create 3 new python files (see table below) and save these in the bot folder we created with our virtual environment.

| Filename        | Description             |
| ------------- |:-------------|
| app.py        | Our server file        |
| main.py       | Main functions to handle webhooks      | 
| chatbot.py    | Chat specific functions will live in here      |  

### Python Web Server
Flask is a web framework that allows us to quickly build web applications. As we installed it with pip we just need to import it into our code.

Route binds a function to a URL, in our case we are listening at the root of our app ```app.route("/")``` and returns a simple message if GET is used otherwise if POST it will print the posted data (webhook data)
1. Add the following code to ```app.py``` and save the file:
```python
from flask import Flask, request
 
app = Flask(__name__)

@app.route("/", methods=['POST','GET'])
def index():
   if request.method == 'GET':
      return '<h1>Hello from Webhook Listener App!</h1>'
   if request.method == 'POST':
      print(request.get_json())

if __name__ == "__main__":
    app.run(debug=True)
```
3. Ensure your virtual environment is active and run:
```bash
$ python3 app.py
```
4. Check the server is running http://127.0.0.1:5000/

5. Also check loading your ```Ngrok Forwarding URL``` to ensure you see the same content

When you loaded the above URL, you should see that it displayed some text on the webpage. This is because app.route is set for / and when that endpoint is accessed we run our index() function. In this case it checked that the request method when loading the webpage was GET.

Later after we setup our webhooks to listen for messages from Webex Teams, they will use POST to our server.

Now that we have our flask web app running we can move on to making Webex API calls in Postman and then come back to integrate the calls into our app.

## Making Calls with Postman
Postman is a great tool for quickly and easily testing APIs. It allows us to see exactly what response we get back from a request so we can then look how we might structure our code.
1. Add your Webex Bots Access Token to the Webex Environment in Postman 
![Image of adding Access Token](https://github.com/benbenbenbenbenbenbenbenbenben/webex-teams-bot-guide/blob/master/images/token.png?raw=true)  
2. From the Webex Teams API Collection select Rooms > List Rooms
![Image of postman](https://github.com/benbenbenbenbenbenbenbenbenben/webex-teams-bot-guide/blob/master/images/list-rooms.png?raw=true)  

3. Hit send to get back a JSON list of rooms your Bot is assigned to. You should see he is added to at least the 1 space we created earlier. Copy the value of id which will serve as our Room ID to post messages later.

4. Send your own message
    1. Select Messages > Create a Message (plain text)
    2. Click Body and change {{_room}} to the room id from step 3
    ![Image of postman](https://github.com/benbenbenbenbenbenbenbenbenben/webex-teams-bot-guide/blob/master/images/post-message.png?raw=true) 
    3. Hit send and you should see the text appear in your Webex Teams

### Setup Webhooks 
This is required to listen for events in webex teams so we can have our code perform different functions. Read more about Webex Webhooks here:
https://developer.webex.com/docs/api/guides/webhooks

We could also do this step in our code, however as it is only required once, it is easier to do so from Postman.

1. Select Webhooks > Create a webhook
    1. Click Body and update JSON replacing Ngrok in targetUrl with your ```Ngrok Forwarding URL``` and hit send to create our first webhook
```json
    {
      "name": "Listen for Messages Created Webhook",
      "resource": "messages",
      "event": "created",
      "targetUrl": "Ngrok"
    }
```
2. In your Webex teams bot room send it a message ```@mention Hello```. Check your terminal window running your app.py script to see it log the received webhook.
3. If you read through the log you may note that it does not list the Text data we sent, so we will need to go back to our app and add some additional code to get the message text.

## Python Making A Request

To see what a python request code looks like you can go to Postman, select again the Create a Message API and click code on the right hand side. Select Python Requests from the various languages. This will give you a code snippet that you could just copy paste into your code. We are going to make our own.

1. We are going to use main.py to run our main functions so that we can keep our flask script seperate.
    1. Edit app.py to import our main files funtions and instead of printing the webhook we want to call a function which we will call handler passing it the POST request we received.

```python
from main import *

return handler(request)
```

Your final app.py file should look like this:

```py
from flask import Flask, request
from main import *
 
app = Flask(__name__)

@app.route("/", methods=['POST','GET'])
def index():
   if request.method == 'GET':
      return '<h1>Hello from Webhook Listener App!</h1>'
   if request.method == 'POST':
      return handler(request)

if __name__ == "__main__":
    app.run(debug=True)
```

### Creating Functions

In this section we will setup our main.py file to handle the webhook data and respond back to the user if they said a greeting. 

The below code has been setup to:
* Import our modules
* Add the Bot's variables
* Main handler function that accepts the webhook post request 
* Extracts and prints the json payload from request
* Returns back to our app.py file to complete the request

```py
# Import modules
from flask import request
from chatbot import *

# Variables
bot_token = "YOUR TOKEN"
bot_email = "yourbot@webex.bot"

# Main handler function
def handler(request):
    webhook_event = request.get_json()
    print(webhook_event)

    # TODO: Ignore Bots Messages

    # TODO: Get Message Text

    # TODO: Respond To Users Messages

    return 'success' 
```

We have 3 conditions to build in this file:
1. Check ```if``` the webhook alert is triggered by the Bot
2. Extract the message text ```if``` webhook resource is a message
3. Post a message back to the user ```if``` they said a greeting

#### 1. Ignore Bots Messages
Based on the webhook json data we have how do we check to see if it is from our Bot? Lets take a look at the data:
```json
{
   "id":"Y2lzY29zcGFyazo.....",
   "name":"Listen Messages Created Webhook",
   "targetUrl":"http://8d.ngrok.io/",
   "resource":"messages",
   "event":"created",
   "orgId":"Y2lzY29zc...",
   "createdBy":"Y2lzY29zcGFy...Q",
   "appId":"Y2lzY29zcGF...",
   "ownedBy":"creator",
   "status":"active",
   "created":"2020-03-20T09:07:31.684Z",
   "actorId":"Y2lzY29zc...",
   "data":{
      "id":"Y2lzY29zc...",
      "roomId":"Y2lzY29z...",
      "roomType":"group",
      "personId":"Y2lzY2...",
      "personEmail":"youbot@webex.bot",
      "created":"2020-03-24T13:53:07.584Z"
   }
}
```
From this sample you can see the JSON object has a resource key with the value of messages and another key called data that has a nested object with personEmail. We can use these two bits to check it was a message and from our bot. 

```py
    # Ignore Bots Messages
    if webhook_event['resource'] == 'messages' and webhook_event['data']['personEmail'] == bot_email:
        return 'success'
```

#### 2. Extract the message text
As you saw from the above json data there was no text from the user so we will need to get that. Lets look at the webex api docs to see what we need to get the text:

> Get Message Details: Shows details for a message, by message ID.
Specify the message ID in the messageId parameter in the URI.
https://developer.webex.com/docs/api/v1/messages/get-message-details

We can use the value of id in the webhook data object to get the message details. As this is a chatbot specific task we will create a function here that calls another function in ```chatbot.py``` to make the api get request.

To make the api call we also need to authenticate with the ```authorization header``` using our ```Bot Token```. Add this just after you print the webhook data:
```py
    headers = {
        'authorization': f'Bearer {bot_token}' 
    }
```

Our function which we pass two params (webhook data and headers), we will assign the returned value to message variable and then print the message text to the console:
```py
    # Get Message Text From Webhook Alert
    if webhook_event['resource'] == 'messages':
        message = get_message(webhook_event, headers)
        print('Text Received: ' + message)
```

#### 3. Post a message back to the user
Now that we have recevied the text from the user we can check if it contains any keywords like a greeting. If it matches a greeting then we want to respond. Feel free to customise the greetings by adding your own in the array ```['greeting']```.  

We will have our ```chatbot.py``` file run the logic for checking if the users message (obtained from step 2 above) matches any keyword in the array.

If we find a match then our conditional if statement returns true and it will proceed to post a message to the Webex room. For this again we will use ```chatbot.py```, passing the payload which contains the room id, the text we want to respond and our headers:

```py
    # Respond To Users Messages
    if message_contains(message, ['hello', 'hi', 'greetings', 'gday']):
        post_message(payload,'Hello Human', headers)
```

### Chatbot (GET and POST)
As we built in our ```main.py``` file, have 3 functions to build in our ```chatbot.py``` file:
1. Get the message text
2. Check if message contains a greeting
3. Post message to teams

This will be our base code:
```py
# Import modules
import json
import requests

# TODO: Get the event (most recent message) that triggered the webhook

# TODO: Check whether message contains one of multiple possible options

# TODO: Post a message in Webex Teams

```
#### 1. Get Message
The function will make an api call to webex teams using a get request. Once this is received back we convert to json and assign this to the response varaiable and return the text value from the response object.. 

We are accepting two arguments, the webhook event data and our headers.

>To determe the correct URL, we can check the docs:
https://developer.webex.com/docs/api/v1/messages/get-message-details

So to get the message details we need to add the ```id``` to the url: https://api.ciscospark.com/v1/messages/. 
If we reference back to our json data the id value is stored in 
```json
"data":{ "id":"Y2lzY29zc..."}
```
We can append the url string like so: 
```py 
f'https://api.ciscospark.com/v1/messages/{event["data"]["id"]}
```

Putting this all together, our function will be:

```py
def get_message(event, headers):
    url = f'https://api.ciscospark.com/v1/messages/{event["data"]["id"]}'
    response = requests.get(url, headers=headers).json()
    return response['text']
```
#### 2. Check Message
Again we are accepting two arguments, the text we extracted from the webhook event data and our possible greeting combinations.

We convert the text to lower case as 'TEXT' != 'text'. Then loop through each option (greeting) from our options array. If it matches with a word in our message string we return back ```true``` otherwise no match found and returns ```false```.

```py
def message_contains(text, options):
    message = text.lower()
    for option in options:
        if option in message:
            return True
    return False
```
#### 3. Post Message
This functions requires 3 arguments; payload, message and headers.

Payload contains our room_id set already in main.py when the webhook was received. We will assign the message (which contains the text we want to send) to 'markdown' which will be added in our payload. 

>Very much like the get request earlier we can check the doc to see the URL we need to hit:
https://developer.webex.com/docs/api/v1/messages/create-a-message

Instead of using ```data=json.dumps(payload)``` we can pass the payload to the ```json``` parameter in the request which will encode it automatically for us.

There is no need for this function to return anything back.

Our function will be:

```py
def post_message(payload, message, headers):
    payload['markdown'] = message
    requests.post('https://api.ciscospark.com/v1/messages/',headers=headers,json=payload)
```

### Final Testing
```@mention``` your bot and say a greeting (hi, hello etc). You should now see it post a message back!

## Next Steps
This should have given you the basics to creating your own chatbot using Webex Teams and Python. Why not try creating your own logic to handle if a user asks for a joke or to check if their network devices are online!

Here is two resources to help you out:
* Dad jokes api: https://icanhazdadjoke.com/api
* Cisco Meraki api: https://developer.cisco.com/meraki/api/#/rest


## License
MIT


