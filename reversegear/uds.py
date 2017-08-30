import string
from pyvit.hw.logplayer import LogPlayer
from pyvit.dispatch import Dispatcher
from pyvit.proto.isotp import IsotpInterface
from pyvit.proto.uds import *


class UDSDecoder:
    def __init__(self, debug=False):
        self.debug = debug

    def read_file(self, filename, tx_id, rx_id):
        lp = LogPlayer(filename, realtime=False)
        disp = Dispatcher(lp)
        uds_req = UDSInterface(disp, 0, tx_id)
        uds_resp = UDSInterface(disp, 0, rx_id)
        disp.start()

        session = []

        while True:
            try:
                req = uds_req.decode_request()
                if req is None:
                    break

                if self.debug:
                    print(req)
                session.append(req)

                resp = None
                # wait until we get a response
                # this will return None if there is a response pending
                tries = 0
                while resp is None and tries < 5:
                    resp = uds_resp.decode_response()
                    tries = tries + 1

                if self.debug:
                    print(resp)
                session.append(resp)

            except NegativeResponseException as e:
                session.append(e)

        disp.stop()
        return session

    def generate_output(self, session):
        for r in session:
            if isinstance(r, GenericRequest):
                print('\n[->] Request [%s / 0x%X]' % (r.name, r.SID))
                for k in r.keys():
                    print('%s: ' % k, end='')
                    print(self.format_data(r[k]))
                print('')

            elif isinstance(r, GenericResponse):
                print('[<-] Response [%s / 0x%X]' % (r.name, r.SID))
                for k in r.keys():
                    print('%s: ' % k, end='')
                    print(self.format_data(r[k]))
                print('')

            elif isinstance(r, NegativeResponseException):
                print('\n[!!] %s' % r)

            elif r is None:
                print('Unknown Service')

    def format_data(self, data, line_len=8):
        result = ''
        if isinstance(data, int):
            result = '0x%X' % data
        elif isinstance(data, list):
            result += '\n'
            for addr in range(0, len(data), line_len):
                # add the address
                result += '%03X: ' % addr

                # add line of data as hex
                for b in data[addr:addr+line_len]:
                    result += '%02X ' % b

                # if this is the last line, pad it
                if int(addr / 8) == int(len(data) / line_len):
                    for _ in range(0, line_len - (len(data) % line_len)):
                        result += '   '

                result += '\t\t'

                # add line of data as ascii
                for b in data[addr:addr+line_len]:
                    if chr(b) in string.printable and b >= 32 and b < 0x7F:
                        result += chr(b)
                    else:
                        result += '.'

                result += '\n'
        return result
