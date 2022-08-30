from services import SocketService

try:
    socketService = SocketService()
except Exception as e:
    print(e)
    exit()

@socketService.emit()
def getReading() -> object:
    # Return a json serializable object

if __name__ == "__main__":
    pass