from rich.console import Console
from rich.table import Table

from model.span import Model

json_data = """
{
  "Cisco-NX-OS-device:span-items": {
    "monitor-items": {
      "Monitor-list": [
        {
          "id": 10,
          "allowSharing": false,
          "configState": "down",
          "description": "demo_ac6",
          "destinationIp": "10.100.0.10",
          "erspanId": 10,
          "fwdDropsDirection": "none",
          "ipDscp": 0,
          "ipTtl": 255,
          "isFwdDropsRx": false,
          "isFwdDropsRxLowPriority": false,
          "isMarkerMilliSeconds": false,
          "isMarkerPacket": false,
          "markerPktInt": 100,
          "mtu": 10240,
          "srcintf-items": {
            "SourceIntf-list": [
              {
                "id": "spo512",
                "allowPfc": false,
                "direction": "both"
              }
            ]
          },
          "type": "erspan-source",
          "vrfName": "default"
        }
      ]
    }
  }
}
"""

span = Model.model_validate_json(json_data)
print(span.model_dump_json(by_alias=True, exclude_defaults=True, indent=2))


table = Table(title="SPAN")

table.add_column("ID", justify="right", style="cyan", no_wrap=True)
table.add_column("Type", style="magenta")
table.add_column("Interfaces", justify="right", style="green")


if (
    span.span_items != None
    and span.span_items.monitor_items != None
    and span.span_items.monitor_items.monitor_list != None
):
    for span_item in span.span_items.monitor_items.monitor_list:
        if (
            span_item.type != None
            and span_item.srcintf_items != None
            and span_item.srcintf_items.source_intf_list
        ):
            table.add_row(
                str(span_item.id),
                span_item.type.root.root.value,
                ";".join([x.id for x in span_item.srcintf_items.source_intf_list]),
            )

console = Console()
console.print(table)
