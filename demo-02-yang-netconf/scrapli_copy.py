from scrapli import Netconf
from scrapli.netconf import DatastoreType


from settings import Settings


def main():
    netconf = Netconf(
        host=Settings.host,
    )

    with netconf as nc:
        result = nc.copy_config(
            target=DatastoreType.CANDIDATE, source=DatastoreType.RUNNING
        )
        print(result.result)


if __name__ == "__main__":
    main()
