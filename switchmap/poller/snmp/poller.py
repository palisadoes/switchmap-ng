"""Asynchronous SNMP Poller module for switchmap-ng."""

# Switchmap imports
from switchmap.poller.configuration import ConfigPoller
from switchmap.poller import POLLING_OPTIONS, SNMP, POLL
from . import snmp_manager
from . import snmp_info
from switchmap.core import log


class Poll:
    """Asynchronous SNMP poller for switchmap-ng that gathers network data.

    This class manages SNMP credential validation and data querying for
    network devices using asynchronous operations for improved
    performance and scalability.

    Args:
        hostname (str): The hostname or IP address of the device to poll

    Methods:
        initialize_snmp(): Validates SNMP credentials and
           initializes SNMP interaction
        query(): Queries the device for topology data asynchronously
    """

    def __init__(self, hostname):
        """Initialize the class.

        Args:
            hostname: Hostname to poll

        Returns:
            None
        """
        # Initialize key variables
        self._server_config = ConfigPoller()
        self._hostname = hostname
        self.snmp_object = None

    async def initialize_snmp(self):
        """Initialize SNMP connection asynchronously.

        Returns:
            bool: True if successful, False otherwise
        """
        # Get snmp config information from Switchmap-NG
        validate = snmp_manager.Validate(
            POLLING_OPTIONS(
                hostname=self._hostname,
                authorizations=self._server_config.snmp_auth(),
            )
        )

        # Get credentials asynchronously
        authorization = await validate.credentials()

        # Create an SNMP object for querying
        if _do_poll(authorization) is True:
            self.snmp_object = snmp_manager.Interact(
                POLL(hostname=self._hostname, authorization=authorization)
            )
            return True
        else:
            log_message = (
                "Uncontactable or disabled host {}, or no valid SNMP "
                "credentials found in it.".format(self._hostname)
            )
            log.log2info(1081, log_message)
            return False

    def close(self):
        """Clean up SNMP resources.

        This method should be called when the Poll object is no longer needed
        to ensure proper cleanup of SNMP engine resources.

        Args:
            None

        Returns:
            None
        """
        if self.snmp_object and hasattr(self.snmp_object, "close"):
            self.snmp_object.close()

    async def query(self):
        """Query all remote hosts for data.

        Args:
            None

        Returns:
            dict: Polled data or None if failed
        """
        # Initialize key variables
        _data = None

        # Only query if the device is contactable
        if bool(self.snmp_object) is False:
            log.log2warning(1001, f"No valid SNMP object for {self._hostname} ")
            return _data

        # Get data
        log_message = """\
Querying topology data from host: {}.""".format(
            self._hostname
        )

        log.log2info(1078, log_message)

        status = snmp_info.Query(snmp_object=self.snmp_object)

        _data = await status.everything()

        return _data


def _do_poll(authorization):
    """Determine whether doing a poll is valid.

    Args:
        authorization: SNMP object

    Returns:
        poll: True if a poll should be done
    """
    # Initialize key variables
    poll = False

    if bool(authorization) is True:
        if isinstance(authorization, SNMP) is True:
            poll = bool(authorization.enabled)

    return poll
