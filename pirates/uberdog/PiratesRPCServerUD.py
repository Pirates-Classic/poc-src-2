import traceback
import json
import sys

from direct.directnotify.DirectNotifyGlobal import *
from direct.task import Task
from direct.stdpy.threading2 import Thread

from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler


class PiratesRPCHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/PRPC2',)

class PiratesRPCServerUD(Thread):
    notify = directNotify.newCategory('PiratesRPCServerUD')
    notify.setInfo(True)

    def __init__(self, air):
        Thread.__init__(self)

        self.air = air
        self.hostname = config.GetString('rpc-hostname', '127.0.0.1')
        self.port = config.GetInt('rpc-port', 6484)
        self.running = True
        self.server = SimpleXMLRPCServer((self.hostname, self.port),
            logRequests=False, requestHandler=PiratesRPCHandler)

        self.server.register_introspection_functions()
        self.registerCommands()

    def registerFunction(self, function, name=None):
        self.server.register_function(function, name)

    def run(self):
        self.notify.info('Starting RPC server at %s:%d' % (self.hostname, self.port))
        self.server.serve_forever(poll_interval=0.001)

    def shutdown(self):
        self.server.shutdown()
        self.server.server_close()

    def registerCommands(self):
        self.registerFunction(self.ping)
        self.registerFunction(self.systemMessage)
        self.registerFunction(self.systemMessageChannel)
        self.registerFunction(self.kickChannel)
        self.registerFunction(self.getDistricts)
        self.registerFunction(self.getHolidays)
        self.registerFunction(self.startHoliday)
        self.registerFunction(self.stopHoliday)

    def formatCallback(self, code=200, message='Success', **kwargs):
        response = {'code': code, 'message': message}
        for keyword in kwargs:
            response[keyword] = kwargs[keyword]

        return json.dumps(response)

    def ping(self, response):
        """
        Summary:
            Responds with the [data] that was sent. This method exists only for
            testing purposes.

        Parameters:
            [any data] = The data to be given back in response.

        Example response: 'pong'
        """

        return self.formatCallback(response=response)

    def systemMessage(self, message):
        """
        Summary:
            Broadcasts a [message] to the entire server globally.

        Parameters:
            [str message] = The message to broadcast.
        """

        self.air.systemMessage(message)
        return self.formatCallback()

    def systemMessageChannel(self, message, channel):
        """
        Summary:
            Broadcasts a [message] to any client whose Client Agent is
            subscribed to the provided [channel].

        Parameters:
            [int channel] = The channel to direct the message to.
            [str message] = The message to broadcast.
        """

        self.air.systemMessage(message, channel)
        return self.formatCallback()

    def kickChannel(self, channel, reason=1, message=''):
        """
        Summary:
            Kicks any users whose CAs are subscribed to a particular [channel] with a [code].

        Parameters:
            [int channel] = The channel to direct the message to.
            [int code] = An optional code to kick.
            [string reason] = An optional reason.
        """

        try:
            self.air.kickChannel(channel, reason, message)
        except Exception as e:
            return self.formatCallback(code=100, message='Failed to kick channel, '
                'An unexpected error occured', error=repr(e))

        return self.formatCallback()

    def getDistricts(self):
        """
        Summary:
            Retrieves the last reported status of all the districts in the server cluster
        Returns:
            districts: List containing all districts
        """

        districts = self.air.districtTracker.getShards()
        return self.formatCallback(districts=districts)

    def getHolidays(self):
        """
        Summary:
            Retrieves a list of all holidays happening on the cluster
        Returns:
            holidays: List containing all unique holidays
        """

        districts = self.air.districtTracker.getShards()
        holidays = []
        for district in districts:
            holidays += district['holidays']

        return self.formatCallback(holidays=str(set(holidays)))

    def startHoliday(self, holidayId, time, announce=False):
        """
        Summary:
            Tells all NewsManagers in the cluster to start a specific holiday id for a
            set amount of time.
        Parameters:
            [int holidayId] = The holiday id to start
            [int time] = The time in seconds for the holiday to run
            [bool announce] = Broadcasts to Discord that the holiday started
        """

        self.air.newsManager.startHoliday(int(holidayId), int(time), quietly=not announce)
        return self.formatCallback()

    def stopHoliday(self, holidayId):
        """
        Summary:
            Tells all NewsManagers in the cluster to stop a specific holiday id.
        Parameters:
            [int holidayId] = The holiday id to stop
        """

        self.air.newsManager.stopHoliday(int(holidayId))
        return self.formatCallback()
