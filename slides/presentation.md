---
marp: true
theme: default
class: invert
math: mathjax
paginate: true
footer: "Pydantify | AutoCon6 2026"
---

# I 💖 YANG. Said No Python Developer Ever

*Urs Baumann* | *AutoCon6 2026*


---

# Dedective Dylan

<style>
  .container {
    display: flex;
  }
  .col {
    flex: 1;
  }
</style>
<div class="container">
<div class="col">
<ul>
<li>Needs to inspect network traffic</li>
<li>Wants to automate ERSPAN deployment</li>
</ul>
</div>
<div class="col">
<img src="img/dedective.jpg" alt="Detective" height="500px">
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
