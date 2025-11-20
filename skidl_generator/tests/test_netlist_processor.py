from processing.netlist_processor import NetlistProcessor

sample_netlist = """
(export
  (components
    (comp
      (ref "R1")
      (value "1k")
      (libsource (lib "Device") (part "R"))
    )
    (comp
      (ref "C1")
      (value "100n")
      (libsource (lib "Device") (part "C"))
    )
  )
  (nets
    (net (code 1) (name "GND") (node (ref "C1") (pin "2")))
    (net (code 2) (name "N1")  (node (ref "R1") (pin "1")))
    (net (code 3) (name "N2")  (node (ref "R1") (pin "2")) (node (ref "C1") (pin "1")))
  )
)
"""

print("Parsing sample netlist...")
parsed = NetlistProcessor.parse_netlist(sample_netlist)
print("Parsed components:", len(parsed['components']))
for comp in parsed['components']:
    print(" -", comp.get('ref'), "value=", comp.get('value'), "nets=", comp.get('nets'))

print("\nParsed nets:", len(parsed['nets']))
for net in parsed['nets']:
    print(" -", net.get('name'), "nodes=", net.get('nodes'))

print("\nValidating...")
val = NetlistProcessor.validate_netlist(parsed)
print("Valid:", val['valid'])
print("Errors:", val['errors'])
print("Warnings:", val['warnings'])

