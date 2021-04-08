#!/usr/bin/env python3

import tweepy

auth = tweepy.OAuthHandler("OvFPT9Pa3vRXSs59u5C28UN9B",
                           "c4U6BcXJJAn3OSpgXfTA9os4Pwf6C3jehHSr0qbNMVGb2PVm56")

auth.set_access_token("1355907395852054529-FLiSg5BbC8dTChwr2MSD06CjkMMeWh",
                      "ULNIjElnAmxYH58rySr9FCsv2wMXlRCzzEzyb0OODsn2m")

api = tweepy.API(auth)

api.update_with_media("test.png","MOO!")
