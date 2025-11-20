import re
from typing import List, Dict, Any


class NetlistProcessor:
    """
    Robust parser for KiCad/SKiDL S-expression netlists.
    """

    # ----------------------------------------------------------------------
    # TOKENIZER — FIXED to not split quoted strings containing spaces.
    # ----------------------------------------------------------------------
    @staticmethod
    def _tokenize_sexpr(text: str) -> List[str]:
        token_re = re.compile(r'''
            \(|\)                      # parentheses
            | "([^"]*)"               # quoted string (group 1 = content)
            | [^\s()]+                # atom
        ''', re.VERBOSE)

        tokens = []
        for m in token_re.finditer(text):
            if m.group(0) == '(' or m.group(0) == ')':
                tokens.append(m.group(0))
            elif m.group(1) is not None:
                tokens.append(m.group(1))  # keep full string content
            else:
                tokens.append(m.group(0))
        return tokens

    # ----------------------------------------------------------------------
    # PARSE TOKENS → TREE
    # ----------------------------------------------------------------------
    @staticmethod
    def _parse_tokens(tokens: List[str]):
        stack = []
        current = []
        for t in tokens:
            if t == '(':
                stack.append(current)
                current = []
            elif t == ')':
                parent = stack.pop()
                parent.append(current)
                current = parent
            else:
                current.append(t)

        if stack:
            raise ValueError("Unbalanced S-expression")

        return current[0]

    # ----------------------------------------------------------------------
    # FIND TAG
    # ----------------------------------------------------------------------
    @staticmethod
    def _find_tag(node, tag):
        """Return all sublists whose first element is tag."""
        results = []
        if isinstance(node, list):
            for sub in node:
                if isinstance(sub, list):
                    if len(sub) > 0 and sub[0] == tag:
                        results.append(sub)
                    results.extend(NetlistProcessor._find_tag(sub, tag))
        return results

    # ----------------------------------------------------------------------
    # Convert children of a node into key:value dict
    # ----------------------------------------------------------------------
    @staticmethod
    def _sexpr_object(items: List[List]) -> Dict[str, Any]:
        out = {}
        for entry in items:
            if not isinstance(entry, list) or len(entry) < 2:
                continue
            key = entry[0]
            if len(entry) == 2:
                out[key] = entry[1]
            else:
                out[key] = entry[1:]
        return out

    # ----------------------------------------------------------------------
    # MAIN PARSER
    # ----------------------------------------------------------------------
    @staticmethod
    def parse_netlist(text: str) -> Dict[str, Any]:
        if not text:
            return {'components': [], 'nets': [], 'metadata': {}}

        tokens = NetlistProcessor._tokenize_sexpr(text)
        tree = NetlistProcessor._parse_tokens(tokens)

        components = []
        nets = []

        # -----------------------------
        # COMPONENTS
        # -----------------------------
        comp_blocks = NetlistProcessor._find_tag(tree, "components")
        if comp_blocks:
            block = comp_blocks[0]

            for child in block[1:]:
                if isinstance(child, list) and len(child) > 0 and child[0] == "comp":

                    comp_obj = NetlistProcessor._sexpr_object(child[1:])

                    # Extract libsource
                    lib = None
                    part = None
                    if "libsource" in comp_obj and isinstance(comp_obj["libsource"], list):
                        ld = NetlistProcessor._sexpr_object(comp_obj["libsource"])
                        lib = ld.get("lib")
                        part = ld.get("part")

                    components.append({
                        "ref": comp_obj.get("ref"),
                        "value": comp_obj.get("value"),
                        "description": comp_obj.get("description"),
                        "lib": lib,
                        "part": part,
                        "raw": comp_obj
                    })

        # -----------------------------
        # NETS
        # -----------------------------
        net_blocks = NetlistProcessor._find_tag(tree, "nets")
        if net_blocks:
            block = net_blocks[0]

            for child in block[1:]:
                if isinstance(child, list) and len(child) > 0 and child[0] == "net":

                    net_obj = NetlistProcessor._sexpr_object(child[1:])
                    node_entries = []

                    for entry in child[1:]:
                        if isinstance(entry, list) and entry[0] == "node":
                            nd = NetlistProcessor._sexpr_object(entry[1:])
                            node_entries.append({"ref": nd.get("ref"), "pin": nd.get("pin")})

                    nets.append({
                        "name": net_obj.get("name"),
                        "code": net_obj.get("code"),
                        "nodes": node_entries,
                        "raw": net_obj
                    })

        # -----------------------------
        # COMPONENT → NET CONNECTIONS
        # -----------------------------
        comp_nets = {}
        for net in nets:
            for node in net["nodes"]:
                ref = node.get("ref")
                if ref:
                    comp_nets.setdefault(ref, []).append(net["name"])

        for c in components:
            c["nets"] = comp_nets.get(c["ref"], [])

        return {
            "components": components,
            "nets": nets,
            "metadata": {
                "total_components": len(components),
                "total_nets": len(nets)
            }
        }

    # ----------------------------------------------------------------------
    # VALIDATION
    # ----------------------------------------------------------------------
    @staticmethod
    def validate_netlist(parsed):
        errors = []
        warnings = []

        nets = parsed.get("nets", [])

        names = [n.get("name") for n in nets if n.get("name")]
        if not any(x in names for x in ("GND", "0", "Gnd")):
            errors.append("No ground reference found")

        for n in nets:
            name = n.get("name") or f"NET_{n.get('code')}"
            count = len(n.get("nodes", []))
            if count <= 1:
                warnings.append(f"Floating net: {name} (only {count} connection(s))")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
