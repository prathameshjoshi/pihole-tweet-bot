#shebang needed for cronjob reference
#!/usr/bin/env python3

import credentials
import tweepy
import datetime
import json
import urllib3

# Add pihole ipaddress
pihole_api = 'http://path.to.your.pihole.url/admin/api.php'

#Reads and loads JSON data from Pi-Hole api URL specific to your static IP you set for your Raspberry Pi
http = urllib3.PoolManager()
req = http.request('GET', pihole_api)
data = json.loads(req.data.decode('utf-8'))

tweet_template = "\nAds Blocked: %s\nAds Percentage Today: %i\nDNS Queries Today: %s\nDomains Blocked: %s"

data = tweet_template % (data['ads_blocked_today'], float (data['ads_percentage_today']), data['dns_queries_today'], data['domains_being_blocked'])

def get_api(cfg):
        auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
        auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
        return tweepy.API(auth)

def main():
        #Here we are defining the parameters for accessing Twitter's API securely, fill in the key with your corresponding twitter credentials
        cfg = {
                "consumer_key":credentials.consumer_key,
                "consumer_secret":credentials.consumer_secret,
                "access_token":credentials.access_token,
                "access_token_secret":credentials.access_token_secret
                }
        api = get_api(cfg)

        #The inital tweet that gets posted with string concatenation
        tweet = "I am a #RaspberryPi #Python scripted bot\nThis is my daily #Pihole report:\n" + data  + "\n\nTime and date: " + datetime.datetime.today().strftime("%H:%M %m-%d-%Y")
        status = api.update_status(status=tweet)
        print(tweet)

if __name__ == "__main__":
        main()
