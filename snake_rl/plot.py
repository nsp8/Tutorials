from random import choices
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


def plot(scores, mean_scores):
    if scores and mean_scores:
        plt.clf()  # clear previous frame
        plt.title("Training")
        plt.xlabel("Number of games")
        plt.ylabel("Score")
        plt.plot(scores, label="Score")
        plt.plot(mean_scores, label="Mean Score")
        plt.ylim(ymin=0)
        # Force x and y ticks to be integers
        plt.gca().xaxis.set_major_locator(MultipleLocator(1))
        plt.gca().yaxis.set_major_locator(MultipleLocator(1))
        last_score = scores[-1]
        last_mean_score = mean_scores[-1]
        plt.text(len(scores) - 1, last_score, str(last_score))
        plt.text(len(mean_scores) - 1, last_mean_score, str(last_mean_score))
        plt.legend()
        plt.show(block=False)
        plt.pause(0.1)


def plot_test():
    plot(choices(range(2, 10), k=10), choices(range(2, 10), k=10))
