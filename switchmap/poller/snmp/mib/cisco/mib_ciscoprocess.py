"""Class interacts with devices supporting CISCO-PROCESS-MIB."""

from collections import defaultdict
from switchmap.poller.snmp.base_query import Query
import asyncio
from switchmap.core import log


def get_query():
    """Return this module's Query class.

    Args:
        None

    Returns:
        type: CiscoProcessQuery class
    """
    return CiscoProcessQuery


def init_query(snmp_object):
    """Initialize and return this module's Query class.

    Args:
        snmp_object: SNMP interact class object from snmp_manager.py

    Returns:
        CiscoProcessQuery: Initialized query instance
    """
    return CiscoProcessQuery(snmp_object)


class CiscoProcessQuery(Query):
    """Class interacts with devices supporting CISCO-PROCESS-MIB."""

    def __init__(self, snmp_object):
        """Instantiate the class.

        Args:
            snmp_object: SNMP interact class object from snmp_manager.py

        Returns:
            None
        """
        self.snmp_object = snmp_object

        # Test OID for Cisco CPU monitoring - cpmCPUTotalTable
        test_oid = ".1.3.6.1.4.1.9.9.109.1.1.1.1.8.1"

        super().__init__(snmp_object, test_oid, tags=["system"])

    async def system(self):
        """Get system resource data from Cisco devices."""
        # Initialize key variables
        final = defaultdict(lambda: defaultdict(dict))

        # Get CPU and memory data concurrently
        try:
            cpu_data, memory_used_data, memory_free_data = await asyncio.gather(
                self.cpmcputotal5minrev(),
                self.memorypoolused(),
                self.memorypoolfree(),
                return_exceptions=True,
            )

            # Populate final results with better structure
            if cpu_data is not None and not isinstance(cpu_data, Exception):
                final["CISCO-PROCESS-MIB"]["cpmCPUTotal5minRev"] = cpu_data

            if memory_used_data is not None and not isinstance(
                memory_used_data, Exception
            ):
                final["CISCO-PROCESS-MIB"][
                    "ciscoMemoryPoolUsed"
                ] = memory_used_data

            if memory_free_data is not None and not isinstance(
                memory_free_data, Exception
            ):
                final["CISCO-PROCESS-MIB"][
                    "ciscoMemoryPoolFree"
                ] = memory_free_data
        except Exception as e:
            log.log2warning(1095, f"Error in Cisco Process MIB: {e}")
            return final

        return final

    async def cpmcputotal5minrev(self, oidonly=False):
        """Return dict of CISCO-PROCESS-MIB cpmCPUTotal5minRev for device."""
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Process OID - 5 minute average CPU utilization
        oid = ".1.3.6.1.4.1.9.9.109.1.1.1.1.8"

        # Return OID value for unittests
        if oidonly is True:
            return oid

        try:
            results = await self.snmp_object.swalk(oid, normalized=True)
            for key, value in results.items():
                data_dict[int(key)] = value
        except Exception as e:
            log.log2warning(1317, f"Error querying Cisco CPU: {e}")

        return data_dict

    async def memorypoolused(self, oidonly=False):
        """Get total used memory from CISCO-MEMORY-POOL-MIB.

        Args:
            oidonly (bool): If True, return the OID string instead of querying.

        Returns:
            int | str | None: Sum of used memory in bytes,
                              OID string if oidonly=True,
                              or None on error.
        """
        # Process OID - Enhanced memory pool used (high capacity)
        oid = ".1.3.6.1.4.1.9.9.48.1.1.1.5"

        # Return OID value for unittests
        if oidonly is True:
            return oid

        try:
            results = await self.snmp_object.swalk(oid, normalized=True)
            used_memory = sum(results.values())

            return used_memory
        except Exception as e:
            log.log2warning(1318, f"Error querying Cisco MemoryPoolUsed: {e}")
            return None

    async def memorypoolfree(self, oidonly=False):
        """Get total free memory from CISCO-MEMORY-POOL-MIB.

        Args:
            oidonly (bool): If True, return the OID string instead of querying.

        Returns:
            int | str | None: Sum of free memory in bytes,
                              OID string if oidonly=True,
                              or None on error.
        """
        # Process OID - Enhanced memory pool free (high capacity)
        oid = ".1.3.6.1.4.1.9.9.48.1.1.1.6"

        # Return OID value for unittests
        if oidonly is True:
            return oid

        try:
            results = await self.snmp_object.swalk(oid, normalized=True)
            free_memory = sum(results.values())

            return free_memory

        except Exception as e:
            log.log2warning(1319, f"Error querying Cisco MemoryPoolFree: {e}")
            return None
