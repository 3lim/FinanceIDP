import twitter, yaml, os.path, sys, json

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

def main():
    config = read_config()
    twitter_api = load_twitter(config)

    track_languages = ['en']
    track_stocks = ['Google']

    for line in twitter_api.GetStreamFilter(track=track_stocks, languages=track_languages):
        #tweet = json.loads(line)
        print(line['text'].encode("utf-8"))
        print('\n')


if __name__ == '__main__':
    main()
