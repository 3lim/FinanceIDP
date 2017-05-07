import twitter, yaml, os.path, sys, json, random
from time import gmtime, strftime, time

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

def record_tweet_stream(twitter_api, tracked_words, output_file, time_limit_minutes=30):
    track_languages = ['en']
    time_start = time()

    with open(output_file, 'w',encoding="utf-8") as f:
        for line in twitter_api.GetStreamFilter(track=tracked_words, languages=track_languages):
            f.write(json.dumps(line))
            f.write('\n')
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
