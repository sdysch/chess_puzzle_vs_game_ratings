import requests
import pprint
from chessdotcom import get_player_stats, get_player_profile
from datetime import datetime, timedelta
from progress.bar import IncrementalBar
import argparse

#====================================================================================================

def main(args):
    # TODO, specify with argparse at runtime?
    URL = "https://api.chess.com/pub/country/GB/players"
    data = requests.get(URL).json()

    pp = pprint.PrettyPrinter()
    #pp.pprint(data)

    # TODO last rating or peak rating?
    # peak rating can be biased to the default chess.com starting rating
    gameRatingType   = "last"
    puzzleRatingType = "highest"

    chessRatings = []
    #puzzleRatings = []
    #gameRatings   = []

    # output file
    f = open("results.txt", "w")

    i = 0
    maxPlayers = len(data["players"]) if not args.maxPlayers else args.maxPlayers
    with IncrementalBar("Getting user data", max = maxPlayers) as bar:
        for player in data["players"]:

            if args.maxPlayers and i == maxPlayers:
                break

            # find time account was made, reject if newer than 4 weeks
            joinTimestamp = get_player_profile(player).json["player"]["joined"]
            now = datetime.now()
            difference = now - datetime.fromtimestamp(joinTimestamp)
            if difference < timedelta(weeks = 4):
                continue

            # get player's ratings

            player_stats = get_player_stats(player).json["stats"]
            #pp.pprint(player_stats)

            # puzzles
            # skip if no puzzle rating
            # doesn't seem possible to see how many puzzles the player has done :'(
            # However, a player who has done no puzzles has no rating. Best we can do is skip
            if "tactics" not in player_stats.keys():
                continue

            try:
                puzzleRating = player_stats["tactics"][puzzleRatingType]["rating"]
            except KeyError:
                continue

            # get ratings from each of these categories
            categories = ["chess_blitz", "chess_bullet", "chess_rapid", "chess_daily"]
            ratings = []
            for category in categories:
                if category not in player_stats.keys():
                    continue

                # get nGames of this category, skip if < args.minGames
                stats = player_stats[category]
                record = stats["record"]
                nGames = 0
                try:
                    nGames += record["win"]
                except KeyError:
                    pass
                try:
                    nGames += record["lose"]
                except KeyError:
                    pass
                try:
                    nGames += record["draw"]
                except KeyError:
                    pass

                if nGames < args.minGames:
                    continue

                ratings += [player_stats[category][gameRatingType]["rating"]]

            # check we got at least 1 rating, else skip
            if len(ratings) == 0:
                continue
            
            maxRating = max(ratings)

            # only get here if we have both game and puzzle rating, add to store
            #gameRatings += [maxRating]
            #puzzleRatings += [puzzleRating]
            #chessRatings += [(maxRating, puzzleRating)]
            f.write(str(maxRating) + " " + str(puzzleRating) + "\n")

            # only increment if we select this data point
            bar.next()
            i += 1

    # write results to file
    # with open("results.txt", "w") as f:
        # for result in chessRatings:
            # f.write(str(result[0]) + " " + str(result[1]) + "\n")
    f.close()

#====================================================================================================

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--maxPlayers", metavar = "MAXPLAYERS", type = int, help = "Maximum number of users to include")
    parser.add_argument("--minGames", metavar = "MINGAMES", type = int, default = 10, help = "Minimum number of games player must have in this category")
    args = parser.parse_args()
    main(args)
