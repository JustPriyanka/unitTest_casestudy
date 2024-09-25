import wrapper

def readhashLog(library):
    print('')
    while True:
        returnCode, logLine = wrapper.hashReadNextLogLine(library)
        if (int(returnCode) == 0):
            print('HashReadNextLogLine: {}.'.format(logLine))
        else:
            break
    return

def returnhashLogLine(library):
    while True:
        returnCode, logLine = wrapper.hashReadNextLogLine(library)
        if (int(returnCode) == 0):
            return format(logLine)

def waitforHashDirectory(library, opID:int):
    while True:
        returnCode, opRunning = wrapper.hashStatus(library, opID)
        if ((int(returnCode) != 0) or (opRunning != True)):
            break
    print('\nHashDirectory has finished.')
    return True