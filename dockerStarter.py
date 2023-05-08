import docker
import sys
import datetime
import time
import queue
# for log in container.logs(stream=True):
    # print(log.strip().decode('utf-8'))

# log_chunk = client.containers.run(**test_container_config)
#

def cleanupIsoTime(t):
    t = t[:-1]
    t = t + '0'*(26-len(t))

    return t

class Function:

    def __init__(self, name="test.js"):
        self.name = name
        self.arrivalTime = -1.0

    @property
    def path(self):
        return "functions/" + self.name

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
functionArrivalTimeMap: dict[int, list[Function]] = {
        0: [Function("fetchJsonExtended.js")],
        1: [Function(), Function( "fetchGithubUser.js")],
        2: [Function()],
        3: [Function()],
        5: [Function()],
        7: [Function()],
        10: [Function()],
        13: [Function()],
        15: [Function()],
}

# a map of running containers id to the functions they're running
invocationContainerMap = {}


############## Utility methods ##################
def getExeTime(info):
    """returns the total running time of a container after it has exited"""
    st = info["State"]["StartedAt"][:26]
    ft = info["State"]["FinishedAt"][:26]

    st = datetime.datetime.fromisoformat(st)
    ft = datetime.datetime.fromisoformat(ft)

    return (ft - st).total_seconds()

def infoLog(time, msg):
    print(f"[{time:.2f}] {msg}")

############# MAIN FUNCTION #######################
if __name__ == "__main__":
    function = sys.argv[1]

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
            'image': 'node:16',
            # 'name': 'tmp',
            'detach': True,
            # 'stream': True,
            # 'command': f'node {function}'
            'volumes': volume_config,
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
            'command': f'node {function}',
            # 'command': 'ping google.com',
            # 'command': 'echo hello world',
            # 'command': 'node',
            # 'tty': True
            'volumes': volume_config,
            }
    # ************END OF TEST CONFIG*****************************
    # container = client.containers.run(**container_config)
    print(test_container_config['command'])
    # container = client.containers.run(**test_container_config)

    st = time.time()
    container_logs = client.containers.run(**test_container_config)
    et = time.time()


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

    print(container_logs)
    client.containers.get("tmp").remove()

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

    timeDiff = (et - st) * 1000
    print(f"total time = {timeDiff} milliseconds")
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
    DEFAULT_VALUE = 0.7
    DEFAULT_VALUE_TWO = DEFAULT_VALUE
    st = time.time()
    alpha = 0.5
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

                    infoLog(currTime, f"container {client.containers.get(k).name}, running function {v} has finished executing and will be removed")
                    client.containers.get(k).remove()
                    del invocationContainerMap[k]
                    currContainers -= 1

        if int(currTime) in functionArrivalTimeMap:
            for fn in functionArrivalTimeMap[int(currTime)]:
                infoLog(currTime, f"new Function arrival {fn.name}")

                # set actual arrival time for function fn
                fn.arrivalTime = currTime

                if fn.name in predictedExecutionTimeMap:
                    prevPred = predictedExecutionTimeMap[fn.name]

                    # in case the first container for this function hasn't finished running and we don't have any latest execution time
                    try:
                        latestExecutionTime = latestExecutionTimeMap[fn.name]
                    except KeyError:
                        latestExecutionTime = prevPred
                else:
                    prevPred = DEFAULT_VALUE
                    latestExecutionTime = DEFAULT_VALUE_TWO


                # predict execution time here and put that in the priority queue ds which is taskQueue
                newPred = (1-alpha)*prevPred + alpha * latestExecutionTime
                predictedExecutionTimeMap[fn.name] = newPred
                taskQueue.put((fn.arrivalTime + newPred, fn))

        if not taskQueue.empty() and currContainers < CONTAINER_POOL_LIMIT:
            function = taskQueue.get()[1]

            # calculate waiting time and store it in a map
            # might have rewrite the map to store for different values of alpha
            functionWaitingTime = currTime - function.arrivalTime
            waitingTimeMap[function.name] = functionWaitingTime

            currContainer = client.containers.run(command=f"node {function.path}", **container_config)
            infoLog(currTime, f"{function.name} being executed in a container with the container name {currContainer.name}")
            invocationContainerMap[currContainer.id] = function.name
            currContainers += 1

        if taskQueue.empty() and currTime > 20:
            break

        time.sleep(0.1)



