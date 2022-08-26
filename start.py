from modules.listener import KjoretimeListener
from time import sleep
setup = False

if __name__ == '__main__':
    if not setup:
        vv = KjoretimeListener()
        vv.scheduler()
    while True:
        try:
            print(vv.current_classes)
        except AttributeError:
            
            print("not yet ready, waiting")
            sleep(2)
