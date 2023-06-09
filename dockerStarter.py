import docker
import json
import pickle
import os
import sys
import datetime
import time
import queue
import statistics
# for log in container.logs(stream=True):
    # print(log.strip().decode('utf-8'))

# log_chunk = client.containers.run(**test_container_config)
#
############## Utility methods ##################
def getExeTime(info):
    """returns the total running time of a container after it has exited"""
    st = info["State"]["StartedAt"][:26]
    ft = info["State"]["FinishedAt"][:26]

    st = datetime.datetime.fromisoformat(st)
    ft = datetime.datetime.fromisoformat(ft)

    return (ft - st).total_seconds()


def getArrivalQueue(arrivalMap: dict):
    arrivalQueue = queue.PriorityQueue()
    for time, functions in arrivalMap.items():
        arrivalQueue.put((time, functions))

    return arrivalQueue

def getAverageWaitingTime(waitingTimeMap):
    averageWaitingTimeMap = {}

    for alpha, alphaMap in waitingTimeMap.items():
        innerDict = {}
        for fn, waitingTimes in alphaMap.items():
            innerDict[fn] = statistics.median_low(waitingTimes)

        averageWaitingTimeMap[alpha] = innerDict

    return averageWaitingTimeMap

def infoLog(time, msg):
    print(f"[{time:.2f}] {msg}")


def cleanupIsoTime(t):
    t = t[:-1]
    t = t + '0'*(26-len(t))

    return t

def getFunctionArrivalMap(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)

    res = {}

    for k, v in data.items():
        res[int(k)] = [Function(f) for f in v]

    return res

def logMapUtilFunction(file_path, map):
    with open(file_path, 'a') as fp:
        fp.write("\n" + datetime.datetime.now().strftime("%d-%m-%Y, %H:%M:%S") + "\n")
        fp.write(json.dumps(map, indent=4))
        fp.write("\n")

def getPerAlphaAverage(waitingTimeMap):
    res = {}

    for alpha, map in waitingTimeMap.items():
        # performance can be improved by doing this imperatively but what's the point?
        # this calculation happens at the end of the experiment anyway
        res[alpha] = statistics.median_low([i for waitingTimes in map.values() for i in waitingTimes])

    return res

class Function:

    def __init__(self, name="test.js"):
        self.name = name
        self.arrivalTime = -1.0

    @property
    def path(self):
        return self.name

    def __lt__(self, other):
       return self.arrivalTime < other.arrivalTime

'''
listOfFunctions= [
        Function(0),
        Function(1),
        Function(1),
        Function(2),
        Function(3),
        Function(5),
        Function(7),
        Function(10),
        Function(13),
        Function(15),
    ]
'''
functionArrivalTimeMap = getFunctionArrivalMap("functionArrivalQueue.json");


# a map of running containers id to the functions they're running
invocationContainerMap = {}


############# MAIN FUNCTION #######################
if __name__ == "__main__":
    client = docker.from_env()

    # ************VOLUME CONFIG*********************************
    '''
    # volume config format
    volume_config = {
            '<host path>': {
                'bind': '<path inside container>',
                'mode': 'ro'0ationTimeMa
                }
            }
    '''

    volume_config = {
            '/home/milind/code/etas/functions/': {
                'bind': '/functions/',
                'mode': 'ro'
                }
            }
    # ************END OF CONFIG*********************************


    # ************THIS CONFIG WORKS PERFECTLY FOR LOGGING********
    # ************PLEASE DON'T TOUCH*****************************
    container_config = {
            # 'image': 'node:16',
            'image': 'node-test',
            # 'name': 'tmp',
            'detach': True,
            # 'stream': True,
            # 'command': f'node {function}'
            # 'volumes': volume_config,
            }

    # ***********END OF CONFIG***********************************

    # ***********TEST CONFIG FOR CONTAINER**********************
    # I probably don't need to put the command in the config dictionary,
    # as the command might change
    test_container_config = {
            'image': 'node:16',
            # 'command': 'echo hello world!',
            'name': 'tmp', 
            # 'detach': True,
            # 'stdout': True,
            # 'stream': True,
            # 'command': f'node {function}',
            # 'command': 'ping google.com',
            # 'command': 'echo hello world',
            # 'command': 'node',
            # 'tty': True
            'volumes': volume_config,
            }
    # ************END OF TEST CONFIG*****************************
    # container = client.containers.run(**container_config)
    # print(test_container_config['command'])
    # container = client.containers.run(**test_container_config)

    # st = time.time()
    # container_logs = client.containers.run(**test_container_config)
    # et = time.time()


    '''
    # code to copy file to container volume. not required anymore
    # as I'm just loading the host folder as container volume

    with open(f'./{function}', 'rb') as f:
        container.put_archive('/functions/', f)

    container.exec_run(f'node {function}')
    '''
 
    '''
    # this is wrong because you would use the for loop construct when you're streaming
    # the logs with a detached container and if you're doing that then you shouldn't have
    # a container object container such that you can use container.logs()
    for line in container.logs(): 
        print(line)
    '''
    # time.sleep(2)
    # print(container.logs())

    # print(container_logs)
    # client.containers.get("tmp").remove()

    client2 = docker.APIClient()
    '''
    info = client2.inspect_container(client.containers.get("tmp").id)

    # fromisoformat function can only take in string values of len 26
    container_startedAt = info["State"]["StartedAt"][:26]
    container_finishedAt = info["State"]["FinishedAt"][:26]
    print(container_startedAt)
    print(container_finishedAt)

    startTime = datetime.datetime.fromisoformat(container_startedAt)
    finishTime = datetime.datetime.fromisoformat(container_finishedAt)
    timeDiff = (finishTime - startTime).total_seconds() * 1000

    '''

    # timeDiff = (et - st) * 1000
    # print(f"total time = {timeDiff} milliseconds")
    # container.remove()


    ######################## HANDLE QUEUE OF FUNCTIONS #######################

    predictedExecutionTimeMap: dict[str, float]= {}
    latestExecutionTimeMap = {}
    waitingTimeMap = {}

    '''
    for In in :
        if fn in predictedExecutionTimeMap:
            # after execution time prediction is done. run and get real execution time.
            st = time.time()
            currLogs = client.containers.run(**test_container_config)
            et = time.time()

            exeTime = (et - st)
        else:
            st = time.time()
            currLogs = client.containers.run(**test_container_config)
            et = time.time()

            exeTime = (et - st)
            predictedExecutionTimeMap[fn] = exeTime
    '''

    taskQueue: queue.PriorityQueue = queue.PriorityQueue()
    currContainers = 0
    CONTAINER_POOL_LIMIT = 3
    defaultExeTime = {
            "fetchGithubRepoDetails.js": 0.3,
            "fetchGithubUser.js": 0.27,
            "fetchJsonExtended.js": 0.8,
            "fetchCovidData.js": 0.5,
            "currencyExchange.js": 0.9,
            }
    st = time.time()
    alphas = [0.1, 0.2, 0.3, 0.4, 0.5]
    latestArrivedFunction = None
    midWaitingTimeMap = {}
    arrivalQueue = getArrivalQueue(functionArrivalTimeMap)
    exeTimeMap = {}
    predTimeMap = {}

    for alpha in alphas:
        midWaitingTimeMap = {}
        innerExeTimeMap = {}
        innerPredTimeMap = {}
        arrivalQueue = getArrivalQueue(functionArrivalTimeMap)

        while True:
            currTime = time.time() - st

            # check if any container has finished running.
            # if it has store it's execution time and remove it from the dictionary
            # k is the container id here
            if len(invocationContainerMap) > 0:
                for k, v in list(invocationContainerMap.items()):
                    info = client2.inspect_container(k)
                    if info["State"]["Status"] == "exited":
                        exeTime = getExeTime(info)
                        latestExecutionTimeMap[v] = exeTime

                        if v not in innerExeTimeMap:
                            innerExeTimeMap[v] = []

                        innerExeTimeMap[v].append(exeTime)

                        infoLog(currTime, f"container {client.containers.get(k).name}, running function {v} has finished executing and will be removed")
                        container = client.containers.get(k)
                        print(container.logs().decode())
                        container.remove()
                        del invocationContainerMap[k]
                        currContainers -= 1

            if latestArrivedFunction is None:
                if not arrivalQueue.empty():
                    latestArrivedFunction = arrivalQueue.get()

            elif latestArrivedFunction[0] <= int(currTime):
                infoLog(currTime, f"functions arrived till {int(currTime)} will be processed now")
                arrivedFunctions = latestArrivedFunction[1]
                for fn in arrivedFunctions:
                    infoLog(currTime, f"new Function arrival {fn.name}")

                    # set actual arrival time for function fn
                    fn.arrivalTime = currTime

                    # set entry in midWaitingTimeMap
                    if fn.name not in midWaitingTimeMap:
                        midWaitingTimeMap[fn.name] = []

                    if fn.name in predictedExecutionTimeMap:
                        prevPred = predictedExecutionTimeMap[fn.name]

                        # in case the first container for this function hasn't finished running and we don't have any latest execution time
                        try:
                            latestExecutionTime = latestExecutionTimeMap[fn.name]
                        except KeyError:
                            latestExecutionTime = prevPred
                    else:
                        prevPred = defaultExeTime[fn.name]
                        latestExecutionTime = prevPred


                    # predict execution time here and put that in the priority queue ds which is taskQueue
                    newPred = (1-alpha)*prevPred + alpha * latestExecutionTime
                    predictedExecutionTimeMap[fn.name] = newPred

                    if fn.name not in innerPredTimeMap:
                        innerPredTimeMap[fn.name] = []
                    innerPredTimeMap[fn.name].append(newPred)

                    taskQueue.put((fn.arrivalTime + newPred, fn))

                # del currTime entries in functionArrivalTimeMap
                infoLog(currTime, f"functions for arrival time {int(currTime)} have all been queued")
                latestArrivedFunction = None

            if not taskQueue.empty():
                function = taskQueue.get()[1]

                if currContainers < CONTAINER_POOL_LIMIT:
                    # calculate waiting time and store it in a map
                    # might have rewrite the map to store for different values of alpha
                    functionWaitingTime = currTime - function.arrivalTime
                    # waitingTimeMap[function.name] = (functionWaitingTime + (waitingTimeMap[function.name] if function.name in waitingTimeMap else functionWaitingTime) ) / 2
                    midWaitingTimeMap[function.name].append(functionWaitingTime)

                    currContainer = client.containers.run(command=f"node {function.path}", **container_config)
                    infoLog(currTime, f"{function.name} being executed in a container with the container name {currContainer.name}")
                    invocationContainerMap[currContainer.id] = function.name
                    currContainers += 1
                else:
                    taskQueue.put((currTime + predictedExecutionTimeMap[function.name], function))

            if taskQueue.empty() and arrivalQueue.empty() and len(invocationContainerMap) == 0:
                break

            time.sleep(0.1)

        waitingTimeMap[alpha] = midWaitingTimeMap
        exeTimeMap[alpha] = innerExeTimeMap
        predTimeMap[alpha] = innerPredTimeMap

    # at this point we have the waiting time map for all alphas
    # store them in pickle files.
    averageWaitingTimeMap = getAverageWaitingTime(waitingTimeMap)
    perAlphaAverageWaitingTimeMap = getPerAlphaAverage(waitingTimeMap)

    curr_time = datetime.datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
    directory = f"results/{curr_time}"
    os.makedirs(directory)

    with open(os.path.join(directory, "waitingTimeMap.pickle"), "wb") as file:
        pickle.dump(waitingTimeMap, file)

    with open(os.path.join(directory, "averageWaitingTimeMap.pickle"), "wb") as file:
        pickle.dump(averageWaitingTimeMap, file)

    with open(os.path.join(directory, "perAlphaAverageWaitingTimeMap.pickle"), "wb") as file:
        pickle.dump(perAlphaAverageWaitingTimeMap, file)

    with open(os.path.join(directory, "exeTimeMap.pickle"), "wb") as file:
        pickle.dump(exeTimeMap, file)

    with open(os.path.join(directory, 'predTimeMap.pickle'), "wb") as file:
        pickle.dump(predTimeMap, file)

    print(json.dumps(averageWaitingTimeMap, indent=4))


