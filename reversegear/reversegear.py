import argparse

from .uds import UDSDecoder
from .ids import IDStats

__version__ = '0.1.0'


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

    ids_parser = subparsers.add_parser('ids')
    ids_parser.add_argument('inputs', nargs='+')
    ids_parser.set_defaults(func=ids_func)

    iddiff_parser = subparsers.add_parser('iddiff')
    iddiff_parser.add_argument('a')
    iddiff_parser.add_argument('b')
    iddiff_parser.set_defaults(func=iddiff_func)

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


def ids_func(args):
    stats = IDStats()
    for f in args.inputs:
        frames = stats.read_file(f)
        stats.generate_output(frames)


def iddiff_func(args):
    stats = IDStats()
    ids_a = stats.unique_ids(stats.read_file(args.a))
    ids_b = stats.unique_ids(stats.read_file(args.b))

    print('Unique to %s:' % args.a)
    for arb_id in [i for i in ids_a if i not in ids_b]:
        print(arb_id)

    print('')

    print('Unique to %s:' % args.b)
    for arb_id in [i for i in ids_b if i not in ids_a]:
        print(arb_id)
