import argparse

from .uds import UDSDecoder

__version__ = '0.0.1'


def auto_int(x):
    return int(x, 0)


def main():
    parser = argparse.ArgumentParser(
        description='Offline reverse engineering tools for automotive'
        'networks.')
    parser.add_argument('--debug', action='store_true',
                        help='enable debug output')

    subparsers = parser.add_subparsers(title='subcommand',
                                       help='additional help')
    uds_parser = subparsers.add_parser('uds')
    uds_parser.add_argument('tx_id', type=auto_int,
                            help='CAN arbitration ID transmitted'
                            'by the scan tool')
    uds_parser.add_argument('rx_id', type=auto_int,
                            help='CAN arbitration ID received'
                            'by the scan tool')
    uds_parser.add_argument('inputs', nargs='+')
    uds_parser.set_defaults(func=uds_func)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


def uds_func(args):
    decoder = UDSDecoder(debug=args.debug)
    for f in args.inputs:
        session = decoder.read_file(f, args.tx_id, args.rx_id)
        decoder.generate_output(session)
