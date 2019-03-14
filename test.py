import tweepy
import argparse
import re
import csv
import datetime


# COMMAND PARSER
def tw_parser():
    global user, f, t

    # Parse the command
    parser = argparse.ArgumentParser(description='Twitter Search User Timeline')
    parser.add_argument('-user', action='store', dest='user', help='id/name of the user you want to search',
                        default='realDonaldTrump')
    parser.add_argument('-f', action='store', dest='f', help='Search user timeline from \n with format: D/M/Y',
                        default=datetime.datetime.strptime("1/6/2017",'%d/%m/%Y'))
    parser.add_argument('-t', action='store', dest='t', help='Search user timeline to \n with format: D/M/Y',
                        default=datetime.datetime.now())
    args = parser.parse_args()
    user = args.user
    f = args.f
    t = args.t
    #check the format
    if type(f) != datetime.datetime:
        if re.search(r'\d+/\d+/\d+', f) is not None:
            try:
                f = datetime.datetime.strptime(f,'%d/%m/%Y')
            except ValueError:
                print('Please Enter Correct Format: D/M/Y')
        else:
            print('Please Enter Correct Format: D/M/Y')


    if type(t) != datetime.datetime:
        if re.search(r'\d+/\d+/\d+', t) is not None:
            try:
                t = datetime.datetime.strptime(t,'%d/%m/%Y')
            except ValueError:
                print('Please Enter Correct Format: D/M/Y')
        else:
            print('Please Enter Correct Format: D/M/Y')


    print('User: %s, From: %s, To: %s' % (user,f,t))


def tw_search(api):
    # Open/Create a csv file to append data
    csvFile = open('result1.csv', 'w', newline='', encoding='utf-8')
    # Use csv Writer
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(["created_at", "text", "retweet_count", "favorite_count", "source"])

    for tweet in tweepy.Cursor(api.user_timeline,
                               id=str(user),
                               tweet_mode = 'extended').items():

        # TWEET INFO
        # EXCLUSIVE THE RETWEET & TWEETS OUTSIDE THE TIME RANGE
        if f < tweet.created_at < t:
            if (not tweet.retweeted) and ('RT @' not in tweet.full_text):
                created_at = tweet.created_at
                text = tweet.full_text
                source = tweet.source
                retweet_count = tweet.retweet_count
                favorite_count = tweet.favorite_count
            else:
                continue
        else:
            break

        csvWriter.writerow([created_at, str(text).encode('utf-8'), retweet_count, favorite_count, source])

    csvFile.close()


# MAIN ROUTINE
def main():
    global api
    tw_parser()
    auth = tweepy.OAuthHandler('aHKA0GxVY5xDiZdMjnqxXWaKI', 'XuE4R5QrrZrYsyTnhJsJwCYR1YDsZdT2sfbGCRV2uvgRlmM5SE')
    auth.set_access_token('1092241640503238656-lI8FEhDtdReSsORorJNec6tMMLcrmH',
                          'ndiGLuhGImp5dtoxxz5T6mWz0UwZyBXDcpzO5MCngg5M3')

    api = tweepy.API(auth)
    tw_search(api)


if __name__ == "__main__":
    main()