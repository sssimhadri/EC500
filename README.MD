# EC500 Assigment 2
Reviewer: Dana Szapiro

1)Test.py
- Clone twitter.py from master branch
- Clone Test.py
- Run code from command line

2)Webapp
- Clone Folder
- Add twitter credentials
- Run code with python3 app.py
- Navegate in browser to http://127.0.0.1:5000/

3) Code Review
The twitter.py module was functional but was missing several key factors from the assigment:
- It did not include the Google Vision API and was not doing any image recognition on the downloaded pictures from the twitter feed.
- There was almost no error handeling code. Most exceptions were handled by the API that the function was calling.
- Provided no information in the Readme file so it made it more difficult to start working with the code. 
Additionally, the code was design to be syncronous which makes the waiting time very long. It also stores all of the tweets in the feed in a file that never gets cleaned up which can also make it not very efficient memorywise.

# Program Runtime: 29.606 seconds
# Size of Memory required: 6464496 Bytes
