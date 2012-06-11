#Copyright 2011-2012 Calxeda, In.  All Rights Reserved.

"""A series of wrappers around RMCP+ Payload commands"""

from pyipmi import Command, InteractiveCommand, IpmiError
from pyipmi.tools.responseparser import ResponseParserMixIn


class ActivatePayloadCommand(InteractiveCommand, ResponseParserMixIn):
    """Describes the Activate Payload command"""

    #TODO: there could be other payload types

    name = "Activate Payload"
    ipmitool_args = ["-I", "lanplus", "-C", "0", "sol", "activate"]


class DeactivatePayloadCommand(Command, ResponseParserMixIn):
    """Describes the Deactivate Payload command"""

    #TODO: there could be other payload types

    def handle_command_error(self, out, err):
        if err.find('Info: SOL payload already de-activated') > -1:
            return

        raise IpmiError(err)

    name = "Deactivate Payload"
    ipmitool_args = ["-I", "lanplus", "sol", "deactivate"]


payload_commands = {
    "activate_payload" : ActivatePayloadCommand,
    "deactivate_payload" : DeactivatePayloadCommand
}
