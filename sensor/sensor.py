from services import SocketService

try:
    socketService = SocketService()
except Exception as e:
    print(e)
    exit()

@socketService.emit()
def getReading() -> object:
    #TODO: Functionality
    
    # Important!!! Return a json serializable object
    pass

if __name__ == "__main__":
    pass