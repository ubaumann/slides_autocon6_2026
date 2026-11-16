from scrapli import Netconf
from scrapli.netconf import DatastoreType, DefaultOperation

from settings import Settings

CONFIG = """
<System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
    <span-items>
        <monitor-items operation="replace">
            <Monitor-list>
                <id>10</id>
                <allowSharing>false</allowSharing>
                <configState>down</configState>
                <description>demo_ac6</description>
                <destinationIp>10.100.0.10</destinationIp>
                <erspanId>10</erspanId>
                <fwdDropsDirection>none</fwdDropsDirection>
                <ipDscp>0</ipDscp>
                <ipTtl>255</ipTtl>
                <isFwdDropsRx>false</isFwdDropsRx>
                <isFwdDropsRxLowPriority>false</isFwdDropsRxLowPriority>
                <isMarkerMilliSeconds>false</isMarkerMilliSeconds>
                <isMarkerPacket>false</isMarkerPacket>
                <markerPktInt>100</markerPktInt>
                <mtu>10240</mtu>
                <srcintf-items>
                    <SourceIntf-list>
                        <id>eth1/1/1</id>
                        <allowPfc>false</allowPfc>
                        <direction>both</direction>
                    </SourceIntf-list>
                </srcintf-items>
                <type>erspan-source</type>
                <vrfName>default</vrfName>
            </Monitor-list>
        </monitor-items>
    </span-items>
</System>
"""


def main():
    netconf = Netconf(
        host=Settings.host,
    )

    with netconf as nc:
        result = nc.edit_config(
            config=CONFIG,
            target=DatastoreType.CANDIDATE,
            default_operation=DefaultOperation.MERGE,
        )
        print(result.result)


if __name__ == "__main__":
    main()
