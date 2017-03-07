"""
Copyright (C) 2016-2017 Orange
This software is distributed under the terms and conditions of the 'BSD 3'
license which can be found in the file 'LICENSE' in this package distribution
"""
import json
import logging
from argparse import ArgumentParser, Action

from orange_datashare import __version__
from orange_datashare.command import ThermostatMode
from orange_datashare.command_line_client import load_client
from orange_datashare.data import StatsField
from orange_datashare.subscription import Origin

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
    parser.add_argument('-t', '--target', action='store', dest='target', default='https://datashare.orange.com',
                        help='Set server target. Default production: https://datashare.orange.com')
    parser.add_argument('-v', '--verbose', action='store_true', dest='verbose', default=False,
                        help='Set default log to DEBUG')
    parser.add_argument('-V', '--version', action='version', version=__version__)
    commands = parser.add_subparsers(help='commands', dest='action')

    # Connections
    commands.add_parser('list_connections', help='List connections')
    sub_parser = commands.add_parser('get_connection', help='Get connection')
    sub_parser.add_argument('connection_id', action=StorePositional, type=int, help='Connection id')
    sub_parser = commands.add_parser('create_connection', help='Create connection')
    sub_parser.add_argument('connector_name', action=StorePositional, type=str, help='Connector name')
    sub_parser.add_argument('connection_key', action=StorePositional, type=str, help='Connection key')
    sub_parser = commands.add_parser('update_connection_status', help='Update connection status')
    sub_parser.add_argument('connection_id', action=StorePositional, type=int, help='Connection id')
    sub_parser.add_argument('status', action=StorePositional, type=str, help='Status')
    sub_parser.add_argument('reason', action=StorePositional, type=str, help='Reason')
    sub_parser = commands.add_parser('delete_connection', help='Delete connection')
    sub_parser.add_argument('connection_id', action=StorePositional, type=int, help='Connection id')

    # Devices
    sub_parser = commands.add_parser('list_devices', help='List devices of a connection')
    sub_parser.add_argument('connection_id', action=StorePositional, type=int, help='Connection id')
    sub_parser = commands.add_parser('get_device', help='Get a device of a connection')
    sub_parser.add_argument('connection_id', action=StorePositional, type=int, help='Connection id')
    sub_parser.add_argument('device_id', action=StorePositional, type=int, help='Device id')
    sub_parser = commands.add_parser('set_devices', help='Set the devices of a connection')
    sub_parser.add_argument('connection_id', action=StorePositional, type=int, help='Connection id')
    sub_parser.add_argument('devices', action=StorePositional, type=str, help='The json representation of the devices')
    sub_parser = commands.add_parser('update_devices', help='Update the devices of a connection (merge with existing)')
    sub_parser.add_argument('connection_id', action=StorePositional, type=int, help='Connection id')
    sub_parser.add_argument('devices', action=StorePositional, type=str, help='The json representation of the devices')

    # Subscriptions
    commands.add_parser('list_subscriptions', help='List subscriptions')
    sub_parser = commands.add_parser('get_subscription', help='Get subscription')
    sub_parser.add_argument('subscription_key', action=StorePositional, type=str, help='Subscription key')
    sub_parser = commands.add_parser('set_subscription', help='Set the subscription')
    sub_parser.add_argument('subscription_key', action=StorePositional, type=str, help='Subscription key')
    sub_parser.add_argument('path', action=StorePositional, type=str, help='Data path')
    sub_parser.add_argument('url', action=StorePositional, type=str, help='Subscription url')
    sub_parser.add_argument('origin', action=StorePositional, type=str,
                            help='Origin (%s)' % ', '.join(Origin.__members__.keys()))
    sub_parser.add_argument('filter', action=StorePositional, type=str,
                            help='The json representation of the subscription filter')
    sub_parser = commands.add_parser('remove_subscription', help='Remove subscription')
    sub_parser.add_argument('subscription_key', action=StorePositional, type=str, help='Subscription key')
    commands.add_parser('remove_all_subscriptions', help='Remove all subscriptions')

    # Data
    commands.add_parser('list_streams', help='List available streams')
    sub_parser = commands.add_parser('get_data', help='Get data of a stream')
    sub_parser.add_argument('stream', action=StorePositional, type=str, help='Stream path')
    sub_parser = commands.add_parser('write_data', help='Write data to a stream')
    sub_parser.add_argument('stream', action=StorePositional, type=str, help='Stream path')
    sub_parser.add_argument('data', action=StorePositional, type=str,
                            help='The json representation of the data')
    sub_parser = commands.add_parser('get_stats', help='Get data statistics for a stream')
    sub_parser.add_argument('stream', action=StorePositional, type=str, help='Stream path')
    sub_parser.add_argument('fields', metavar='N', type=str, nargs='*',
                            help='Stats fields to be returned (default ALL)')

    sub_parser = commands.add_parser('get_summaries', help='Get data summaries for a stream')
    sub_parser.add_argument('stream', action=StorePositional, type=str, help='Stream path')

    # Light
    sub_parser = commands.add_parser('set_light_state', help='Set light state')
    sub_parser.add_argument('light_udi', action=StorePositional, type=str, help='Light udi')
    sub_parser.add_argument('state', action=StorePositional, type=str, help='Light state (on/off)')
    sub_parser.add_argument('color', action=StorePositional, type=str, help='Light color (in hex format)')

    # Thermostat
    sub_parser = commands.add_parser('set_thermostat_mode', help='Set thermostat mode')
    sub_parser.add_argument('thermostat_udi', action=StorePositional, type=str, help='Thermostat udi')
    sub_parser.add_argument('mode', action=StorePositional, type=str,
                            help='Thermostat mode (%s)' % ', '.join(ThermostatMode.__members__.keys()))
    sub_parser.add_argument('temperature', action=StorePositional, type=float, help='Thermostat mode temperature')
    sub_parser.add_argument('end_date', action=StorePositional, type=str,
                            help='Thermostat mode end date in JSON format')

    arguments = parser.parse_args()

    if arguments.verbose:
        logging.basicConfig(level=logging.DEBUG, format='%(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='%(message)s')
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
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
    command_mapper["set_subscription"] = lambda c: c.subscription.set_subscription("me",
                                                                                   arguments.subscription_key,
                                                                                   arguments.path,
                                                                                   arguments.url,
                                                                                   getattr(Origin,
                                                                                           arguments.origin.upper()),
                                                                                   json.loads(arguments.filter))
    command_mapper["remove_subscription"] = lambda c: c.subscription.remove_subscription("me",
                                                                                         arguments.subscription_key)
    command_mapper["remove_all_subscriptions"] = lambda c: c.subscription.remove_subscriptions("me")

    # Data
    command_mapper["list_streams"] = lambda c: c.data.list_streams("me")
    command_mapper["get_data"] = lambda c: c.data.get_data("me", arguments.stream)
    command_mapper["write_data"] = lambda c: c.data.write_data("me",
                                                               arguments.stream,
                                                               json.loads(arguments.data))
    command_mapper["get_stats"] = lambda c: c.data.get_stats("me", arguments.stream,
                                                             [getattr(StatsField, field.upper())
                                                              for field in arguments.fields]
                                                             )

    command_mapper["get_summaries"] = lambda c: c.data.get_summaries("me", arguments.stream)

    # Light
    command_mapper["set_light_state"] = lambda c: c.command.set_light_state("me",
                                                                            [arguments.light_udi],
                                                                            arguments.state.lower() == "on",
                                                                            arguments.color if len(arguments.color) > 0
                                                                            else None)

    # Thermostat
    command_mapper["set_thermostat_mode"] = lambda c: c.command.set_thermostat_mode("me", [arguments.thermostat_udi],
                                                                                    getattr(ThermostatMode,
                                                                                            arguments.mode.upper()),
                                                                                    arguments.temperature,
                                                                                    arguments.end_date)

    def _print_result(result):
        if result is not None:
            try:
                _logger.info(json.dumps(result, indent=1))
            except:
                _logger.info(result)

    with load_client(arguments.target) as client:
        if arguments.action is not None:
            try:
                _print_result(command_mapper[arguments.action](client))
            except KeyError:
                _logger.error('\'%s\': not implemented', arguments.action)
        else:
            parser.print_help()


if __name__ == '__main__':
    main()
