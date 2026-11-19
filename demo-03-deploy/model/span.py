from __future__ import annotations

from enum import Enum
from typing import Annotated, ClassVar

from pydantic import AliasChoices, ConfigDict, Field, RootModel

from pydantify_common.model import XMLPydantifyModel


class AddressIpv4Type(RootModel[str]):
    model_config = ConfigDict(
        regex_engine="python-re",
    )
    root: Annotated[
        str,
        Field(
            pattern="^(?=^.*(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])(%[p\\{N\\}p\\{L\\}]+)?.*$).*$"
        ),
    ]
    """
    global address Ipv4 base type
    """


class AddressIpv6Type(RootModel[str]):
    model_config = ConfigDict(
        regex_engine="python-re",
    )
    root: Annotated[
        str,
        Field(
            pattern="^(?=^.*((.*:|.*[0-9a-fA-F]{0,4}):)([0-9a-fA-F]{0,4}:){0,5}((([0-9a-fA-F]{0,4}:)?(:|[0-9a-fA-F]{0,4}))|(((25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9])\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9])))(%[p\\{N\\}p\\{L\\}]+)?.*$)(?=^.*(([^:]+:){6}(([^:]+:[^:]+).*|(.*\\..*).*)).*|.*((([^:]+:)*[^:]+)?::(([^:]+:)*[^:]+)?)(%.+)?.*$).*$"
        ),
    ]
    """
    global address Ipv6 base type
    """


class EnumerationEnum2(Enum):
    local = "local"
    erspan_source = "erspan-source"
    erspan_dst = "erspanDst"
    warp = "warp"


class EnumerationEnum4(Enum):
    up = "up"
    down = "down"


class EnumerationEnum5(Enum):
    v2 = "v2"
    v3 = "v3"
    v3_rfc_compliant = "v3-rfc-compliant"


class EnumerationEnum6(Enum):
    none = "none"
    rx = "rx"
    tx = "tx"
    both = "both"


class EnumerationEnum7(Enum):
    rx = "rx"
    tx = "tx"
    both = "both"


class FiltervlanListListEntry(XMLPydantifyModel):
    """
    Range of Filter VLANs specified for the current monitor sesion list
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[str | None] = "http://cisco.com/ns/yang/cisco-nx-os-device"
    prefix: ClassVar[str | None] = "top"
    vlan: Annotated[
        str,
        Field(
            serialization_alias="Cisco-NX-OS-device:vlan",
            validation_alias=AliasChoices("Cisco-NX-OS-device:vlan", "vlan"),
        ),
    ]
    """
    VLAN id for Filter VLAN
    """


class SpanFwddropsrcdirectionType(RootModel[EnumerationEnum6]):
    model_config = ConfigDict(
        regex_engine="python-re",
    )
    root: EnumerationEnum6


class SpanHeaderverType(RootModel[EnumerationEnum5]):
    model_config = ConfigDict(
        regex_engine="python-re",
    )
    root: EnumerationEnum5


class SpanSrcdirectionType(RootModel[EnumerationEnum7]):
    model_config = ConfigDict(
        regex_engine="python-re",
    )
    root: EnumerationEnum7


class SpanStateType(RootModel[EnumerationEnum4]):
    model_config = ConfigDict(
        regex_engine="python-re",
    )
    root: EnumerationEnum4


class SpanTypeType(RootModel[EnumerationEnum2]):
    model_config = ConfigDict(
        regex_engine="python-re",
    )
    root: EnumerationEnum2


class TypeLeaf(RootModel[SpanTypeType]):
    model_config = ConfigDict(
        regex_engine="python-re",
    )
    root: SpanTypeType
    """
    Type of the current monitor session
    """


class ConfigstateLeaf(RootModel[SpanStateType]):
    model_config = ConfigDict(
        regex_engine="python-re",
    )
    root: SpanStateType
    """
    State of the current session as configured by the user
    """


class DestinationgroupListListEntry(XMLPydantifyModel):
    """
    Destination group configuration MO for warp session. list
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[str | None] = "http://cisco.com/ns/yang/cisco-nx-os-device"
    prefix: ClassVar[str | None] = "top"
    grpid: Annotated[
        int,
        Field(
            ge=1,
            le=12,
            serialization_alias="Cisco-NX-OS-device:grpid",
            validation_alias=AliasChoices("Cisco-NX-OS-device:grpid", "grpid"),
        ),
    ]
    """
    The group id for the destination port
    """


class DirectionLeaf(RootModel[SpanSrcdirectionType]):
    model_config = ConfigDict(
        regex_engine="python-re",
    )
    root: SpanSrcdirectionType
    """
    The direction of the source interface - Rx, Tx, Both
    """


class DirectionLeaf2(RootModel[SpanSrcdirectionType]):
    model_config = ConfigDict(
        regex_engine="python-re",
    )
    root: SpanSrcdirectionType
    """
    The direction of the source VLAN - Rx, Tx, Both
    """


class DirectionLeaf3(RootModel[SpanSrcdirectionType]):
    model_config = ConfigDict(
        regex_engine="python-re",
    )
    root: SpanSrcdirectionType
    """
    The direction of the source VSAN - Rx, Tx, Both
    """


class DstgrpItemsContainer(XMLPydantifyModel):
    """
    Destination group configuration MO for warp session.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[str | None] = "http://cisco.com/ns/yang/cisco-nx-os-device"
    prefix: ClassVar[str | None] = "top"
    destination_group_list: Annotated[
        list[DestinationgroupListListEntry] | None,
        Field(
            serialization_alias="Cisco-NX-OS-device:DestinationGroup-list",
            validate_default=True,
            validation_alias=AliasChoices(
                "Cisco-NX-OS-device:DestinationGroup-list",
                "destination_group_list",
                "DestinationGroup-list",
            ),
        ),
    ] = []


class FilterItemsContainer(XMLPydantifyModel):
    """
    Range of Filter VLANs specified for the current monitor sesion
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[str | None] = "http://cisco.com/ns/yang/cisco-nx-os-device"
    prefix: ClassVar[str | None] = "top"
    filter_vlan_list: Annotated[
        list[FiltervlanListListEntry] | None,
        Field(
            serialization_alias="Cisco-NX-OS-device:FilterVlan-list",
            validate_default=True,
            validation_alias=AliasChoices(
                "Cisco-NX-OS-device:FilterVlan-list",
                "filter_vlan_list",
                "FilterVlan-list",
            ),
        ),
    ] = []


class FilteripItemsContainer(XMLPydantifyModel):
    """
    Filter ip tx configuration MO for local and ERSPAN monitor session.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[str | None] = "http://cisco.com/ns/yang/cisco-nx-os-device"
    prefix: ClassVar[str | None] = "top"
    source_ip: Annotated[
        AddressIpv4Type | AddressIpv6Type | None,
        Field(
            serialization_alias="Cisco-NX-OS-device:sourceIp",
            validation_alias=AliasChoices(
                "Cisco-NX-OS-device:sourceIp", "source_ip", "sourceIp"
            ),
        ),
    ] = None
    """
    filter source ip for monitor session.
    """
    source_mask: Annotated[
        AddressIpv4Type | AddressIpv6Type | None,
        Field(
            serialization_alias="Cisco-NX-OS-device:sourceMask",
            validation_alias=AliasChoices(
                "Cisco-NX-OS-device:sourceMask", "source_mask", "sourceMask"
            ),
        ),
    ] = None
    """
    filter mask for source ip of monitor session.
    """
    destination_ip: Annotated[
        AddressIpv4Type | AddressIpv6Type | None,
        Field(
            serialization_alias="Cisco-NX-OS-device:destinationIp",
            validation_alias=AliasChoices(
                "Cisco-NX-OS-device:destinationIp", "destination_ip", "destinationIp"
            ),
        ),
    ] = None
    """
    filter destination ip for monitor session.
    """
    destination_mask: Annotated[
        AddressIpv4Type | AddressIpv6Type | None,
        Field(
            serialization_alias="Cisco-NX-OS-device:destinationMask",
            validation_alias=AliasChoices(
                "Cisco-NX-OS-device:destinationMask",
                "destination_mask",
                "destinationMask",
            ),
        ),
    ] = None
    """
    filter mask for destination ip of  monitor session.
    """
    is_tx_control_pkts: Annotated[
        bool | None,
        Field(
            serialization_alias="Cisco-NX-OS-device:isTxControlPkts",
            validation_alias=AliasChoices(
                "Cisco-NX-OS-device:isTxControlPkts",
                "is_tx_control_pkts",
                "isTxControlPkts",
            ),
        ),
    ] = None
    """
    Denotes whether filter tx control packets is enabled for the given monitor session
    """


class FwddropsdirectionLeaf(RootModel[SpanFwddropsrcdirectionType]):
    model_config = ConfigDict(
        regex_engine="python-re",
    )
    root: SpanFwddropsrcdirectionType
    """
    Denotes forwarding drop direction for the given erspan-source session None, Rx, Tx, Both
    """


class HeadertypeLeaf(RootModel[SpanHeaderverType]):
    model_config = ConfigDict(
        regex_engine="python-re",
    )
    root: SpanHeaderverType
    """
    Denotes header type ver is enabled for the given erspan session
    """


class SourceintfListListEntry(XMLPydantifyModel):
    """
    Source interface configuration MO. list
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[str | None] = "http://cisco.com/ns/yang/cisco-nx-os-device"
    prefix: ClassVar[str | None] = "top"
    direction: Annotated[
        DirectionLeaf | None,
        Field(
            serialization_alias="Cisco-NX-OS-device:direction",
            validate_default=True,
            validation_alias=AliasChoices("Cisco-NX-OS-device:direction", "direction"),
        ),
    ] = "both"
    id: Annotated[
        str,
        Field(
            serialization_alias="Cisco-NX-OS-device:id",
            validation_alias=AliasChoices("Cisco-NX-OS-device:id", "id"),
        ),
    ]
    """
    The interface id for the session
    """
    allow_pfc: Annotated[
        bool | None,
        Field(
            serialization_alias="Cisco-NX-OS-device:allowPfc",
            validation_alias=AliasChoices(
                "Cisco-NX-OS-device:allowPfc", "allow_pfc", "allowPfc"
            ),
        ),
    ] = False
    """
    Denotes whether allow-pfc is enabled for the given source
    """


class SourcevlanListListEntry(XMLPydantifyModel):
    """
    Source configuration MO. list
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[str | None] = "http://cisco.com/ns/yang/cisco-nx-os-device"
    prefix: ClassVar[str | None] = "top"
    vlan: Annotated[
        str,
        Field(
            serialization_alias="Cisco-NX-OS-device:vlan",
            validation_alias=AliasChoices("Cisco-NX-OS-device:vlan", "vlan"),
        ),
    ]
    """
    VLAN id for Source VLAN
    """
    direction: Annotated[
        DirectionLeaf2 | None,
        Field(
            serialization_alias="Cisco-NX-OS-device:direction",
            validate_default=True,
            validation_alias=AliasChoices("Cisco-NX-OS-device:direction", "direction"),
        ),
    ] = "both"


class SourcevsanListListEntry(XMLPydantifyModel):
    """
    Source vsan configuration MO. list
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[str | None] = "http://cisco.com/ns/yang/cisco-nx-os-device"
    prefix: ClassVar[str | None] = "top"
    vsan: Annotated[
        str,
        Field(
            serialization_alias="Cisco-NX-OS-device:vsan",
            validation_alias=AliasChoices("Cisco-NX-OS-device:vsan", "vsan"),
        ),
    ]
    """
    VSAN id for Source VSAN
    """
    direction: Annotated[
        DirectionLeaf3 | None,
        Field(
            serialization_alias="Cisco-NX-OS-device:direction",
            validate_default=True,
            validation_alias=AliasChoices("Cisco-NX-OS-device:direction", "direction"),
        ),
    ] = "both"


class SrcItemsContainer(XMLPydantifyModel):
    """
    Source configuration MO.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[str | None] = "http://cisco.com/ns/yang/cisco-nx-os-device"
    prefix: ClassVar[str | None] = "top"
    source_vlan_list: Annotated[
        list[SourcevlanListListEntry] | None,
        Field(
            serialization_alias="Cisco-NX-OS-device:SourceVlan-list",
            validate_default=True,
            validation_alias=AliasChoices(
                "Cisco-NX-OS-device:SourceVlan-list",
                "source_vlan_list",
                "SourceVlan-list",
            ),
        ),
    ] = []


class SrcintfItemsContainer(XMLPydantifyModel):
    """
    Source interface configuration MO.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[str | None] = "http://cisco.com/ns/yang/cisco-nx-os-device"
    prefix: ClassVar[str | None] = "top"
    source_intf_list: Annotated[
        list[SourceintfListListEntry] | None,
        Field(
            serialization_alias="Cisco-NX-OS-device:SourceIntf-list",
            validate_default=True,
            validation_alias=AliasChoices(
                "Cisco-NX-OS-device:SourceIntf-list",
                "source_intf_list",
                "SourceIntf-list",
            ),
        ),
    ] = []


class SrcvsanItemsContainer(XMLPydantifyModel):
    """
    Source vsan configuration MO.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[str | None] = "http://cisco.com/ns/yang/cisco-nx-os-device"
    prefix: ClassVar[str | None] = "top"
    source_vsan_list: Annotated[
        list[SourcevsanListListEntry] | None,
        Field(
            serialization_alias="Cisco-NX-OS-device:SourceVsan-list",
            validate_default=True,
            validation_alias=AliasChoices(
                "Cisco-NX-OS-device:SourceVsan-list",
                "source_vsan_list",
                "SourceVsan-list",
            ),
        ),
    ] = []


class MonitorListListEntry(XMLPydantifyModel):
    """
    Monitor MO for each SPAN session identified by session id list
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[str | None] = "http://cisco.com/ns/yang/cisco-nx-os-device"
    prefix: ClassVar[str | None] = "top"
    type: Annotated[
        TypeLeaf | None,
        Field(
            serialization_alias="Cisco-NX-OS-device:type",
            validate_default=True,
            validation_alias=AliasChoices("Cisco-NX-OS-device:type", "type"),
        ),
    ] = "local"
    config_state: Annotated[
        ConfigstateLeaf | None,
        Field(
            serialization_alias="Cisco-NX-OS-device:configState",
            validate_default=True,
            validation_alias=AliasChoices(
                "Cisco-NX-OS-device:configState", "config_state", "configState"
            ),
        ),
    ] = "down"
    description: Annotated[
        str | None,
        Field(
            max_length=32,
            min_length=0,
            serialization_alias="Cisco-NX-OS-device:description",
            validation_alias=AliasChoices(
                "Cisco-NX-OS-device:description", "description"
            ),
        ),
    ] = None
    """
    Description for the current monitor session
    """
    vrf_name: Annotated[
        str | None,
        Field(
            pattern="^(?=^[A-Za-z0-9!@#$\\^\\*=\\+\\{\\}\\.;:_-]{1,32}$).*$",
            serialization_alias="Cisco-NX-OS-device:vrfName",
            validation_alias=AliasChoices(
                "Cisco-NX-OS-device:vrfName", "vrf_name", "vrfName"
            ),
        ),
    ] = None
    """
    VRF name for the erspan-source session.(user specified name / default / manangement)
    """
    acl_name: Annotated[
        str | None,
        Field(
            max_length=64,
            min_length=0,
            serialization_alias="Cisco-NX-OS-device:aclName",
            validation_alias=AliasChoices(
                "Cisco-NX-OS-device:aclName", "acl_name", "aclName"
            ),
        ),
    ] = None
    """
    Name of the Access Control List applied on the current monitor session
    """
    id: Annotated[
        int,
        Field(
            ge=1,
            le=32,
            serialization_alias="Cisco-NX-OS-device:id",
            validation_alias=AliasChoices("Cisco-NX-OS-device:id", "id"),
        ),
    ]
    """
    Session identification number for current monitor session.
    """
    mtu: Annotated[
        int | None,
        Field(
            ge=64,
            le=10240,
            serialization_alias="Cisco-NX-OS-device:mtu",
            validation_alias=AliasChoices("Cisco-NX-OS-device:mtu", "mtu"),
        ),
    ] = 10240
    """
    Value of Maximum transmission unit truncation size for SPAN packets
    """
    allow_sharing: Annotated[
        bool | None,
        Field(
            serialization_alias="Cisco-NX-OS-device:allowSharing",
            validation_alias=AliasChoices(
                "Cisco-NX-OS-device:allowSharing", "allow_sharing", "allowSharing"
            ),
        ),
    ] = False
    """
    Denotes whether sharing is enabled for the given filter ACL
    """
    header_type: Annotated[
        HeadertypeLeaf | None,
        Field(
            serialization_alias="Cisco-NX-OS-device:headerType",
            validation_alias=AliasChoices(
                "Cisco-NX-OS-device:headerType", "header_type", "headerType"
            ),
        ),
    ] = None
    is_marker_packet: Annotated[
        bool | None,
        Field(
            serialization_alias="Cisco-NX-OS-device:isMarkerPacket",
            validation_alias=AliasChoices(
                "Cisco-NX-OS-device:isMarkerPacket",
                "is_marker_packet",
                "isMarkerPacket",
            ),
        ),
    ] = False
    """
    Denotes whether marker packet is enabled for the given erspan-source session
    """
    is_marker_milli_seconds: Annotated[
        bool | None,
        Field(
            serialization_alias="Cisco-NX-OS-device:isMarkerMilliSeconds",
            validation_alias=AliasChoices(
                "Cisco-NX-OS-device:isMarkerMilliSeconds",
                "is_marker_milli_seconds",
                "isMarkerMilliSeconds",
            ),
        ),
    ] = False
    """
    Denotes whether marker value given in millis seconds
    """
    is_fwd_drops_rx: Annotated[
        bool | None,
        Field(
            serialization_alias="Cisco-NX-OS-device:isFwdDropsRx",
            validation_alias=AliasChoices(
                "Cisco-NX-OS-device:isFwdDropsRx", "is_fwd_drops_rx", "isFwdDropsRx"
            ),
        ),
    ] = False
    """
    Denotes whether source forwarding drops rx is enabled for the given erspan-source session
    """
    is_fwd_drops_rx_low_priority: Annotated[
        bool | None,
        Field(
            serialization_alias="Cisco-NX-OS-device:isFwdDropsRxLowPriority",
            validation_alias=AliasChoices(
                "Cisco-NX-OS-device:isFwdDropsRxLowPriority",
                "is_fwd_drops_rx_low_priority",
                "isFwdDropsRxLowPriority",
            ),
        ),
    ] = False
    """
    Denotes whether source forwarding drops rx has low priority for the given erspan-source session
    """
    fwd_drops_direction: Annotated[
        FwddropsdirectionLeaf | None,
        Field(
            serialization_alias="Cisco-NX-OS-device:fwdDropsDirection",
            validate_default=True,
            validation_alias=AliasChoices(
                "Cisco-NX-OS-device:fwdDropsDirection",
                "fwd_drops_direction",
                "fwdDropsDirection",
            ),
        ),
    ] = "none"
    erspan_id: Annotated[
        int | None,
        Field(
            ge=0,
            le=1023,
            serialization_alias="Cisco-NX-OS-device:erspanId",
            validation_alias=AliasChoices(
                "Cisco-NX-OS-device:erspanId", "erspan_id", "erspanId"
            ),
        ),
    ] = 0
    """
    ERSPAN identification number
    """
    ip_ttl: Annotated[
        int | None,
        Field(
            ge=1,
            le=255,
            serialization_alias="Cisco-NX-OS-device:ipTtl",
            validation_alias=AliasChoices(
                "Cisco-NX-OS-device:ipTtl", "ip_ttl", "ipTtl"
            ),
        ),
    ] = 255
    """
    ERSPAN IP time-to-live value
    """
    ip_dscp: Annotated[
        int | None,
        Field(
            ge=0,
            le=63,
            serialization_alias="Cisco-NX-OS-device:ipDscp",
            validation_alias=AliasChoices(
                "Cisco-NX-OS-device:ipDscp", "ip_dscp", "ipDscp"
            ),
        ),
    ] = 0
    """
    ERSPAN IP DSCP value
    """
    marker_pkt_int: Annotated[
        int | None,
        Field(
            ge=1,
            le=1000,
            serialization_alias="Cisco-NX-OS-device:markerPktInt",
            validation_alias=AliasChoices(
                "Cisco-NX-OS-device:markerPktInt", "marker_pkt_int", "markerPktInt"
            ),
        ),
    ] = 100
    """
    ERSPAN session send marker packet interval value
    """
    destination_ports: Annotated[
        str | None,
        Field(
            serialization_alias="Cisco-NX-OS-device:destinationPorts",
            validation_alias=AliasChoices(
                "Cisco-NX-OS-device:destinationPorts",
                "destination_ports",
                "destinationPorts",
            ),
        ),
    ] = None
    """
    Destination ports for the current session
    """
    destination_ip: Annotated[
        AddressIpv4Type | AddressIpv6Type | None,
        Field(
            serialization_alias="Cisco-NX-OS-device:destinationIp",
            validation_alias=AliasChoices(
                "Cisco-NX-OS-device:destinationIp", "destination_ip", "destinationIp"
            ),
        ),
    ] = None
    """
    Destination IP address for the current erspan session
    """
    destination_ipv6: Annotated[
        str | None,
        Field(
            pattern="^(?=^.*((.*:|.*[0-9a-fA-F]{0,4}):)([0-9a-fA-F]{0,4}:){0,5}((([0-9a-fA-F]{0,4}:)?(:|[0-9a-fA-F]{0,4}))|(((25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9])\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9])))(%[p\\{N\\}p\\{L\\}]+)?.*$)(?=^.*(([^:]+:){6}(([^:]+:[^:]+).*|(.*\\..*).*)).*|.*((([^:]+:)*[^:]+)?::(([^:]+:)*[^:]+)?)(%.+)?.*$).*$",
            serialization_alias="Cisco-NX-OS-device:destinationIpv6",
            validation_alias=AliasChoices(
                "Cisco-NX-OS-device:destinationIpv6",
                "destination_ipv6",
                "destinationIpv6",
            ),
        ),
    ] = None
    """
    Destination IPv6 address for the current erspan session
    """
    source_ip: Annotated[
        AddressIpv4Type | AddressIpv6Type | None,
        Field(
            serialization_alias="Cisco-NX-OS-device:sourceIp",
            validation_alias=AliasChoices(
                "Cisco-NX-OS-device:sourceIp", "source_ip", "sourceIp"
            ),
        ),
    ] = None
    """
    Source IP address for the current erspan destination session
    """
    source_ipv6: Annotated[
        str | None,
        Field(
            pattern="^(?=^.*((.*:|.*[0-9a-fA-F]{0,4}):)([0-9a-fA-F]{0,4}:){0,5}((([0-9a-fA-F]{0,4}:)?(:|[0-9a-fA-F]{0,4}))|(((25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9])\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9])))(%[p\\{N\\}p\\{L\\}]+)?.*$)(?=^.*(([^:]+:){6}(([^:]+:[^:]+).*|(.*\\..*).*)).*|.*((([^:]+:)*[^:]+)?::(([^:]+:)*[^:]+)?)(%.+)?.*$).*$",
            serialization_alias="Cisco-NX-OS-device:sourceIpv6",
            validation_alias=AliasChoices(
                "Cisco-NX-OS-device:sourceIpv6", "source_ipv6", "sourceIpv6"
            ),
        ),
    ] = None
    """
    Source IPv6 address for the current erspan destination session
    """
    srcintf_items: Annotated[
        SrcintfItemsContainer | None,
        Field(
            serialization_alias="Cisco-NX-OS-device:srcintf-items",
            validation_alias=AliasChoices(
                "Cisco-NX-OS-device:srcintf-items", "srcintf_items", "srcintf-items"
            ),
        ),
    ] = None
    filter_items: Annotated[
        FilterItemsContainer | None,
        Field(
            serialization_alias="Cisco-NX-OS-device:filter-items",
            validation_alias=AliasChoices(
                "Cisco-NX-OS-device:filter-items", "filter_items", "filter-items"
            ),
        ),
    ] = None
    src_items: Annotated[
        SrcItemsContainer | None,
        Field(
            serialization_alias="Cisco-NX-OS-device:src-items",
            validation_alias=AliasChoices(
                "Cisco-NX-OS-device:src-items", "src_items", "src-items"
            ),
        ),
    ] = None
    srcvsan_items: Annotated[
        SrcvsanItemsContainer | None,
        Field(
            serialization_alias="Cisco-NX-OS-device:srcvsan-items",
            validation_alias=AliasChoices(
                "Cisco-NX-OS-device:srcvsan-items", "srcvsan_items", "srcvsan-items"
            ),
        ),
    ] = None
    filterip_items: Annotated[
        FilteripItemsContainer | None,
        Field(
            serialization_alias="Cisco-NX-OS-device:filterip-items",
            validation_alias=AliasChoices(
                "Cisco-NX-OS-device:filterip-items", "filterip_items", "filterip-items"
            ),
        ),
    ] = None
    dstgrp_items: Annotated[
        DstgrpItemsContainer | None,
        Field(
            serialization_alias="Cisco-NX-OS-device:dstgrp-items",
            validation_alias=AliasChoices(
                "Cisco-NX-OS-device:dstgrp-items", "dstgrp_items", "dstgrp-items"
            ),
        ),
    ] = None


class MonitorItemsContainer(XMLPydantifyModel):
    """
    Monitor MO for each SPAN session identified by session id
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[str | None] = "http://cisco.com/ns/yang/cisco-nx-os-device"
    prefix: ClassVar[str | None] = "top"
    monitor_list: Annotated[
        list[MonitorListListEntry] | None,
        Field(
            serialization_alias="Cisco-NX-OS-device:Monitor-list",
            validate_default=True,
            validation_alias=AliasChoices(
                "Cisco-NX-OS-device:Monitor-list", "monitor_list", "Monitor-list"
            ),
        ),
    ] = []


class SpanItemsContainer(XMLPydantifyModel):
    """
    SPAN Entity
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[str | None] = "http://cisco.com/ns/yang/cisco-nx-os-device"
    prefix: ClassVar[str | None] = "top"
    monitor_items: Annotated[
        MonitorItemsContainer | None,
        Field(
            serialization_alias="Cisco-NX-OS-device:monitor-items",
            validation_alias=AliasChoices(
                "Cisco-NX-OS-device:monitor-items", "monitor_items", "monitor-items"
            ),
        ),
    ] = None


class Model(XMLPydantifyModel):
    """
    Initialize an instance of this class and serialize it to JSON; this results in a RESTCONF payload.

    ## Tips
    Initialization:
    - all values have to be set via keyword arguments
    - if a class contains only a `root` field, it can be initialized as follows:
        - `member=MyNode(root=<value>)`
        - `member=<value>`

    Serialziation:
    - `exclude_defaults=True` omits fields set to their default value (recommended)
    - `by_alias=True` ensures qualified names are used (necessary)
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[str | None] = "http://cisco.com/ns/yang/cisco-nx-os-device"
    prefix: ClassVar[str | None] = "top"
    span_items: Annotated[
        SpanItemsContainer | None,
        Field(
            serialization_alias="Cisco-NX-OS-device:span-items",
            validation_alias=AliasChoices(
                "Cisco-NX-OS-device:span-items", "span_items", "span-items"
            ),
        ),
    ] = None


if __name__ == "__main__":
    model = Model(
        # <Initialize model here>
    )

    restconf_payload = model.model_dump_json(
        exclude_defaults=True, by_alias=True, indent=2
    )

    print(f"Generated output: {restconf_payload}")

    # Send config to network device:
    # from pydantify.utility import restconf_patch_request
    # restconf_patch_request(url='...', user_pw_auth=('usr', 'pw'), data=restconf_payload)
