"""Vocabulary + record validator (deterministic; no LLM).

Vocab loads design/vocab_v1.json, renders it for the prompt, validates a record returned by
the translator, and accepts new terms (controlled extension: a new facet leaf needs an
existing parent; a new action needs a type).
"""

import difflib
import json
import re
from pathlib import Path

VOCAB_PATH = Path(__file__).resolve().parent / "design" / "vocab_v1.json"
SCOPE_FACETS = ("task", "medium", "artifact")
MODALITIES = ("O", "F", "P", "Pref")
NAME = re.compile(r"^[a-z][a-z0-9_]*$")
NEGATED = re.compile(r"^(no|not|never|avoid|skip|dont|without)_")


class Vocab:
    def __init__(self, path=VOCAB_PATH):
        raw = json.loads(Path(path).read_text())
        self.facets = raw["facets"]                       # nested: dict = parent, str = leaf
        self.actions = {}                                 # name -> {type, values?, doc, group}
        for group, items in raw["actions"].items():
            if group.startswith("_"):
                continue
            for name, spec in items.items():
                self.actions[name] = {**spec, "group": group}
        self.additions = []                               # log of accepted new terms

    # ---- lookups -------------------------------------------------------------------------
    def terms(self, facet):
        """All term names of a facet (parents and leaves) -> True if parent."""
        out = {}

        def walk(node):
            for k, v in node.items():
                if k == "_doc":
                    continue
                out[k] = isinstance(v, dict)
                if isinstance(v, dict):
                    walk(v)
        walk(self.facets[facet])
        return out

    def leaves(self, facet, term):
        """Leaf names covered by a term (a leaf covers itself)."""
        def find(node):
            for k, v in node.items():
                if k == "_doc":
                    continue
                if k == term:
                    return v
                if isinstance(v, dict):
                    r = find(v)
                    if r is not None:
                        return r
            return None

        def collect(name, node):
            if not isinstance(node, dict):
                return [name]
            return [l for k, v in node.items() if k != "_doc" for l in collect(k, v)]
        node = self.facets[facet] if term == facet else find(self.facets[facet])
        return collect(term, node) if node is not None else []

    def descendants(self, facet, term):
        """All terms below a term (children, grandchildren, ...)."""
        def find(node):
            for k, v in node.items():
                if k == "_doc":
                    continue
                if k == term:
                    return v
                if isinstance(v, dict):
                    r = find(v)
                    if r is not None:
                        return r
            return None

        def walk(node):
            out = []
            for k, v in node.items():
                if k != "_doc":
                    out.append(k)
                    if isinstance(v, dict):
                        out += walk(v)
            return out
        node = find(self.facets[facet])
        return walk(node) if isinstance(node, dict) else []

    def groups(self):
        return sorted({a["group"] for a in self.actions.values()})

    # ---- prompt rendering ----------------------------------------------------------------
    def render(self):
        lines = ["### Facets (indented = child; a parent covers its children)"]

        def walk(node, depth):
            for k, v in node.items():
                if k == "_doc":
                    continue
                doc = v.get("_doc", "") if isinstance(v, dict) else v
                lines.append(f"{'  ' * depth}- {k}: {doc}")
                if isinstance(v, dict):
                    walk(v, depth + 1)
        for facet, tree in self.facets.items():
            lines.append(f"{facet}  ({tree.get('_doc', '')})")
            walk(tree, 1)
        lines.append("\n### Actions (name [type]: meaning), by group")
        for g in self.groups():
            lines.append(f"{g}")
            for name, a in self.actions.items():
                if a["group"] != g:
                    continue
                t = a["type"] + (f" {a['values']}" if a["type"] == "enum" else "")
                lines.append(f"  - {name} [{t}]: {a.get('doc', '')}")
        return "\n".join(lines)

    # ---- controlled extension ------------------------------------------------------------
    def _similar(self, name, pool):
        return difflib.get_close_matches(name, [p for p in pool if p != name], n=2, cutoff=0.8)

    def check_new_term(self, t, confirmed):
        """Errors for one proposed term ([] = acceptable)."""
        name = t.get("name", "")
        if not isinstance(name, str) or not NAME.match(name):
            return [f"new term name '{name}' must be snake_case"]
        if t.get("kind") == "facet":
            facet = t.get("facet")
            if facet not in self.facets:
                return [f"new term '{name}': unknown facet '{facet}'"]
            terms = self.terms(facet)
            if name in terms:
                return [f"new term '{name}' already exists in facet '{facet}': use it, do not re-add it"]
            parent = t.get("parent")
            if parent != facet and not terms.get(parent, False):
                return [f"new term '{name}': parent '{parent}' is not an existing parent term of facet "
                        f"'{facet}' (parents: {[facet] + [k for k, p in terms.items() if p]})"]
            near = self._similar(name, terms)
        elif t.get("kind") == "action":
            if name in self.actions:
                return [f"new action '{name}' already exists: use it, do not re-add it"]
            if NEGATED.match(name):
                return [f"new action '{name}' is negated: name the positive behavior and use modality F"]
            if t.get("type") not in ("bool", "int", "enum"):
                return [f"new action '{name}': type must be bool, int, or enum"]
            if t["type"] == "enum" and not (isinstance(t.get("values"), list) and len(t["values"]) >= 2):
                return [f"new action '{name}': an enum needs a 'values' list with at least 2 values"]
            if t.get("group") not in self.groups():
                return [f"new action '{name}': group must be one of {self.groups()}"]
            near = self._similar(name, self.actions)
        else:
            return [f"new term '{name}': kind must be 'facet' or 'action'"]
        if near and name not in confirmed:
            return [f"new term '{name}' looks like existing {near}. Reuse the existing term if it has the "
                    f"same meaning; if it is really different, send the same new term again."]
        return []

    def add(self, t, source):
        if t["kind"] == "facet":
            def find(node, key):
                for k, v in node.items():
                    if k == key and isinstance(v, dict):
                        return v
                    if isinstance(v, dict):
                        r = find(v, key)
                        if r is not None:
                            return r
                return None
            parent = self.facets[t["facet"]] if t["parent"] == t["facet"] else find(self.facets[t["facet"]], t["parent"])
            parent[t["name"]] = t.get("doc", "")
        else:
            spec = {"type": t["type"], "doc": t.get("doc", ""), "group": t["group"]}
            if t["type"] == "enum":
                spec["values"] = t["values"]
            self.actions[t["name"]] = spec
        self.additions.append({**t, "source": source})

    # ---- record validation ---------------------------------------------------------------
    def validate(self, rec, confirmed=()):
        """Return (errors, new_terms_to_add). confirmed = new-term names already pushed back once."""
        if not isinstance(rec, dict):
            return ["the reply must be one JSON object"], []
        if rec.get("fits") is False:
            ok = isinstance(rec.get("unfit_reason"), str) and rec["unfit_reason"].strip()
            return ([] if ok else ["fits=false needs a one-sentence unfit_reason"]), []
        errors, new = [], []
        for t in (rec.get("new_terms") if isinstance(rec.get("new_terms"), list) else []):
            e = self.check_new_term(t, confirmed) if isinstance(t, dict) else ["each new term must be an object"]
            errors += e
            if not e:
                new.append(t)
        if not isinstance(rec.get("new_terms") or [], list):
            errors.append("new_terms must be a list")
        new_facet = {(t["facet"], t["name"]) for t in new if t["kind"] == "facet"}
        new_action = {t["name"]: t for t in new if t["kind"] == "action"}

        def known(facet, term):
            if not isinstance(term, str):   # the model sometimes returns an object instead of a name
                return False
            return term in self.terms(facet) or (facet, term) in new_facet

        if not known("actor", rec.get("actor")):
            errors.append(f"actor '{rec.get('actor')}' is not an actor term")
        scope = rec.get("scope")
        if not isinstance(scope, dict):
            errors.append("scope must be an object with task, medium, artifact lists")
        else:
            for facet in SCOPE_FACETS:
                vals = scope.get(facet, [])
                if not isinstance(vals, list):
                    errors.append(f"scope.{facet} must be a list")
                    continue
                for v in vals:
                    if not known(facet, v):
                        errors.append(f"scope.{facet}: '{v}' is not a {facet} term")
                for v in vals:   # a list means ANY of its terms, so a parent swallows its child
                    kids = [c for c in vals if isinstance(v, str) and isinstance(c, str) and c in self.descendants(facet, v)]
                    if kids:
                        errors.append(f"scope.{facet} lists '{v}' together with its child term(s) {kids}. A list means "
                                      f"ANY of its terms, so '{v}' already covers them. Keep only the narrowest "
                                      f"term(s) the rule is about.")
            for k in scope:
                if k not in SCOPE_FACETS:
                    errors.append(f"scope has unknown facet '{k}' (allowed: {list(SCOPE_FACETS)})")
        for key in ("when", "unless"):
            for c in rec.get(key) or []:
                if not (isinstance(c, dict) and known("situation", c.get("situation")) and isinstance(c.get("value"), bool)):
                    errors.append(f"{key}: each item must be {{'situation': <situation term>, 'value': true|false}}; got {c}")
        if rec.get("modality") not in MODALITIES:
            errors.append(f"modality must be one of {list(MODALITIES)}")
        act = rec.get("action")
        if not isinstance(act, dict) or not isinstance(act.get("name"), str):
            errors.append("action must be an object with a 'name'")
        else:
            spec = self.actions.get(act["name"]) or new_action.get(act["name"])
            if spec is None:
                errors.append(f"action '{act['name']}' is not in the vocabulary (reuse an existing action, "
                              f"or add it under new_terms)")
            elif spec["type"] == "enum":
                if act.get("value") not in spec["values"]:
                    errors.append(f"action '{act['name']}' is an enum: 'value' must be one of {spec['values']}")
            elif spec["type"] == "int":
                lo, hi = act.get("min"), act.get("max")
                ints = all(v is None or (isinstance(v, int) and not isinstance(v, bool)) for v in (lo, hi))
                if not ints or (lo is None and hi is None) or (lo is not None and hi is not None and lo > hi):
                    errors.append(f"action '{act['name']}' is an int: give integer 'min' and/or 'max' with min <= max")
            elif any(k in act for k in ("value", "min", "max")):
                errors.append(f"action '{act['name']}' is a bool: give only its name (polarity goes in modality)")
        return errors, (new if not errors else [])
