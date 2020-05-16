import tweepy
import json
from TwitterHarvesterFunc import mainFunction, all_keywords, all_regions, fst_half_keywords, MAX_COUNT


def main():

    auth = tweepy.AppAuthHandler(
        "X7zGj3Ow4bPu05Em8WGGsko3G", "VkYgRxRkid5Ru4cpU7QineZIK2icnpRIHpZpVGaH8RlSYCJIQG")
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)
    half_keywords = fst_half_keywords
    keywords = all_keywords
    region = all_regions
    count = MAX_COUNT
    language = 'en'
    variables = {}
    with open('variables.json') as json_file:
        variables = json.load(json_file)
    mainFunction(api, half_keywords, keywords, count, language, region, variables)

    return


main()
