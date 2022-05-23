from PyQt6 import QtCore

class AsyncVKAPI(QtCore.QRunnable):
    def __init__(self, vkapi, method, **kwargs):
        super(AsyncVKAPI, self).__init__()
        self.signals = AsyncVKAPISignals()
        self.vkapi = vkapi
        self.method = method
        self.kwargs = kwargs

    def run(self):
        if '_returnData' in self.kwargs:
            self._returnData = self.kwargs['_returnData']
            del self.kwargs['_returnData']
         
        if self.method == 'getHistory':
            result = getattr(self.vkapi, self.method)(**self.kwargs)
            self.signals.getHistory.emit(result, *self._returnData)
        else:
            result = getattr(self.vkapi, self.method)(**self.kwargs)
            self.signals.getChats.emit(result)
            

class AsyncVKAPISignals(QtCore.QObject):
    getChats = QtCore.pyqtSignal(object)
    getHistory = QtCore.pyqtSignal(object, object, object, object)