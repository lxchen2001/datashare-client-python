import logging
import json
from argparse import ArgumentParser, Action

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

    # Connections
    commands.add_parser('list_connections', help='List connections')
    sub_parser = commands.add_parser('get_connection', help='Get connection')
    sub_parser.add_argument('connection_id', action=StorePositional, type=str, help='Connection id')
    sub_parser = commands.add_parser('create_connection', help='Create connection')
    sub_parser.add_argument('connector_name', action=StorePositional, type=str, help='Connector name')
    sub_parser.add_argument('connection_key', action=StorePositional, type=str, help='Connection key')
    sub_parser = commands.add_parser('update_connection_status', help='Update connection status')
    sub_parser.add_argument('connection_id', action=StorePositional, type=str, help='Connection id')
    sub_parser.add_argument('status', action=StorePositional, type=str, help='Status')
    sub_parser.add_argument('reason', action=StorePositional, type=str, help='Reason')
    sub_parser = commands.add_parser('delete_connection', help='Delete connection')
    sub_parser.add_argument('connection_id', action=StorePositional, type=str, help='Connection id')

    # Devices
    sub_parser = commands.add_parser('list_devices', help='List devices of a connection')
    sub_parser.add_argument('connection_id', action=StorePositional, type=str, help='Connection id')
    sub_parser = commands.add_parser('get_device', help='Get a device of a connection')
    sub_parser.add_argument('connection_id', action=StorePositional, type=str, help='Connection id')
    sub_parser.add_argument('device_id', action=StorePositional, type=str, help='Device id')
    sub_parser = commands.add_parser('set_devices', help='Set the devices of a connection')
    sub_parser.add_argument('connection_id', action=StorePositional, type=str, help='Connection id')
    sub_parser.add_argument('devices', action=StorePositional, type=str, help='The json representation of the devices')
    sub_parser = commands.add_parser('update_devices', help='Update the devices of a connection (merge with existing)')
    sub_parser.add_argument('connection_id', action=StorePositional, type=str, help='Connection id')
    sub_parser.add_argument('devices', action=StorePositional, type=str, help='The json representation of the devices')


    # Subscriptions
    commands.add_parser('list_subscriptions', help='List subscriptions')
    sub_parser = commands.add_parser('get_subscription', help='Get subscription')
    sub_parser.add_argument('subscription_key', action=StorePositional, type=str, help='Subscription key')

    arguments = parser.parse_args()

    if arguments.verbose:
        logging.basicConfig(level=logging.DEBUG, format='%(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='%(message)s')
    command_mapper = dict()
    for name, value in getattr(arguments, StorePositional.ORDER_ARGS_ATTRIBUTE_NAME, []):
        setattr(arguments, name, value)
    # Connections
    command_mapper["list_connections"] = lambda c: c.connection.list_connections("me")
    command_mapper["get_connection"] = lambda c: c.connection.get_connection("me", arguments.connection_id)
    command_mapper["create_connection"] = lambda c: c.connection.create_connection("me",
                                                                                   arguments.connector_name,
                                                                                   arguments.connection_key)
    command_mapper["update_connection_status"] = lambda c: \
        c.connection.update_connection_status("me",
                                              arguments.connection_id,
                                              arguments.status,
                                              arguments.reason)
    command_mapper["delete_connection"] = lambda c: c.connection.delete_connection("me", arguments.connection_id)

    # Devices
    command_mapper["list_devices"] = lambda c: c.device.list_devices("me", arguments.connection_id)
    command_mapper["get_device"] = lambda c: c.device.get_device("me", arguments.connection_id, arguments.device_id)
    command_mapper["set_devices"] = lambda c: c.device.set_connection_devices("me",
                                                                              arguments.connection_id,
                                                                              json.loads(arguments.devices))
    command_mapper["update_devices"] = lambda c: c.device.update_connection_devices("me",
                                                                                    arguments.connection_id,
                                                                                    json.loads(arguments.devices))

    # Subscriptions
    command_mapper["list_subscriptions"] = lambda c: c.subscription.list_subscriptions("me")
    command_mapper["get_subscription"] = lambda c: c.subscription.get_subscription("me", arguments.subscription_key)

    with load_client() as client:
        if arguments.action is not None:
            try:
                result = command_mapper[arguments.action](client)
                if result is not None:
                    _logger.info(result)
            except KeyError:
                _logger.error('\'%s\': not implemented', arguments.action)
        else:
            parser.print_help()


if __name__ == '__main__':
    main()
