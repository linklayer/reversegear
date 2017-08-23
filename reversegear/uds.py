import pprint
from pyvit.hw.logplayer import LogPlayer
from pyvit.dispatch import Dispatcher
from pyvit.proto.isotp import IsotpInterface
from pyvit.proto.uds import *

class UDSDecoder:
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
                session.append(req)

                resp = None
                # wait until we get a response
                # this will return None if there is a response pending
                while resp is None:
                    resp = uds_resp.decode_response()
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
                    print('\t%s: %s' % (k, pprint.pformat(r[k], indent=8,
                                                        compact=True)))
            elif isinstance(r, GenericResponse):
                print('[<-] Response [%s / 0x%X]' % (r.name, r.SID))
                for k in r.keys():
                    print('\t%s: %s' % (k, pprint.pformat(r[k], indent=8,
                                                        compact=True)))

            elif isinstance(r, NegativeResponseException):
                print('\n[!!] %s' % r)
            elif r is None:
                print('Unknown Service')
