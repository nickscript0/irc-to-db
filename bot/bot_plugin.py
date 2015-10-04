# -*- coding: utf-8 -*-
from irc3.plugins.command import command
import irc3
from influxdb import InfluxDBClient


class DBClient:

    def __init__(self):
        self.client = InfluxDBClient(
            'influxdb', 8086, 'root', 'root', 'db1')

    def write(self, channel, event, message, full_user):
        self._write(channel, event, message, full_user)
        self._writeAllTags(channel, event, message, full_user)

    def _write(self, channel, event, message, full_user):
        json_body = [
            {
                "measurement": "irc",
                "tags": {
                    "channel": channel,
                    "event": event,
                    "user_address": full_user,
                    "user": self._parseUser(full_user)
                },
                "fields": {
                    "value": message
                }
            }
        ]
        self.client.write_points(json_body)

    def _writeAllTags(self, channel, event, message, full_user):
        json_body = [
            {
                "measurement": "irc_tag",
                "tags": {
                    "channel": channel,
                    "event": event,
                    "user_address": full_user,
                    "user": self._parseUser(full_user),
                    "msg": message
                },
                "fields": {
                    "value": self._parseUser(full_user)
                }
            }
        ]
        self.client.write_points(json_body)

    @classmethod
    def _parseUser(cls, full_user):
        """ Parse full user address of the form username!username@username.prefix.server.tld """
        return full_user.split('!')[0]


@irc3.plugin
class Plugin(object):

    def __init__(self, bot):
        self.bot = bot
        self.db = DBClient()

    @irc3.event(irc3.rfc.PRIVMSG)
    def msg(self, *args, **kwargs):
        """
        This callback receives the following arguments:
        args=(), kwargs={'target': channel, 'data': chat_msg, 'event': 'PRIVMSG', 'mask': 'username!username@username.prefix.server.tld'}
        """
        channel = kwargs.get('target')
        message = kwargs.get('data')
        event = kwargs.get('event')
        full_user = kwargs.get('mask')
        self.db.write(channel, event, message, full_user)

        #print("args={}, kwargs={}".format(args, kwargs))
