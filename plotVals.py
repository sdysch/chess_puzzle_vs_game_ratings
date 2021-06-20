import matplotlib.pyplot as plt
import numpy as np

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

    # plot line of equal puzzle and game ratings
    minVal = min(min(gameRatings, puzzleRatings))
    maxVal = max(max(gameRatings, puzzleRatings))
    print(minVal)
    print(maxVal)

    x = np.array(range(minVal, maxVal, 1))
    y = x

    plt.plot(x, y, label = "Equal puzzle and game ratings", c = "r")
    plt.scatter(gameRatings, puzzleRatings, c = "b", marker = ".", label = "chess.com data")

    plt.ylabel("chess.com puzzle rating", fontsize = 15)
    plt.xlabel("chess.com game rating",   fontsize = 15)

    #plt.legend(loc = "best", fontsize = 5)
    plt.legend()

    plt.savefig("chess_game_ratings_vs_puzzles.png")
    plt.show()

#====================================================================================================

if __name__ == "__main__":

    main()
