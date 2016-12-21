from argparse import ArgumentParser, Action
import logging
from orange_datashare.command_line_client import load_client

_logger = logging.getLogger(__name__)


class StorePositional(Action):
    ORDER_ARGS_ATTRIBUTE_NAME = 'ordered_args'

    def __call__(self, _, namespace, values, option_string=None):
        if ('%s' % StorePositional.ORDER_ARGS_ATTRIBUTE_NAME) not in namespace:
            setattr(namespace, StorePositional.ORDER_ARGS_ATTRIBUTE_NAME, [])
        previous = namespace.ordered_args
        previous.append((self.dest, values))
        setattr(namespace, StorePositional.ORDER_ARGS_ATTRIBUTE_NAME, previous)


def main():
    parser = ArgumentParser(add_help=True)
    parser.add_argument('--verbose', action='store_true', dest='verbose', default=False,
                        help='Set default log to DEBUG')
    commands = parser.add_subparsers(help='commands', dest='action')

    commands.add_parser('list_subscriptions', help='List subscriptions')
    sub_parser = commands.add_parser('get_subscription', help='Get subscription')
    sub_parser.add_argument('subscription_key', action=StorePositional, type=str, help='Subscription key')

    arguments = parser.parse_args()

    if arguments.verbose:
        logging.basicConfig(level=logging.DEBUG, format='%(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='%(message)s')
    command_mapper = dict()
    command_mapper["list_subscriptions"] = lambda c: c.subscription.list_subscriptions("me")
    command_mapper["get_subscription"] = lambda c: c.subscription.get_subscription("me", arguments.subscription_key)

    with load_client() as client:
        try:
            result = command_mapper[arguments.action](client)
            if result is not None:
                _logger.info(result)
        except KeyError:
            _logger.error('\'%s\': not implemented')
