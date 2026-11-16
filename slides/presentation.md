---
marp: true
theme: default
class: invert
math: mathjax
paginate: true
# footer: "Pydantify | AutoCon6 2026"
style: |
  .container {
    display: flex;
  }
  .col {
    flex: 1;
  }
---

# I 💖 YANG. Said No Python Developer Ever

*Urs Baumann* | *AutoCon6 2026*


---

# Detective Dylan
<div class="container">
<div class="col">
<ul>
<li>Needs to inspect network traffic</li>
<li>Wants to automate ERSPAN deployment</li>
</ul>
</div>
<div class="col">
<img src="img/detective.jpg" alt="Detective" height="500px">
</div>

---

# ERSPAN

```
monitor session 10 type erspan-source
  description AutoCon6 2026 Demo
  erspan-id 10
  vrf rspan_net
  destination ip 20.26.11.17
  source interface Service-Port-Channel512 both
```

---

# Triggerd by Events

```jinja
{% for session in erspan_sessions %}
no monitor session {{ id }}
monitor session {{ id }} type erspan-source
  description {{ session.description }}
  erspan-id {{ session.erspan_id }}
  vrf rspan_net
  destination ip 20.26.11.17
  source interface {{ session.source_interface }} {{ session.direction }}
{% endfor %}
```

---

# CLI and Template Challenges

<!--
🔲 Testing and validation
🔲 Complex logic
🔲 Transcactions
🔲 Candidate store
🔲 Deprovisioning
-->
<!-- Yes some CLI features can help (commit/rollback) -->
---

# The Template Trap

```shell
switch(config-erspan-src)# description ?
  LINE  Enter the description string(can include spaces)

switch(config-erspan-src)# description aaaaaaaaaabbbbbbbbbbccccccccccdddddddddd
ERROR: Description string too long (max 32 characters)

switch(config-erspan-src)# destination typo
                                          ^
% Invalid command at '^' marker.
```


<sub>*Strings are easy to generate, hard to validate.*</sub>

---

## CLI is not designed for automation. It is designed for humans.

---

# What does the rest of the world do?

- REST API
  - Cloud providers
  - Hypervisors
- gRPC
  - Talos (Sidero)
- GraphQL
  - Infrahub

<!--
Rest API, RPC, graphQL, ...
 -->

---

# NETCONF / RESTCONF / gNMI

- [RFC 4741: NETCONF Protocol](https://www.rfc-editor.org/info/rfc4741/)
  - 2006
  - RFC 6241 (2011) obsoletes RFC 4741
- [RFC 8040: RESTCONF Protocol](https://www.rfc-editor.org/info/rfc8040/)
- [gNMI Specification github.com/openconfig](https://github.com/openconfig/reference/blob/master/rpc/gnmi/gnmi-specification.md)

---

# Properties

- Transaction Based
- Atomic Operations
- Datastores
- Hierarchical Data Model

<sub>*What about RESTCONF? - [RFC 8072: YANG Patch Media Type](https://www.rfc-editor.org/info/rfc8072/)*</sub>
<!--
- Lock
- Validate
- Commit
-->

---

# "Clear" Error Messages

```xml
<rpc-error>
  <error-type>application</error-type>
  <error-tag>invalid-value</error-tag>
  <error-severity>error</error-severity>
  <error-message>
    Description string too long (max 32 characters)
  </error-message>
</rpc-error>
```


---

# How Engineers Work with YANG Today

```django
<config>
<if:interfaces xmlns:if="urn:ietf:params:xml:ns:yang:ietf-interfaces">
{% for interface in vlan_interfaces %}
  <if:interface>
    <if:name>Vlanif{{ interface.name }}</if:name>
    <ip:ipv4 xmlns:ip="urn:ietf:params:xml:ns:yang:ietf-ip">
      <ip:address>{{ interface.ip.split("/")[0] }}</ip:ip>
      <ip:prefix-length>{{ interface.ip.split("/")[1] }}</ip:prefix-length>
    </ip:ipv4>
  </if:interface>
{% endfor %}
</if:interfaces>
</config>
```

**Jinja templates generate XML, but validate nothing until the device rejects it.**
<sub>*Yes, XML can be validated with tools like yanglint.*</sub>
<!--

-->

---

# Would you do this?

```python
from jinja2 import Template

template = Template("""{
  "username": "{{ username }}",
  "password": "{{ password }}"
}""")

payload = template.render(username="admin", password="S3cret!")
```

---

# Demo Time

<!--
FastAPI -> JSONSchema -> SDK
-->

---


# What We Want

✅ Python objects with typing, validation, and documentation  
✅ IDE autocomplete on configuration paths  
✅ IDE error highlighting before runtime  
✅ Type hints for `mypy` verification  
✅ Serialization / deserialization at boundaries  
✅ Catch errors before any RPC is sent  

---

# Existing Ecosystem

| Tool | Status | Language |
|------|--------|----------|
| [`pyangbind`](https://github.com/robshakir/pyangbind) | Mature | Python |
| [`ygot`](https://github.com/openconfig/ygot) | Active | Go |
| [`ydk-gen`](https://github.com/CiscoDevNet/ydk-gen) | Maintenance | Multi |

**Why not Pydantic?**

---

# Pydantify: The Journey

📅 **2023** – Midterm Project @ Eastern Switzerland University  
Walther & Jovicic, *"Make Model Driven Network Automation Pythonic"*

📦 **v0.5.0** (Dec 2022) – First public version  
📦 **v0.6.0** (Oct 2024) – Pydantic v2 support  
📦 **v0.7.0** (Jan 2025) – Improved decimal64 types  
📦 **v0.8.0** (Feb 2025) – Fixed mandatory list keys  

---

# Pydantify Now

- 📄 Documentation: [`pydantify.github.io/pydantify/`](https://pydantify.github.io/pydantify/)
- 💻 GitHub: [`github.com/pydantify/pydantify`](https://github.com/pydantify/pydantify)
- 📊 Downloads: [`pypistats.org/packages/pydantify`](https://pypistats.org/packages/pydantify)


---

# From YANG Tree to Python

```
module: my-endpoint
  +--rw endpoint
     +--rw address        string
     +--rw port           port
     +--rw description?   string
```

↓

```json
{
  "my-endpoint:endpoint": {
    "address": "::1",
    "port": 2222,
    "description": "Port 2222 on localhost"
  }
}
```

---

# The Pydantic Model (Generated)

```python
class EndpointContainer(BaseModel):
    """Definition of an endpoint"""
    model_config = ConfigDict(populate_by_name=True, regex_engine="python-re")

    address: Annotated[str, Field(alias="my-endpoint:address")]
    """Endpoint address. IP or FQDN"""

    port: Annotated[
        int, Field(alias="my-endpoint:port", ge=1, le=65535)
    ]
    """Port number between 1 and 65535"""

    description: Annotated[
        Optional[str], Field(alias="my-endpoint:description")
    ] = None
    """Endpoint description"""
```

---

# Creating Configuration (Pythonic)

```python
from endpoint import Model, EndpointContainer

port = 8080
host = "localhost"

endpoint1 = Model(
    endpoint=EndpointContainer(address=host, port=port)
)

json_output = endpoint1.model_dump_json(indent=2, exclude_none=True)
```

**Validation happens at instantiation!**

---

# Validation Error (IDE Time)

```python
endpoint_invalid = Model(
    endpoint=EndpointContainer(address=host, port=99999)
)
# ❌ ValidationError: 99999 is greater than maximum 65535
```

**Caught before the first RPC.**

---

# The Pipeline

![Pydantify Workflow](img/pydantify_workflow.png)

---

# Demo Time

<!--
Generate Pydantic models from YANG, validate, and serialize to XML
Configure ERSPAN on a switch using Pydantify
-->

---

# Unsupported / Challenging

❌ Context-aware validation (must/if/xPath)  
❌ `bits` and `decimal64` edge cases  
❌ Complex regular expressions  
❌ Reference validation without device state  

**These remain the device's responsibility.**

---

# The "empty" Type

RFC 7951 Section 6.9:

> An "empty" value is represented as `[null]`, an array with the `"null"` literal being its only element.

```yang
leaf foo {
  type empty;
}
```

```json
"foo": [null]
```

---

# The "empty" Type

RFC 7951 Section 6.9:

> An "empty" value is represented as `[null]`, an array with the `"null"` literal being its only element.

```python
class InterfaceContainer(BaseModel):
    primary: Annotated[
        Optional[List[None]],
        Field(alias="interface:primary", max_length=1, min_length=1),
    ] = None
```

**A workaround that preserves Pydantic compatibility.**

---

# Key Takeaways

| What Works ✅ | What Doesn't ❌ |
|---------------|-----------------|
| Range constraints | `must` / `if` conditions |
| Enum/identity types | xPath expressions |
| Nested structures | Device-state validation |
| Serialization to NETCONF | Idempotency/reconciliation |

**Validate early, serialize at the boundary.**

---

# Closing Message

> If your output is structured data, stop treating it like a string.
>
> Use the schema. Generate the models. Validate before you send.

---

# Questions?

Thank you!

---
# Resources

- 🔗 [`pydantify.github.io/pydantify/`](https://pydantify.github.io/pydantify/)
- 💻 [`github.com/pydantify/pydantify`](https://github.com/pydantify/pydantify)
- 👔 [`linkedin.com/in/ubaumannch`](https://www.linkedin.com/in/ubaumannch)

---

# Vendor Adoption

- 🌐 [`srl-labs/pydantic-srlinux/`](https://github.com/srl-labs/pydantic-srlinux/) – Experimental SRLinux models
- 🎥 [Roman Dodin (Nokia) Demo](https://www.youtube.com/watch?v=CM3sT55zwt0) – How to use Pydantify

---

# Backup Slides

---

# YANG

---

## YANG Example

```yang
module my-endpoint {
    namespace "http://pydantify.github.io/ns/yang/pydantify-endpoint";
    prefix "ep";

    container endpoint {
        leaf name {
            type string;
        }
    }
}
```

```
module: my-endpoint
  +--rw endpoint
     +--rw name        string
```

---

## YANG

- Data Modeling Language
- Definition of data sent over network management protocols
- Allows vendor-specific data definitions
- https://github.com/YangModels/yang
- IETF, RFC 6020, RFC 7950
- IEEE YANG Guidelines

---

## OpenConfig

- Vendor-neutral YANG Model
- Collaborative effort by network operators
- Vendor-neutral
- https://github.com/openconfig/public
- https://openconfig.net/projects/models/

---

## YANG Leaf Statement

<div class="container">
<div class="col">

- One value
- No children
- One instance
- Data Constraints
  - config
  - default
  - mandatory
  - must
  - type

</div>
<div class="col">

```yang
leaf hostname {
    type string;
    description "Device Name"
}
leaf version {
    type string;
    config false;
    description "OS Version"
}
```
```xml
<hostname>sw01</hostname>
<version>16.6.2</version>
```

</div>
</div>

---

## YANG Leaf-List Statement

<div class="container">
<div class="col">

- One value
- No children
- Multiple instances
- Data Constraints
  - max/min elements
  - ordered-by
  - config
  - default
  - mandatory
  - must
  - type

</div>
<div class="col">

```yang
leaf-list interface {
    type string;
    config true;
    description "Interface Name"
}
```
```xml
<interface>Ethernet0/1</interface>
<interface>Ethernet0/2</interface>
<interface>Ethernet0/3</interface>
<interface>Ethernet0/4</interface>
```

</div>
</div>

---

## YANG Container Statement

<div class="container">
<div class="col">

- Non-leaf nodes
- One instance
- No semantic value
  - Exception presence
- Constraints
  - if-feature
  - config
  - must
  - uses
  - when

</div>
<div class="col">

```yang
container time {
    leaf hour {
        type uint8;
        config false;
    }
    leaf minute {
        type uint8;
        config false;
    }
}
```
```xml
<time>
    <hour>10</hour>
    <minute>50</minute>
</time>
```

</div>
</div>

---

## YANG List Statement

<div class="container">
<div class="col">

- Non-leaf nodes
- Multiple instances
- Attributes
  - max-elements
  - min-elements
  - ordered-by

</div>
<div class="col">

```yang
list user {
    key "name";
    leaf name {
        type string;
    }
    leaf full-name {
        type string;
    }
}
```
```xml
<user>
<name>taylor</name>
<full-name>Taylor Swift</full-name>
</user>
<user>
<name>urs</name>
<full-name>Urs Baumann</full-name>
</user>
```

</div>
</div>

---

## YANG Types

<div class="container">
<div class="col">

- int8/16/32/64
- uint8/16/32/64
- decimal64
- string
- enumeration
- boolean
- bits
- binary
- leafref
- typedef

</div>
<div class="col">

```yang
typedef percent {
    type uint8 {
        range "0 .. 100"
    }
    description "Percentage";
}
leaf completed {
    type percent;
}
```
```xml
<completed>90</completed>
```

</div>
</div>

---

## YANG Grouping Statement

<div class="container">
<div class="col">

```yang
grouping endpoint {
    leaf address {
        type inet:ip-address;
    }
    leaf port {
        type ient:port-number;
    }
}
container peer {
    container destination {
        uses endpoint;
    }
}
```

</div>
<div class="col">

```xml
<peer>
<destination>
<address>10.0.0.1</address>
<port>443</port>
</destination>
</peer>
```

</div>
</div>

---

## pyang

```shell
$ pyang ietf-interfaces.yang -f tree --tree-path interfaces/interface

module: ietf-interfaces
  +--rw interfaces
     +--rw interface* [name]
        +--rw name                        string
        +--rw description?                string
        +--rw type                        identityref
        +--rw enabled?                    boolean
        +--rw link-up-down-trap-enable?   enumeration {if-mib}?
```

---

## pyang

```shell
$ pyang -f tree --tree-depth=2 ietf-interfaces.yang

module: ietf-interfaces
  +--rw interfaces
  |  +--rw interface* [name]
  |        ...
  +--ro interfaces-state
     +--ro interface* [name]
           ...
```

---

## pyang

```shell
pyang ietf-interfaces.yang -f sample-xml-skeleton \
--sample-xml-skeleton-path=interfaces/interface
```
```xml
<?xml version='1.0' encoding='UTF-8'?>
<data xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface>
      <name/>
      <description/>
      <type/>
      <link-up-down-trap-enable/>
    </interface>
  </interfaces>
</data>
```

---

## Netconf

```text
+-------------+      +-----------------------------+
(4) |   Content   |      |     Configuration data      |
    +-------------+      +-----------------------------+
           |                           |
    +-------------+      +-----------------------------+
(3) | Operations  |      | <get-config>, <edit-config> |
    +-------------+      +-----------------------------+
           |                           |
    +-------------+      +-----------------------------+
(2) |     RPC     |      |    <rpc>, <rpc-reply>       |
    +-------------+      +-----------------------------+
           |                           |
    +-------------+      +-----------------------------+
(1) |  Transport  |      |   BEEP, SSH, SSL, console   |
    |   Protocol  |      |                             |
    +-------------+      +-----------------------------+
```

https://datatracker.ietf.org/doc/html/rfc4741#section-1.1

---

## NETCONF

- Network Configuration Protocol
- RPC Model (`rpc`, `rpc-reply`, `rpc-error`, `ok`)
- Protocol Operations
- Transaction Based
- https://datatracker.ietf.org/doc/html/rfc6241
- IETF, RFC 4741, RFC 6241

---

## ncclient

<div class="container">
<div class="col">

- ncclient
- NETCONF clients
- rfc6241
- https://ncclient.readthedocs.io/

</div>
<div class="col">

<div style="text-align:center;">
  <p><strong>ncclient</strong></p>
  <p><em>Client library for NETCONF</em></p>
</div>

</div>
</div>

---

## ncclient — get config

```python
from ncclient import manager, xml_

with manager.connect(host=host, username=username, password=password,
                     port=port, hostkey_verify=hostkey_verify) as m:

    response = m.get_config(source="running")
    print(xml_.to_xml(response.data, pretty_print=True))
```

---

## ncclient — get

```python
from ncclient import manager, xml_

filter_interface = """
    <native>
        <interface>
        </interface>
    </native>"""

with manager.connect(host=host, username=username, password=password,
                     port=port, hostkey_verify=hostkey_verify) as m:

    response = m.get(filter=("subtree", filter_interface))
    print(xml_.to_xml(response.data, pretty_print=True))
```

---

## ncclient — get

```python
from ncclient import manager, xml_

with manager.connect(host=host, username=username, password=password,
                     port=port, hostkey_verify=hostkey_verify) as m:

    response = m.get(filter=("xpath", "/native/banner/exec"))
    print(xml_.to_xml(response.data, pretty_print=True))
```

---

## ncclient — locked

```python
from ncclient import manager

with manager.connect(host=host, username=username, password=password,
                     port=port, hostkey_verify=hostkey_verify) as m:

    m.lock("running")
    ...
    m.unlock("running")

    with m.locked("running"):
        ...
```

---

## ncclient — edit config

```python
from ncclient import manager, xml_

set_exec_banner = """
    <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <banner>
          <exec>
            <banner>NetAut</banner>
          </exec>
        </banner>
      </native>
    </config>"""

with manager.connect(host=host, username=username, password=password,
                     port=port, hostkey_verify=hostkey_verify) as m:

    response = m.edit_config(target="running", config=set_exec_banner)
    print(xml_.to_xml(response.xml, pretty_print=True))
```

---

## ncclient — delete operation

```python
from ncclient import manager, xml_

del_exec_banner = """
    <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <banner>
          <exec operation="delete" />
        </banner>
      </native>
    </config>"""

with manager.connect(host=host, username=username, password=password,
                     port=port, hostkey_verify=hostkey_verify) as m:

    response = m.edit_config(target="running", config=del_exec_banner)
    print(xml_.to_xml(response.xml, pretty_print=True))
```

---

## Scrapli

<div class="container">
<div class="col">

- Zig library
- Synchronous and asynchronous
- Python and Go
- https://carlmontanari.github.io/scrapli/

</div>
<div class="col">

<div style="text-align:center;">
  <p><strong>scrapli</strong></p>
  <p><em>scrapli -- scrap(e c)li -- is a set of libraries created to interact with devices via the CLI, and NETCONF.</em></p>
</div>

</div>
</div>

---

## scrapli — get config

```python
from scrapli import AuthOptions, Netconf
from scrapli.netconf import DatastoreType

with Netconf(host=host,
             auth_options=AuthOptions(username=user, password=pw)) as conn:

    result = conn.get_config(source=DatastoreType.RUNNING)
    print(result.result)
```

---

## scrapli — edit config

```python
from scrapli import AuthOptions, Netconf
from scrapli.netconf import DatastoreType

with Netconf(host=host,
             auth_options=AuthOptions(username=user, password=pw)) as conn:

    set_exec_banner = """<config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <banner>
          <exec><banner>NetAut</banner></exec>
        </banner>
      </native>
    </config>"""

    conn.lock(target=DatastoreType.CANDIDATE)
    result = conn.edit_config(config=set_exec_banner, target=DatastoreType.CANDIDATE)
    conn.unlock(target=DatastoreType.CANDIDATE)
    print(result)
```

---

## xmltodict

```python
import json
import xmltodict
from xml.etree import ElementTree

print(
  json.dumps(
    xmltodict.parse(result.result),
    indent=4
  )
)
print(
  json.dumps(
    xmltodict.parse(
      ElementTree.tostring(result.xml_input)
      ),
    indent=4
  )
)
```

---

## pyGNMI

<div class="container">
<div class="col">

- pygnmi
- Capabilities
- Get
- Set
- Subscribe
- https://github.com/akarneliuk/pygnmi

</div>
<div class="col">

<div style="text-align:center;">
  <p><strong>gNMI</strong></p>
  <p><em>gRPC Network Management Interface</em></p>
</div>

</div>
</div>

---

## pyGNMI — get

```python
from pygnmi.client import gNMIclient

paths = [
    'openconfig-interfaces:interfaces',
    'openconfig-network-instance:network-instances'
]
with gNMIclient(target=(host["ip_address"], host["port"]), username=host["username"],
                password=host["password"], insecure=True) as gc:

    result = gc.get(path=paths, encoding='json')
```

---

# YANG to Pydantic Model

<sub>*Examples: [https://github.com/pydantify/pydantify/tree/main/tests/examples](https://github.com/pydantify/pydantify/tree/main/tests/examples)*</sub>

---

# Leaf List

<div class="container">
<div class="col">

```yang
module interfaces {
  namespace
  "http://ultraconfig.com.au/ns/yang/ultraconfig-interfaces";
  prefix if;
  description 'Example demonstarating leafref nodes';

  list interfaces {
    key "name";
    description "List of configured device interfaces";
    leaf name {
      type string;
      description "Interface name";
    }
    leaf-list ip {
      type string;
      description "List of interface IPs";
    }
  }
}
```

</div>
<div class="col">

```python
class InterfacesListEntry(BaseModel):
    """
    List of configured device interfaces
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = (
        "http://ultraconfig.com.au/ns/yang/ultraconfig-interfaces"
    )
    prefix: ClassVar[Optional[str]] = "if"

    name: Annotated[str, Field(alias="interfaces:name")]
    """
    Interface name
    """
    ip: Annotated[Optional[List[str]], Field(alias="interfaces:ip")] = []
    """
    List of interface IPs
    """

```

</div>
</div>

---

# Typedef

```yang
  typedef dotted-quad {
    type string {
      pattern
        '(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])';
    }
    description
      "Four octets written as decimal numbers and separated with the '.' (full stop) character.";
  }
# <omitted for brevity>
      leaf subnet-mask {
        type dotted-quad;
        mandatory "true";
        description
          "Interface subnet mask. Example value: 255.255.255.0";
      }
```

```python
subnet_mask: Annotated[
    str,
    Field(
        alias="interfaces:subnet-mask",
        pattern="^(?=^(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$).*$",
    ),
]
"""
Interface subnet mask. Example value: 255.255.255.0
"""
```

---

# Union

<div class="container">
<div class="col">

```yang
module interfaces {

  namespace
  "http://ultraconfig.com.au/ns/yang/ultraconfig-interfaces";

  prefix if;

  description 'Example demonstarating leafref nodes';

  container interfaces {
    description 'Just a simple example of a container.';

    leaf union_leaf {
        type union {
          type int32;
          type string;
        }
        mandatory "true";
        description
            "Number or 'unbounded'";
    }
  }
}

```

</div>
<div class="col">

```python
class UnionLeafLeaf1(RootModel[int]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: Annotated[int, Field(ge=-2147483648, le=2147483647)]
    """
    Number or 'unbounded'
    """

class InterfacesContainer(BaseModel):
    """
    Just a simple example of a container.
    """
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = (
        "http://ultraconfig.com.au/ns/yang/ultraconfig-interfaces"
    )
    prefix: ClassVar[Optional[str]] = "if"
    union_leaf: Annotated[
        Union[UnionLeafLeaf1, str], Field(alias="interfaces:union_leaf")
    ]
    """
    Number or 'unbounded'
    """
```

</div>
</div>

---

# decimal64

<div class="container">
<div class="col">

```yang
module interfaces {
  namespace
  "http://ultraconfig.com.au/ns/yang/ultraconfig-interfaces";

  prefix if;

  description 'Example using just leafs, containers and modules';

  container interfaces {
    description 'Just a simple example of a container.';

    leaf name {
        type string;
        mandatory "true";
        description
            "Interface name. Example value: GigabitEthernet 0/0/0";
    }

    leaf counter1 {
        type decimal64 {
          range "-20..3";
          fraction-digits 1;
        }
        config "false";
        description
            "Pkt Counter 1";
    }
  }
}

```

</div>
<div class="col">

```python
class InterfacesContainer(BaseModel):
    """
    Just a simple example of a container.
    """
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = (
        "http://ultraconfig.com.au/ns/yang/ultraconfig-interfaces"
    )
    prefix: ClassVar[Optional[str]] = "if"
    name: Annotated[str, Field(alias="interfaces:name")]
    """
    Interface name. Example value: GigabitEthernet 0/0/0
    """
    counter1: Annotated[
        Optional[float], Field(alias="interfaces:counter1", ge=-20.0, le=3.0)
    ] = None
    """
    Pkt Counter 1
    """
class Model(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[Optional[str]] = (
        "http://ultraconfig.com.au/ns/yang/ultraconfig-interfaces"
    )
    prefix: ClassVar[Optional[str]] = "if"
    interfaces: Annotated[
        Optional[InterfacesContainer], Field(alias="interfaces:interfaces")
    ] = None
```

</div>
</div>

---

# Demo 1

---

# OpenAPI Best Practices

[https://learn.openapis.org/best-practices.html](https://learn.openapis.org/best-practices.html)

> Traditionally, two main approaches exist when creating OADs: Code-first and Design-first.
> There have been a number of heated debates over the relative merits of these two approaches but, in the opinion of the OpenAPI Initiative (OAI), the importance of using Design-first cannot be stressed strongly enough.

---

# Generating SDKs

[https://fastapi.tiangolo.com/advanced/generate-clients/](https://fastapi.tiangolo.com/advanced/generate-clients/)

```bash
npx @hey-api/openapi-ts -i http://localhost:8000/openapi.json -o src/client
```

---

# Demo 2

---

# YANG Path

```shell
pyang -f tree Cisco-NX-OS-device.yang --tree-path="/System/span-items"
```

```shell
module: Cisco-NX-OS-device
  +--rw System
     +--rw span-items
        +--ro operSt?          nw_EntOperSt
        +--rw monitor-items
           +--rw Monitor-list* [id]
              +--rw type?                      span_Type
              +--ro operState?                 span_OperStQual
              +--rw configState?               span_State
              +--rw description?               span_Description
              +--rw vrfName?                   l3_VrfName
              +--rw aclName?                   span_AclName
              +--rw id                         span_SsnId
<omitted for brevity>
```

---

# Generate Pydantic Models

```shell
pydantify -t "Cisco-NX-OS-device/System/span-items" Cisco-NX-OS-device.yang
```

---

# The END
