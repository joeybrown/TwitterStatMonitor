# Twitter StatMonitor

This is a program that will monitor Tweets from the Stream Sample API (aobut 1% of tweets at any given time)

Requirements:

1. Python 3 (better unicode support)
2. Rename Variables_example.py to Variables.py and fill in the keys & secrets and adjust any other variables. Get your 2 Twitter keys from dev.twitter.com
3. Redis server running (you can specify the port in Variables.py)
4. Packages in requirements.txt must be installed (pip)

To run it, just run main.py, and hit the endpoint '/getStats' (ex. localhost/getStats)

Let me know if you run into problems, and feel free to submit a pull request!
