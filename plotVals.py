import matplotlib.pyplot as plt

#====================================================================================================

def main():

    # read results
    puzzleRatings = []
    gameRatings   = []

    with open("results.txt", "r") as f:
        for line in f:
            strippedLine = line.strip("\n").split(" ")
            gameRatings += [int(strippedLine[0])]
            puzzleRatings += [int(strippedLine[1])]

    plt.scatter(gameRatings, puzzleRatings, c = "b", marker = ".")

    plt.ylabel("chess.com puzzle rating", fontsize = 15)
    plt.xlabel("chess.com game rating",   fontsize = 15)

    plt.savefig("chess_game_ratings_vs_puzzles.png")
    plt.show()

#====================================================================================================

if __name__ == "__main__":

    main()
