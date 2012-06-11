#Copyright 2012 Calxeda, Inc.  All Rights Reserved.

"""lan config related commands"""

from .. import Command
from pyipmi.lan import *
from pyipmi.tools.responseparser import (ResponseParserMixIn,
                                         str_to_list,
                                         str_to_dict)


class LANPrintCommand(Command, ResponseParserMixIn):
    """Describes the lan print ipmitool command
    """
    name = "LAN Print"
    result_type = LANPrintResults

    def parse_response(self, out, err):
        """ Strip out extraneous colons to allow more generic parsing
        """
        new_out_list = map(lambda x: x.lstrip(' \t\n:'), out.split('\n'))
        new_out = reduce(lambda x, y: x + '\n' + y, new_out_list)

        return self.response_parser(new_out, err)

    def first_word_only(line):
        y = line.split(' ')
        return y[0]

    response_fields = {
        'Set in Progress'       : {},
        'Auth Type Support'     : {'parser' : str_to_list},
        'Auth Type Enable'      : {'lines'  : 5,
                                   'parser' : str_to_dict,
                                   'operator' : ':',
                                   'delimiter' : '\n',
                                   'value_parser' : str_to_list},
        'IP Address Source'     : {},
        'IP Address'            : {},
        'Subnet Mask'           : {},
        'MAC Address'           : {},
        'SNMP Community String' : {},
        'IP Header'             : {'parser' : str_to_dict,
                                   'operator' : '=',
                                   'delimiter' : ' '},
        'BMC ARP Control'       : {'parser' : str_to_list,
                                   'delimiter' : ','},
        'Gratituous ARP Intrvl' : {'parser' : first_word_only},
        'Default Gateway IP'    : {},
        'Default Gateway MAC'   : {},
        'TFTP Server IP'        : {},
        'NTP Server IP'         : {},
        'NTP UDP port'          : {},
        'OEM MAC0'              : {},
        'OEM MAC1'              : {},
        'OEM MAC2'              : {},
        'OEM OUID'              : {},
        'Supercluster OUID'     : {},
        'Supercluster mode'     : {},
        'Supercluster FID'      : {},
        '802.1q VLAN ID'        : {},
        '802.1q VLAN Priority'  : {},
        'RMCP+ Cipher Suites'  : {'parser' : str_to_list,
                                   'delimiter' : ','},
        'Cipher Suite Priv Max' : {}
    }

    @property
    def ipmitool_args(self):
        channel = self._params.get('channel', '')
        return ["lan", "print", channel]


class LANSetCommand(Command, ResponseParserMixIn):
    """Describes the ipmitool lan set command
    """
    name = "LAN Set"
    result_type = LANSetResult

    response_fields = {
    }

    @property
    def ipmitool_args(self):
        command = "lan set %s %s" % (self._params['channel'], self._params['command'])
        command_array = command.split(' ')
        params = self._params['param']
        param_array = [params]
        if self._params['command'] == 'auth':
            param_array = params.split(' ')
        command_array.extend(param_array)
        return command_array


lan_commands = {
    'lan_print'             : LANPrintCommand,
    'lan_set'               : LANSetCommand
}
