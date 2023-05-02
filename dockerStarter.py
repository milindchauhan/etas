import docker
import sys
import datetime
import time

# for log in container.logs(stream=True):
    # print(log.strip().decode('utf-8'))

# log_chunk = client.containers.run(**test_container_config)
#

def cleanupIsoTime(t):
    t = t[:-1]
    t = t + '0'*(26-len(t))

    return t

if __name__ == "__main__":
    function = sys.argv[1]

    client = docker.from_env()


    # ************THIS CONFIG WORKS PERFECTLY FOR LOGGING********
    # ************PLEASE DON'T TOUCH*****************************
    container_config = {
            'image': 'node:16',
            'name': 'tmp',
            # 'detach': True,
            'stream': True,
            'command': f'node {function}'
            }

    # ***********END OF CONFIG***********************************

    # ************VOLUME CONFIG*********************************
    '''
    # volume config format
    volume_config = {
            '<host path>': {
                'bind': '<path inside container>',
                'mode': 'ro'
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

    # ***********TEST CONFIG FOR CONTAINER**********************
    # I probably don't need to put the command in the config dictionary,
    # as the command might change
    test_container_config = {
            'image': 'node:16',
            # 'command': 'echo hello world!',
            'name': 'tmp', 
            'detach': True,
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
    container = client.containers.run(**test_container_config)


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
    time.sleep(2)
    print(container.logs())


    client = docker.APIClient()
    info = client.inspect_container(container.id)

    # fromisoformat function can only take in string values of len 26
    container_startedAt = info["State"]["StartedAt"][:26]
    container_finishedAt = info["State"]["FinishedAt"][:26]
    print(container_startedAt)
    print(container_finishedAt)

    startTime = datetime.datetime.fromisoformat(container_startedAt)
    finishTime = datetime.datetime.fromisoformat(container_finishedAt)

    timeDiff = (finishTime - startTime).total_seconds() * 1000

    print("total time ", timeDiff)
    container.remove()
