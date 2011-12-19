#Copyright 2011 Calxeda, Inc.  All Rights Reserved.

"""Helper objects for various SOL-related commands"""

import pexpect
from pyipmi import IpmiError

ESCAPE_SEQUENCES = {
    "IpmiTool" : {
        "terminate" : "~.",
        "list_escapes" : "~?",
        "escape_char" : "~~"
    }
}

TOOL_RESPONSES = {
    "IpmiTool" : {
        "open" : "[SOL Session operational.  Use ~? for help]",
        "close" : "[terminated ipmitool]"
    }
}

class SOLConsole(object):
    """Create and control an SOL session"""

    def __init__(self, bmc, hostname, username, password):
        self.isopen = False
        self._bmc = bmc
        self._toolname = bmc.handle._tool.__class__.__name__
        self.escapes = ESCAPE_SEQUENCES[self._toolname]
        self.responses = TOOL_RESPONSES[self._toolname]

        # save authenication info
        self._auth_info = {
            'hostname' : hostname,
            'username' : username,
            'password' : password
        }

        # activate SOL session
        self._proc = self._bmc.activate_payload()
        self.expect_exact(self.responses['open'])

        # set up log files
        self._proc.logfile_read = file('sol_read.log', 'w')
        self._proc.logfile_send = file('sol_write.log', 'w')

        try:
            self._login()
        except IpmiError:
            self.close()
            raise

        self.isopen = True

    def __del__(self):
        if self.isopen:
            self.close()
        self._bmc = None

    def close(self):
        self._logout()
        self.sendline(self.escapes['terminate'])
        try:
            self.expect_exact(self.responses['close'], timeout=2)
        except pexpect.TIMEOUT, pexpect.EOF:
            self._bmc.deactivate_payload()

        if self._proc.isalive():
            self._proc.close()

        self.isopen = False

    def _login(self):
        hostname = self._auth_info['hostname']
        username = self._auth_info['username']
        password = self._auth_info['password']

        self.prompt = '%s@%s.*[$#] ' % (username, hostname)
        self.login_prompt = hostname + ' login: '

        # once we've activated a session, either we're logged in,
        # we need to log in, or we're not getting any data back
        login_patterns = [self.login_prompt, self.prompt,
                          pexpect.TIMEOUT, pexpect.EOF]
        self.sendline()
        index = self.expect(login_patterns)

        # if we haven't found a prompt (index > 1),
        # try sending various control characters
        # control characters to send
        controls = ['\\', 'c', 'd']
        while index > 1:
            try:
                self.sendcontrol(controls.pop())
                index = self.expect(login_patterns)
            except IndexError:
                raise IpmiError('SOL session unresponsive')

        if index == 0:
            # need to log in
            try:
                self.sendline(username)
                self.expect_exact('Password: ')
                self.sendline(password)
                self.expect(self.prompt)
            except pexpect.TIMEOUT:
                raise #IpmiError('%s@%s: failed login' % (username, hostname))
        elif index == 1:
            # we're already logged in
            pass

        # make the prompt more predictable
        self.sendline('export PS1="\u@\h:~\$ "')
        self.expect(self.prompt)

    def _logout(self):
        self.sendcontrol('c')
        self.sendline('logout')
        return self.expect([self.login_prompt, pexpect.TIMEOUT]) == 0

    ######################################
    #                                    #
    # Wrappers for pexpect functionality #
    #                                    #
    ######################################

    def expect(self, pattern, timeout=-1, searchwindowsize=None):
        return self._proc.expect(pattern, timeout, searchwindowsize)

    def expect_exact(self, pattern, timeout=-1, searchwindowsize=None):
        return self._proc.expect_exact(pattern, timeout, searchwindowsize)

    def read(self, size=-1):
        # pexpect implements this function by expecting the delimiter
        # the default delimiter is EOF, which for our purposes, is
        # unlikely to be reached. So instead, use pexpect.TIMEOUT
        # as the delimiter for now
        prev_delimiter = self._proc.delimiter
        self._proc.delimiter = pexpect.TIMEOUT
        data = self._proc.read(size)
        self._proc.delimiter = prev_delimiter
        return data

    def readline(self, size=-1):
        return self._proc.readline(size)

    def send(self, s):
        return self._proc.send(s)

    def sendline(self, s=""):
        return self._proc.sendline(s)

    def sendcontrol(self, char):
        return self._proc.sendcontrol(char)


# map config params to range of possible values
SOL_CONFIGURATION_PARAMETERS = {
    "set_in_progress" : ["set_in_progress", "set_complete", "commit_write"],
    "enable" : [True, False],
    "force_encryption" : [True, False],
    "force_authentication" : [True, False],
    "privilege_level" : ["USER", "OPERATOR", "ADMINISTRATOR", "OEM"],
    "character_accumulate_interval" : range(1, 256),
    "character_send_threshold" : range(256),
    "retry_count" : range(8),
    "retry_interval" : range(256),
    "volatile_bit_rate" : [9.6, 19.2, 38.4, 57.6, 115.2], #TODO: "serial"
    "non_volatile_bit_rate" : [9.6, 19.2, 38.4, 57.6, 115.2], #TODO: "serial"
    "payload_channel" : [], # implementation specific
    "payload_port_number" : [], # implementation specific
    # TODO: support OEM parameters
}

# map tools to a list of unsettable params for that tool
TOOL_RESTRICTIONS = {
    "IpmiTool": ["payload_channel", "payload_port_number"],
}
