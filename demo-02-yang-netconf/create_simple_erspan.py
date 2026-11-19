from model.span import *


interfaces = [
    SourceintfListListEntry(
        direction=DirectionLeaf(SpanSrcdirectionType(EnumerationEnum7.both)),
        id="spo512",
    )
]
erspans = [
    MonitorListListEntry(
        type=TypeLeaf(SpanTypeType(EnumerationEnum2.erspan_dst)),
        id=10,
        config_state=ConfigstateLeaf(SpanStateType(EnumerationEnum4.down)),
        erspan_id=10,
        description="Demo AC6",
        vrf_name="default",
        destination_ip="10.100.0.10",  # type: ignore
        srcintf_items=SrcintfItemsContainer(source_intf_list=interfaces),
        fwd_drops_direction=None,
        header_type=HeadertypeLeaf(SpanHeaderverType(EnumerationEnum5.v3)),
    )
]

model = Model(
    span_items=SpanItemsContainer(
        monitor_items=MonitorItemsContainer(monitor_list=erspans)
    )
)

if __name__ == "__main__":
    # print(
    #     model.model_dump_json(
    #         by_alias=True,
    #         exclude_none=True,
    #         exclude_defaults=True,
    #         indent=2,
    #     )
    # )
    from lxml import etree
    from pydantify_common.helper import model_dump_xml, model_dump_xml_string

    print(model_dump_xml_string(model=model, pretty_print=True, data_root=True))

    # Add operation attribute to specific elements
    element = model_dump_xml(model)
    monitor_items = element.find('monitor-items')
    if monitor_items is not None:
        monitor_items.set('operation', 'replace')

    # Serialize to string
    print(etree.tostring(element, encoding=str, pretty_print=True))
