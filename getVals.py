import requests
import pprint
from chessdotcom import get_player_stats, get_player_profile
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
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

    puzzleRatings = []
    gameRatings   = []

    maxPlayers = len(data["players"]) if not args.maxPlayers else args.maxPlayers
    with IncrementalBar("Getting user data", max = maxPlayers) as bar:
        for i, player in enumerate(data["players"]):

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

            # FIXME, need to check if at least 10 games have been played of these categories
            # get ratings from each of these categories
            categories = ["chess_blitz", "chess_bullet", "chess_rapid", "chess_daily"]
            ratings = []
            for category in categories:
                if category not in player_stats.keys():
                    continue

                ratings += [player_stats[category][gameRatingType]["rating"]]

            # check we got at least 1 rating, else skip
            if len(ratings) == 0:
                continue
            
            maxRating = max(ratings)

            # only get here if we have both game and puzzle rating, add to store
            gameRatings += [maxRating]
            puzzleRatings += [puzzleRating]

            bar.next()
            i += 1

    # now we can plot the results

    #print(gameRatings)
    #print(puzzleRatings)

    plt.scatter(gameRatings, puzzleRatings, c = "b", marker = ".")

    plt.ylabel("chess.com puzzle rating", fontsize = 15)
    plt.xlabel("chess.com game rating",   fontsize = 15)

    #plt.show()
    plt.savefig("chess_game_ratings_vs_puzzles.png")

#====================================================================================================

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--maxPlayers", metavar = "MAXPLAYERS", type = int, help = "Maximum number of users to include")
    args = parser.parse_args()
    main(args)
