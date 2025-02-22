import socket
import ssl
from typing import Any, TYPE_CHECKING

SERVER_PROXY_PORT = 3307

if TYPE_CHECKING:
    import psycopg2


def connect(
    ip_address: str, ctx: ssl.SSLContext, **kwargs: Any
) -> "psycopg2.extensions.connection":
    """Helper function to create a psycopg2 DB-API connection object.

    :type ip_address: str
    :param ip_address: A string containing an IP address for the Cloud SQL
        instance.

    :type ctx: ssl.SSLContext
    :param ctx: An SSLContext object created from the Cloud SQL server CA
        cert and ephemeral cert.

    :rtype: psycopg2.extensions.connection
    :returns: A psycopg2 Connection object for the Cloud SQL instance.
    """
    try:
        import psycopg2
    except ImportError:
        raise ImportError(
            'Unable to import module "psycopg2." Please install and try again.'
        )

    # Create socket and wrap with context.
    sock = ctx.wrap_socket(
        socket.create_connection((ip_address, SERVER_PROXY_PORT)),
        server_hostname=ip_address,
    )

    user = kwargs.pop("user")
    db = kwargs.pop("db")
    passwd = kwargs.pop("password", None)
    return psycopg2.connect(
        user=user,
        dbname=db,
        password=passwd,
        host=ip_address,
        port=SERVER_PROXY_PORT,
        sslmode="require",
        sslcontext=ctx,
        **kwargs,
    )
