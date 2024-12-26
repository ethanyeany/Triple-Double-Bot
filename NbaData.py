from nba_api.live.nba.endpoints import boxscore
from nba_api.stats.endpoints import leaguegamefinder
from datetime import datetime, timedelta
from credentials import *
import tweepy

#Creates Tweepy auth to be used later on
client = tweepy.Client(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret)

class NbaData:

    def tweetGen(self):

        #Grabs the game ID's from the previous day and deletes any duplicate ID's
        z = 0
        todays = datetime.today()
        yesterday = todays - timedelta(days=1)
        date =  yesterday.strftime('%Y-%m-%d')
        gameFinder = leaguegamefinder.LeagueGameFinder(league_id_nullable='00')
        games = gameFinder.get_data_frames()[0]
        todaysGames = games[games.GAME_DATE.str.contains(date)]
        gameIdDupe = todaysGames['GAME_ID'].tolist()
        gameIds = list(set(gameIdDupe))
        
        #gameIdTestCase = ['0022400404', '0022400381', '0022400363', '0022401217', '0022401205']


        while z < len(gameIds):

            #Loop that loops through all of the Games from the previous day
            n = 0
            x = 0
            name = gameIds[z]
            obj = NbaData()
            obj.tweetHome(name, n, x)
            obj.tweetAway(name, n, x)
            z += 1


    def tweetHome(self, name, n, x):

       
             #Grabs the home players stats, and team their facing
             games = name
             box = boxscore.BoxScore(games)
             players = box.home_team.get_dict()['players']
             hometeamCity = box.away_team.get_dict()['teamCity']
             hometeamName = box.away_team.get_dict()['teamName']

             while n < len(players):
            
                #Creates array in order to let the loop check if a player scored a triple double 
                playerInfo = players[n]
                playerInfoArray = [playerInfo['statistics']['points'], playerInfo['statistics']['assists'], 
                                    playerInfo['statistics']['reboundsTotal'], playerInfo['statistics']['steals'], playerInfo['statistics']['blocks']]
                playerStats = [int(x) for x in playerInfoArray]
                tripleDouble = 0

                while x < len(playerStats):

                    #Loops checking each stat
                    if playerStats[x] >= 10:
                        tripleDouble += 1
                        x += 1
                    else:
                        x += 1

                
                if tripleDouble >= 3:

                    #If a player scored a triple double a tweet will be created then the varibles reset except for n which moves onto the next player
                    #Response works but isn't good for testing. The other prints are useful for testing
                    #The else print also cen be annoying but useful if testing for something
                    playerStats = [str(x) for x in playerInfoArray]

                    tweet = playerInfo['name'] + " scored a triple double with " + playerStats[0] + " PTS " + playerStats[1] + " RBS " + playerStats[2] + " AST " + playerStats[3] + " STL and " + playerStats[4] + " BLK against the " + hometeamCity + " " + hometeamName
                    print('home')
                    print(tweet)
                     #response = client.create_tweet(text=tweet)
                     #print(f"https://twitter.com/user/status/{response.data['id']}")
                    tripleDouble = 0
                    x = 0
                    n += 1

                else:

                    #print(playerInfo['name'] + " did not score a triple double")
                    tripleDouble = 0
                    x = 0
                    n += 1

    def tweetAway(self, name, n, x):

        
             #Does the same thing as the method above but uses the away team players instead
             games = name
             box = boxscore.BoxScore(games)
             players = box.away_team.get_dict()['players']
             hometeamCity = box.home_team.get_dict()['teamCity']
             hometeamName = box.home_team.get_dict()['teamName']

             while n < len(players):
            
                playerInfo = players[n]
                playerInfoArray = [playerInfo['statistics']['points'], playerInfo['statistics']['assists'], 
                                    playerInfo['statistics']['reboundsTotal'], playerInfo['statistics']['steals'], playerInfo['statistics']['blocks']]
                playerStats = [int(x) for x in playerInfoArray]
                tripleDouble = 0

                while x < len(playerStats):

                    if playerStats[x] >= 10:
                        tripleDouble += 1
                        x += 1
                    else:
                        x += 1

                
                if tripleDouble >= 3:

                    playerStats = [str(x) for x in playerInfoArray]

                    tweet = playerInfo['name'] + " scored a triple double with " + playerStats[0] + " PTS " + playerStats[1] + " RBS " + playerStats[2] + " AST " + playerStats[3] + " STL and " + playerStats[4] + " BLK against the " + hometeamCity + " " + hometeamName
                    print('away')
                    print(tweet)
                     #response = client.create_tweet(text=tweet)
                     #print(f"https://twitter.com/user/status/{response.data['id']}")
                    tripleDouble = 0
                    x = 0
                    n += 1

                else:

                    #print(playerInfo['name'] + " did not score a triple double")
                    tripleDouble = 0
                    x = 0
                    n += 1
  
  