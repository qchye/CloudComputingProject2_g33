import tweepy
from TwitterHarvesterFunc import mainFunction, all_keywords, all_regions, snd_half_keywords, MAX_COUNT


def main():

    auth = tweepy.AppAuthHandler(
        "PmRzO6aE5UCwbU9e9hUWS0PKv", "uV88V1zKlqyEIayVfWnLfCXyTKJngT2u6RUaGO4SpIEfeM4QLm")
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)
    half_keywords = snd_half_keywords
    keywords = all_keywords
    region = all_regions
    count = MAX_COUNT
    language = 'en'
    mainFunction(api, half_keywords, keywords, count, language, region)

    return


main()
