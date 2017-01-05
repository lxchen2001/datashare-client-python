Orange Cloud python client
==========================
.. image:: https://img.shields.io/pypi/v/orange-datashare.svg
:target: https://pypi.python.org/pypi/orange-datashare
.. image:: https://img.shields.io/github/license/Orange-OpenSource/datashare-client-python.svg
	:target: https://raw.githubusercontent.com/Orange-OpenSource/datashare-client-python/master/LICENSE

This library is a python implementation of the `orange datashare <https://developer.orange.com/apis/discover-datashare/>`_
It brings:

- an `api <#api>`_ to build interact with datashare api
- a `command line interface <#cli>`_ to directly interact with datashare

Dependencies
------------
It is based on:

- `oauth2 client library <https://github.com/antechrestos/OAuth2Client>`_, itself based on `requests <https://pypi.python.org/pypi/requests>`_.


Installing
----------

From pip
~~~~~~~~
.. code-block:: bash

	$ pip install orange-datashare

From sources
~~~~~~~~~~~~

To build the library run :

.. code-block:: bash

	$ python setup.py install

Run the OAuth Grant code process
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To start using it you must create a **developer** account on the
`orange partner platform <https://developer.orange.com/signin>`_.
Then create an application. But beware on one things: the **redirect url** must differ from any `localhost` or local url.
Since we want to trick it, do as follow:

- pick a domain name such `http://my-own-cloud.io:8080` (**do not use https as it cannot be handled later**)
- create the application
- map the **domain** `my-own-cloud.io` on `localhost` in your **host file** ( `/etc/hosts` for linux,
    `%systemroot%\\system32\\drivers\\etc\\` for windows)
- run the following code


.. code-block:: python

    from orange_datashare.client import DatashareClient
    # provide the client id and client secret got on your application page
    client = DatashareClient(client_id, client_secret, ['read_indoor_temperature', 'read_connection'])
    # in this example the redirect url  is http://myowncloud.io:8080 and /etc/hosts contains the line
    # 127.0.0.1       myowncloud.io
    redirect_uri = 'http://myowncloud.io:8080'
    url_to_open = client.init_authorize_code_process(redirect_uri=redirect_uri, state='1234')
    print 'Open this URL: %s' % url_to_open
    # this will block until an http request performs a GET locally with code as a query parameter
    code = client.wait_and_terminate_authorize_code_process()
    client.init_with_authorize_code(redirect_uri=redirect_uri, code=code)
    print 'refresh_token got %s' % api_manager.refresh_token

This will run a **local http server listening to your domain**, print an url to open. **Open it in your browser**,
log in using your cloud account, consent the access for your application.
You will be then redirected to your **local http server**. The code will be then extracted and exchanged for a token.
You can save your `refresh token`. Next time you can instantiate the `ApiManager` as follows:

.. code-block:: python

    client = DatashareClient(client_id, client_secret, ['read_indoor_temperature', 'read_connection'])
    api_manager.init_with_token(refresh_token)

You are now fully able to use the api.

API
---
The api brings the following *domains*.

- `connection`: this API will allows you to manage connection.
- `device`: this API will allows you to manage devices of connection.
- `subscription`: this API will allows you to manage your subscriptions
- `data`: with this API you will be allowed to query the data of your devices
- `command`:  this API here to send command on light and thermostat devices

To get some example, take a look at the tests

Command Line interface
----------------------
To run the client, enter the following command :

.. code-block:: bash

	$ orange_datashare

At first execution, it will ask you questions.
Please note that your credentials won't be saved on your disk: only tokens will be kept for further use.

Issues and contributions
------------------------
Please submit issue/pull request.
