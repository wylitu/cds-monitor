# coding: utf-8
__author__ = 'wylitu'
import ConfigParser
from ipUtil import  IpUtil
class ConfigUtil :

    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read('../config/agent.cfg')

    def setEvents(self,events):
        if events == None:
            return
        monitorId = ''
        eventId = ''
        for event in events:
             monitorId.__add__(event.getMonitorId()).__add__(',')
             eventId.__add__(event.getEventId()).__add__(',')

        self.config.set('events', 'eventId',eventId[-1:])
        self.config.set('events', 'monitorId',monitorId[-1:])
        self.config.write(open('../config/agent.cfg', 'w'))

    def getEventId(self,monitorId=''):
        if monitorId == None:
            return None
        monitorIds =  self.config.get('events', 'monitorId').split(',')
        eventIds =  self.config.get('events', 'eventId').split(',')
        i=0
        for id in monitorIds:
             if id == monitorId:
                 return eventIds[i]
             i = i+1
        return None

    def set_host_ip(self,ip):
        if ip == None:
            return None
        self.config.set('monitorHost', 'host',ip)
        self.config.write(open('../config/agent.cfg', 'w'))
        return None

    def get_host_ip(self):
        ip = self.config.get('monitorHost', 'host')
        if ip == '':
            ip = IpUtil().get_local_ip()
            self.set_host_ip(ip)
        return ip

    def init_host_ip(self):
        ip = IpUtil().get_local_ip()
        self.set_host_ip(ip)

if __name__ == '__main__':
    print ConfigUtil().get_host_ip()
