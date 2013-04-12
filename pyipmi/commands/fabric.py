# Copyright (c) 2012, Calxeda Inc.
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
# * Neither the name of Calxeda Inc. nor the names of its contributors
# may be used to endorse or promote products derived from this software
# without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDERS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
# OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
# TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
# THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
# DAMAGE.


from .. import Command
from pyipmi.tools.responseparser import ResponseParserMixIn
from pyipmi.fabric import *
from pyipmi import IpmiError

class CommandWithErrors(Command, ResponseParserMixIn):

    def parse_response(self, out, err):
        """Parse the response to a command

        The 'ipmitool_response_format' attribute is used to determine
        what parser to use to for interpreting the results.

        Arguments:
        out -- the text response of an command from stdout
        err -- the text response of an command from stderr
        """

        out = out + err
        return self.response_parser(out, err)


class FabricGetIPInfoCommand(CommandWithErrors):
    """ Describes the cxoem fabric list_ip_addrs IPMI command
    """

    name = "Retrieve fabric IP info"
    result_type = FabricGetIPInfoResult

    response_fields = {
        'File Name' : {},
        'Error' : {}
    }

    @property
    def ipmitool_args(self):
        if self._params['tftp_addr'] != None:
            tftp_args = self._params['tftp_addr'].split(":")
            if len(tftp_args) == 1:
                return ["cxoem", "fabric", "config", "get", "ipinfo", "tftp",
                        tftp_args[0], "file", self._params['filename']]
            else:
                return ["cxoem", "fabric", "config", "get", "ipinfo", "tftp",
                        tftp_args[0], "port", tftp_args[1], "file",
                        self._params['filename']]
        else:
            return ["cxoem", "fabric", "config", "get", "ipinfo", "file",
                    self._params['filename']]

class FabricGetMACAddressesCommand(CommandWithErrors):
    """ Describes the cxoem fabric list_macs IPMI command
    """

    name = "Retrieve fabric MAC addresses"
    result_type = FabricGetMACAddressesResult

    response_fields = {
        'File Name' : {},
        'Error' : {}
    }

    @property
    def ipmitool_args(self):
        if self._params['tftp_addr'] != None:
            tftp_args = self._params['tftp_addr'].split(":")
            if len(tftp_args) == 1:
                return ["cxoem", "fabric", "config", "get", "macaddrs", "tftp",
                        tftp_args[0], "file", self._params['filename']]
            else:
                return ["cxoem", "fabric", "config", "get", "macaddrs", "tftp",
                        tftp_args[0], "port", tftp_args[1], "file",
                        self._params['filename']]
        else:
            return ["cxoem", "fabric", "config", "get", "macaddrs", "file",
                    self._params['filename']]

class FabricUpdateConfigCommand(Command, ResponseParserMixIn):
    """Describes the ipmitool fabric update config command"""
    name = "Update Config"
    result_type = FabricUpdateConfigResult

    response_fields = {
    }

    @property
    def ipmitool_args(self):
        return ["cxoem", "fabric", "update_config"]

class FabricGetNodeIDCommand(Command, ResponseParserMixIn):
    """Describes the ipmitool fabric get nodeid command"""
    name = "Get NodeID command"
    result_type = int

    def parse_response(self, out, err):
        if err:
            raise IpmiError(err)
        return int(out)

    response_fields = {
    }

    ipmitool_args = ["cxoem", "fabric", "get", "nodeid"]

class FabricGetIPAddrCommand(Command, ResponseParserMixIn):
    """Describes the ipmitool fabric get ipaddr command"""
    name = "Get ipaddr command"
    result_type = str

    def parse_response(self, out, err):
        return out.strip()

    response_fields = {
    }

    @property
    def ipmitool_args(self):
        result = ["cxoem", "fabric", "get", "ipaddr"]
        if self._params.get('nodeid', None):
            result.extend(['node', self._params['nodeid']])
        if self._params.get('iface', None):
            result.extend(['interface', self._params['iface']])
        return result

class FabricGetMacAddrCommand(Command, ResponseParserMixIn):
    """Describes the ipmitool fabric get macaddr command"""
    name = "Get macaddr command"
    result_type = str

    def parse_response(self, out, err):
        if err:
            raise IpmiError(err)
        return out.strip()

    response_fields = {
    }

    @property
    def ipmitool_args(self):
        result = ["cxoem", "fabric", "get", "macaddr", "interface",
                self._params['iface']]
        if self._params.get('nodeid', None):
            result.extend(['node', self._params['nodeid']])
        return result

class FabricGetIPSrcCommand(Command, ResponseParserMixIn):
    """Describes the ipmitool fabric get ipsrc command"""
    name = "Get ipsrc command"
    result_type = int

    def parse_response(self, out, err):
        return int(out)

    response_fields = {
    }

    @property
    def ipmitool_args(self):
        return ["cxoem", "fabric", "config", "get", "ipsrc"]

class FabricSetIPSrcCommand(Command, ResponseParserMixIn):
    """Describes the ipmitool fabric set ipsrc command"""
    name = "Set ipsrc command"

    @property
    def ipmitool_args(self):
        return ['cxoem',
                'fabric',
                'config',
                'set',
                'ipsrc',
                self._params['ipsrc_mode']]

fabric_commands = {
    "fabric_getipinfo"  : FabricGetIPInfoCommand,
    "fabric_getmacaddresses" : FabricGetMACAddressesCommand,
    "fabric_updateconfig"  :FabricUpdateConfigCommand,
    "fabric_getnodeid"  : FabricGetNodeIDCommand,
    "fabric_getipaddr" : FabricGetIPAddrCommand,
    "fabric_getmacaddr" : FabricGetMacAddrCommand,
    "fabric_getipsrc" : FabricGetIPSrcCommand,
    "fabric_setipsrc" : FabricSetIPSrcCommand
}
