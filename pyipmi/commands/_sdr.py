#Copyright 2011 Calxeda, Inc.  All Rights Reserved.
"""SDR related commands"""
import re

from .. import Command
from .. sdr import Sdr, AnalogSdr
from .. tools.ipmitool import IpmitoolCommandMixIn

PAREN_PAIR_VAL = 'CHANGE ME' # FIXME: change

class SdrListCommand(Command, IpmitoolCommandMixIn):
    """Describes the sdr list command

    This is not a single IPMI request type - it's an ipmitool
    command that's composed of multiple IPMI requests.
    """

    name = 'SDR List'
    result_type = Sdr

    ipmitool_response_format = IpmitoolCommandMixIn.COLUMN_RECORD_LIST
    ipmitool_args = ['-v', 'sdr', 'list', 'all']

    def ipmitool_types(self, record):
        """Only matches Analog sensors right now.

           There are several more types of records to match, if they
           are needed.
        """
        if re.search('Sensor Type \(Analog\)', record):
            return AnalogSdr, self.analog_response_fields
        else:
            return None, None

    analog_response_fields = {
        """
        Unparsed fields for analog sensors:

         Readable Thresholds   : lnr lcr lnc unc ucr unr 
         Settable Thresholds   : lnr lcr lnc unc ucr unr 
         Threshold Read Mask   : lnr lcr lnc unc ucr unr 
         Assertion Events      : 
         Assertions Enabled    : unc+ ucr+ unr+ 
         Deassertions Enabled  : unc+ ucr+ unr+ 
        """
        'Sensor ID' : {
            'attr' : ('sensor_name', 'sensor_id'),
            'parser' : PAREN_PAIR_VAL
        },
        'Entity ID' : {
            'attr' : ('entity_id', 'entity_name'),
            'parser' : PAREN_PAIR_VAL
        },
        'Sensor Type (Analog)'  : { 'attr' : 'sensor_type' },
        'Sensor Reading'        : {},
        'Status'                : {},
        'Nominal Reading'       : {},
        'Normal Minimum'        : {},
        'Normal Maximum'        : {},
        'Upper non-recoverable' : {},
        'Upper critical'        : {},
        'Upper non-critical'    : {},
        'Lower non-recoverable' : {},
        'Lower critical'        : {},
        'Lower non-critical'    : {},
        'Positive Hysteresis'   : {},
        'Negative Hysteresis'   : {},
        'Minimum sensor range'  : {},
        'Maximum sensor range'  : {},
        'Event Message Control' : {},
    }

sdr_commands = {
    "get_sdr_list" : SdrListCommand
}
