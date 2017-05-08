## Twitter crawler
### Install Python dependencies
Execute in command line:
```
pip install pyyaml python-twitter
```
### Config
- Rename _config.yml.template_ to _config.yml_
- Add your Twitter API authentication details obtained by following the steps under section 1 [here](http://socialmedia-class.org/twittertutorial.html) to the respective entries in the config file
- Edit the keywords you want to follow in _data/stock-list.txt_
### Run
```
python twitter-pull.py
```
Tweets are saved into _data/tweet_dumps_ per default (one text file per run). Since the Twitter API limits how many keywords we are able to monitor at the same time, it picks a new set of 200 keywords every 30 minutes.
