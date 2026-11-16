from scrapli import Netconf
from scrapli.netconf import DatastoreType

from settings import Settings

FILTER = """
<System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
  <span-items></span-items>
</System>
"""


def main():
    netconf = Netconf(
        host=Settings.host,
    )

    with netconf as nc:
        result = nc.get_config(filter_=FILTER, source=DatastoreType.CANDIDATE)
        print(result.result)


if __name__ == "__main__":
    main()
