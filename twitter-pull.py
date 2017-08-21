import twitter, yaml, os.path, sys, json, random, codecs, nltk
from time import gmtime, strftime, time
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
import re
import string
#import HTMLParser

def read_config():
    config = None
    with open('config.yml', 'r') as f:
        config = yaml.load(f)
    return config

def load_twitter(config):
    twitter_config = config["twitter"]
    twitter_api = twitter.Api(consumer_key=twitter_config["consumer_key"],
                  consumer_secret=twitter_config["consumer_secret"],
                  access_token_key=twitter_config["access_token"],
                  access_token_secret=twitter_config["access_token_secret"])
    return twitter_api

# each line in the file is a tracked word.
def load_tracked_words(filename):
    with open(filename, 'r') as f:
        content = f.readlines()
        # remove whitespace at beginning and end of each line.
        content = [x.strip() for x in content]
        return content
    return None

def filter_tweet(tweet):
    #html_parser = HTMLParser.HTMLParser()
    #escaped_tweet = html_parser.unescape(tweet)
    decoded_tweet = tweet.encode('ascii','ignore').decode('utf-8').lower()
    tweet_no_urls = re.sub(r'\s?https?:\/\/.*[\r\n]*', '', decoded_tweet, flags=re.MULTILINE)

    tokens = word_tokenize(tweet_no_urls)
    tokens_no_mentions = []
    found_mention = False
    translate_table = dict((ord(char), None) for char in string.punctuation)
    for token in tokens:
        stripped_token = token.translate(translate_table)
        if len(stripped_token) == 0 and not token[0] == '@':
            continue

        if stripped_token == 'rt':
            continue

        if not found_mention:
            if token[0] == '@':
                found_mention = True
                continue
            tokens_no_mentions.append(stripped_token)
        else:
            found_mention = False
    stop = set(stopwords.words('english'))
    removed_stopwords = [i for i in tokens_no_mentions if i not in stop]
    return removed_stopwords

def record_tweet_stream(twitter_api, tracked_words, output_file, time_limit_minutes=30):
    track_languages = ['en']
    time_start = time()

    with open(output_file, 'w',encoding="utf-8") as f:
        for line in twitter_api.GetStreamFilter(track=tracked_words, languages=track_languages):
            #tweet = json.loads(line)
            print(line['timestamp_ms'].encode('utf-8'))
            filtered_tweet = filter_tweet(line['text'])
            print(filtered_tweet)
            f.write(line['timestamp_ms'])
            f.write('\r\n')
            f.write(' '.join(filtered_tweet))
            f.write('\r\n')
            f.write('\r\n')
            f.flush()
            if time() - time_start > time_limit_minutes * 60:
                break

def main():
    config = read_config()
    twitter_api = load_twitter(config)

    # pick 200 randomly sampled words and stream for 30 minutes per sample endlessly.
    while True:
        tracked_words = random.sample(load_tracked_words(config["twitter"]["input_file"]), 200)
        print(tracked_words)
        print('\n')

        output_filename = str.format("tweet_stream_{}.json",strftime("%Y%m%d_%H%M%S",gmtime()))
        output_file = os.path.join(config["twitter"]["output_dir"],output_filename)

        record_tweet_stream(twitter_api, tracked_words, output_file)

if __name__ == '__main__':
    main()
