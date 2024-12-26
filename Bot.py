#Created by Ethan Yeany
#12/26/24

import time
from NbaData import NbaData


while True:

    #Sleeps for one day in order to wait for nba.com to update
    obj = NbaData()
    obj.tweetGen()
    time.sleep(86400)
   