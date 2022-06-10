import time

def getTimeAsMS():
    return int(round(time.time() * 1000))


def main():


    lastTime = getTimeAsMS()

    while True:
        newTime = getTimeAsMS()
        if(newTime < lastTime + 200):
            continue
        
        print("lastTime", lastTime)
        lastTime = newTime
    
if __name__ == '__main__':
    main()
    
