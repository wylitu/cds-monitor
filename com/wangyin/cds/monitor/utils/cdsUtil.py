# coding: utf-8
__author__ = 'wylitu'
import requests
import json
from com.wangyin.cds.monitor.model.dbMonitorInstance import DbMonitorInstance
from com.wangyin.cds.monitor.model.dbInfo import DbConfig,DbUnit
from com.wangyin.cds.monitor.model.dbMonitor import DbMonitorConfig
from com.wangyin.cds.monitor.model.monitorTaskEvent import MonitorTaskEvent
import urllib
import urllib2
import datetime,time
import ConfigParser
from configUtil import ConfigUtil

class CDSUtil:

    config = ConfigParser.ConfigParser()
    config.read('../config/agent.cfg')
    serverIp = config.get('cdsServer','host')
    serverPort = config.get('cdsServer','port')
    monitorHostIp = ConfigUtil().get_host_ip()

    @staticmethod
    def getEvents(cls):
        url = URLS.MONITOR_TASK_ENVENT.format(cls.serverIp,cls.serverPort,cls.monitorHostIp)
        print url
        try:
            r = requests.get(url)
        except Exception as e:
            print(e)
            return None
        print r
        retInfo = json.loads(r.text)
        errorCode = retInfo['errorCode']
        if errorCode != 0:
            print(retInfo['errMsg'])
            return None
        retEvents = []
        events = retInfo['resultInfo']
        print retInfo['resultInfo']
        if len(events) != 0:
            for event in events:
                dbinfo = DbConfig(event['dbInfoId'],event['dbMonitorGroupId'], event['ip'], event['port'],event['dbType'])
                monitorId = event['dbMonitorId']
                eventId = event['eventId']
                eventType = event['eventType']
                event = MonitorTaskEvent(eventId,eventType,monitorId,dbinfo)
                retEvents.append(event)
        return retEvents
    @staticmethod
    def getDbConfigsByIp(ip):
        URL = URLS.GET_DB_CONFIG_BY_IP.format(ip)
        r = requests.get(URL)
        dbinfos = json.loads(r.text)
        retDbinfos = []
        if len(dbinfos) != 0:
            for dbinfo in dbinfos:
                dbinfo = DbConfig(dbinfo['groupId'], dbinfo['ip'], dbinfo['port'],dbinfo['dbName'],dbinfo['masterOrSlave'],dbinfo['dbType'],dbinfo['dbStatus'])
                retDbinfos.append(dbinfo)
        return retDbinfos

    @staticmethod    
    def getDbConfigByType(type,gropuId):
        URL = URLS.GET_DB_CONFIG.format(type,gropuId)
        r = requests.get(URL)
        dbinfos = json.loads(r.text)
        retDbinfos = []
        if len(dbinfos) != 0:
            for dbinfo in dbinfos:
                dbinfo = DbConfig(dbinfo['groupId'], dbinfo['ip'], dbinfo['port'],dbinfo['dbName'],dbinfo['masterOrSlave'],dbinfo['dbType'],dbinfo['dbStatus'])
                retDbinfos.append(dbinfo)
        return retDbinfos
    
    @staticmethod
    def getDbMonitorConfigByDbGroupId(groupId):
        URL = URLS.GET_MONITOR_CONFIG_BY_GROUPID.format(groupId)
        r = requests.get(URL)
        dbMonitors = json.loads(r.text)
        dbMonitorConfigs = []
        if len(dbMonitors) != 0:
            for dbMonitor in dbMonitors:
                dbMonitorConfig = DbMonitorConfig(dbMonitor['dbGroupId'],dbMonitor['monitorItem'],dbMonitor['monitorItemName'],dbMonitor['errorNumUpper'],dbMonitor['checkInterval'])
                dbMonitorConfigs.append(dbMonitorConfig)
        return dbMonitorConfigs

    @staticmethod
    def getDbMonitorConfigByDbMonitorId(cls,monitorId):
        URL = URLS.GET_MONITOR_CONFIG_BY_MONITORID.format(cls.serverIp,cls.serverPort,monitorId)
        r = requests.get(URL)
        retInfo = json.loads(r.text)
        errorCode = retInfo['errorCode']
        if errorCode != 0:
            print(retInfo['errMsg'])
            return None
        dbMonitor = retInfo['resultInfo']
        dbMonitorConfig = None
        print dbMonitor
        if dbMonitor != None:
            dbMonitorConfig = DbMonitorConfig(dbMonitor['id'],dbMonitor['dbMonitorGroupId'],dbMonitor['monitorItem'],dbMonitor['checkTimes'],dbMonitor['errorNumUpper'],
                                                  dbMonitor['checkInterval'],dbMonitor['monitorScriptType'],dbMonitor['monitorScriptPath'])
        return dbMonitorConfig

    @staticmethod
    def get_db_unit(cls,ip,db_type):
        URL = URLS.GET_DB_UNIT.format(cls.serverIp,cls.serverPort,ip,db_type)
        r = requests.get(URL)
        retInfo = json.loads(r.text)
        errorCode = retInfo['errorCode']
        if errorCode != 0:
            print(retInfo['errMsg'])
            return None
        db_units = retInfo['resultInfo']
        print db_units
        dbUnits = []
        if len(db_units) != 0:
            for db_unit in db_units:
                db_unit = DbUnit(db_unit['ip'],db_unit['port'],db_unit['dbName'],'root',db_unit['passwd'],db_unit['masterOrSlave'],db_unit['dbType'])
                dbUnits.append(db_unit)
        return dbUnits
    
    @staticmethod
    def monitorInstanceFormat(monitorInstance):
        monitorIns =  {}
        monitorIns['dbMinitorId']= monitorInstance.db_monitor_id
        monitorIns['monitorItem'] = monitorInstance.monitor_item
        monitorIns['dbInfoId'] = monitorInstance.db_info_id
        monitorIns['creationDate'] = monitorInstance.creation_date
        monitorIns['errorNum'] = monitorInstance.error_num
        monitorIns['alarmMsg'] = monitorInstance.alarm_msg
        monitorIns['monitorValue'] = monitorInstance.monitor_value
        print monitorIns
        return monitorIns

    @staticmethod
    def sendMonitorInstance(cls,monitorIns):
        monitorIns = cls.monitorInstanceFormat(monitorIns)
        print 'send monitorInsance to cds server...'
        values = json.dumps(monitorIns)
        print values
        headers={'Content-Type': 'application/json'}
        url = URLS.COLLECT_MONITOR_RESULT.format(cls.serverIp,cls.serverPort)
        r = requests.post(url, data=values, headers=headers)
        retInfo = json.loads(r.text)
        print(retInfo)
        if retInfo['errorCode'] !=0:
            print retInfo['errMsg']

class URLS:
    MONITOR_TASK_ENVENT = 'http://{0}:{1}/rest/events/ip/{2}'
    GET_DB_CONFIG = 'http://{0}:{1}/rest/dbinfo/type/{2}/dbGroupId/{3}'
    GET_DB_CONFIG_BY_IP = 'http://{0}:{1}/rest/dbInfo/ip/{2}'
    GET_MONITOR_CONFIG_BY_GROUPID = 'http://{0}:{1}/rest/dbmonitor/dbGroupId/{2}'
    GET_MONITOR_CONFIG_BY_MONITORID = 'http://{0}:{1}/rest/monitor/monitorId/{2}'
    GET_DB_UNIT = 'http://{0}:{1}/rest/dbinfo/dbunits/{2}/dbtype/{3}'
    COLLECT_MONITOR_RESULT = 'http://{0}:{1}/rest/monitor/collectMonitorResult/json'

if __name__ == '__main__':
    #print(CDSUtil.getDbMonitorConfigByDbMonitorId(CDSUtil,1))
    #print( CDSUtil.getEvents(CDSUtil))
    print(CDSUtil.sendMonitorInstance(CDSUtil,DbMonitorInstance('1','1','dbhang_check',int(time.time()),'2', '','db connect error')))
