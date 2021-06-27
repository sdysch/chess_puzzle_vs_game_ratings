import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
from scipy.stats import pearsonr

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
    #print(minVal)
    #print(maxVal)

    x = np.array(range(minVal, maxVal, 1))
    y = x

    plt.plot(x, y, label = "Equal puzzle and game ratings", c = "r")
    plt.scatter(gameRatings, puzzleRatings, c = "b", marker = ".", s = 1, label = "chess.com data")

    plt.ylabel("chess.com puzzle rating", fontsize = 15)
    plt.xlabel("chess.com game rating",   fontsize = 15)

    #plt.legend(loc = "best", fontsize = 5)
    plt.legend()

    plt.savefig("chess_game_ratings_vs_puzzles.png")
    #plt.show()
    print(pearsonr(gameRatings, puzzleRatings))

    fig2, axs = plt.subplots(1, 2, figsize = (10, 5))
    #plt.tight_layout()


    bins = 25
    axs[0].hist(gameRatings, bins = bins, color = "blue")
    axs[0].set_xlabel("Game ratings")
    axs[0].set_ylabel("Events / bin")

    axs[1].hist(puzzleRatings, bins = bins, color = "blue")
    axs[1].set_xlabel("Puzzle ratings")
    axs[1].set_ylabel("Events / bin")

    #plt.show()
    fig2.savefig("hists_1D.png")

    fig3, axis = plt.subplots()
    #h = axis.hist2d(gameRatings, puzzleRatings, bins = [25, 25], norm = LogNorm())
    h = axis.hist2d(gameRatings, puzzleRatings, bins = [25, 25])
    #plt.show()
    axis.set_xlabel("Game ratings")
    axis.set_ylabel("Puzzle ratings")
    fig3.colorbar(h[3], ax=axis)

    fig3.savefig("hist_2D.png")

#====================================================================================================

if __name__ == "__main__":

    main()
