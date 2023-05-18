import os
import pickle
import json
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

def loadPickle(filePath):
    with open(filePath, "rb") as file:
        data = pickle.load(file)

    return data

def repr(map):
    print(json.dumps(map, indent=4))

def printMap(filePath):
    map = loadPickle(filePath)
    print(filePath)
    repr(map)
    print(" ")

if __name__ == "__main__":
    perAlpha = os.path.join(os.getcwd(),"perAlphaAverageWaitingTimeMap.pickle")
    waitingTimes = os.path.join(os.getcwd(),"waitingTimeMap.pickle")
    avgWaiting = os.path.join(os.getcwd(),"averageWaitingTimeMap.pickle")

    for fp in [waitingTimes, avgWaiting, perAlpha]:
        printMap(fp)

    plt.plot(
            loadPickle(perAlpha).keys(),
            loadPickle(perAlpha).values(),
            marker='o'
            )

    plt.grid(True)
    plt.xlabel('alpha')
    plt.ylabel('average waiting time (sec)')

    plt.show()
    plt.savefig(os.path.join(os.getcwd(), "waitingTimes_vs_alpha"))

    plt.clf()

    waitingTimesMap = loadPickle(waitingTimes)
    averageWaitingTimeMap = loadPickle(avgWaiting)

    _tmp = averageWaitingTimeMap[0.1]

    for fn_name, _ in _tmp.items():
        plt.plot(
                averageWaitingTimeMap.keys(), # all alphas
                [averageWaitingTimeMap[alpha][fn_name] for alpha in averageWaitingTimeMap.keys()],
                label=fn_name,
                marker="^"
                )
    plt.legend()

    plt.xlabel("alpha")
    plt.ylabel("avg. waiting time (s)")
    plt.show()
    plt.clf()


    # some results don't have the following files so they may fail at this point.
    exeTimePath = os.path.join(os.getcwd(), "exeTimeMap.pickle")
    predTimePath = os.path.join(os.getcwd(), "predTimeMap.pickle")

    exeTimeMap = loadPickle(exeTimePath)
    predTimeMap = loadPickle(predTimePath)

    alphas = exeTimeMap.keys()
    functions = exeTimeMap[0.1].keys()

    for fn in functions:
        for alpha in alphas:
            plt.plot(
                    [i for i in range(len(exeTimeMap[alpha][fn]))],
                    exeTimeMap[alpha][fn],
                    marker="^",
                    label="execution time"
                    )
            plt.plot(
                    [i for i in range(len(predTimeMap[alpha][fn]))],
                    predTimeMap[alpha][fn],
                    marker="v",
                    label="predicted time"
                    )

            plt.ylim(0, 3)
            
            plt.grid(True)
            plt.title(f"{fn}-{alpha}")
            plt.xlabel('nth invocation')
            plt.ylabel('execution time (s)')
            plt.legend()
            plt.show()
            plt.clf()
