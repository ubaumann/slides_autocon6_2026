


Checking yang path

```
uvx pyang -f tree Cisco-NX-OS-device.yang | wc -l
uvx pyang -f tree Cisco-NX-OS-device.yang --tree-depth=2 | grep --color=auto -E 'span|$' 
uvx pyang -f tree Cisco-NX-OS-device.yang --tree-path="/System/span-items"
```

generating the model
```
uv run pydantify -t "Cisco-NX-OS-device/System/span-items" Cisco-NX-OS-device.yang -o ~/iac_oss/slides_autocon6_2026/demo-02-yang-netconf/model
```



Pylance Type Checking Mode



config by hand
```
monitor session 10 type erspan-source
  description demo_AC6
  erspan-id 10
  vrf default
  destination ip 10.100.0.10
  source interface Service-Port-Channel512 both
```
