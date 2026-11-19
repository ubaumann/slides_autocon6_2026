from lxml import etree
from pydantify_common import model_dump_xml, XmlWrapper

from model.span import *


def create_model() -> Model:
    interfaces = [
        SourceintfListListEntry(
            direction=DirectionLeaf(SpanSrcdirectionType(EnumerationEnum7.both)),
            id="spo512",
        )
    ]
    erspans = [
        MonitorListListEntry(
            type=TypeLeaf(SpanTypeType(EnumerationEnum2.erspan_source)),
            id=10,
            config_state=ConfigstateLeaf(SpanStateType(EnumerationEnum4.down)),
            erspan_id=10,
            description="Demo AC6",
            vrf_name="default",
            destination_ip="10.100.0.10",  # type: ignore
            srcintf_items=SrcintfItemsContainer(source_intf_list=interfaces),
        )
    ]

    model = Model(
        span_items=SpanItemsContainer(
            monitor_items=MonitorItemsContainer(monitor_list=erspans)
        )
    )
    return model


def generate_xml() -> str:
    model = create_model()
    # Add operation attribute to specific elements
    element = model_dump_xml(
        model,
        wrappers=[
            XmlWrapper("System", "http://cisco.com/ns/yang/cisco-nx-os-device"),
        ],
    )
    monitor_items = element.find("./span-items/monitor-items")
    if monitor_items is not None:
        monitor_items.set("operation", "replace")
    return etree.tostring(element, encoding=str, pretty_print=True)
