"""Stage B: schema record -> Z3 formulas (deterministic; no LLM).

World builds the Z3 symbols once from the vocabulary:
  - actor / task / medium / artifact: one finite enum sort per facet. Its values are the
    leaves; a parent term is the set of its leaves plus a residual leaf `<parent>__other`
    ("something under this parent that no listed child names"), so a parent is strictly
    wider than its children.
  - situation terms: Bool variables.
  - actions: bool -> Bool, enum -> enum sort (values exclude each other), int -> Int.
A record becomes two formulas:
  scope   = actor & task & medium & artifact & when & not(unless)   (where the rule applies)
  content = the behavior itself (a / var == value / min <= var <= max)
"""

from z3 import And, Bool, BoolVal, Const, EnumSort, Int, Not, Or

SCOPE_FACETS = ("task", "medium", "artifact")


class World:
    def __init__(self, vocab, alias=None):
        # alias: behavior key -> canonical key, from checker/merge_vocab.py. A key is a bool
        # action name, or "<enum action>=<value>". Merged behaviors share one Z3 formula.
        self.alias = alias or {}
        self.var, self.cover = {}, {}          # facet -> z3 variable; facet -> term -> [z3 leaf values]
        for facet in ("actor",) + SCOPE_FACETS:
            names = {}                          # term -> leaf names it covers

            def walk(name, node):
                if not isinstance(node, dict):
                    names[name] = [name]
                    return names[name]
                leaves = [f"{name}__other"]
                for k, v in node.items():
                    if k != "_doc":
                        leaves += walk(k, v)
                names[name] = leaves
                return leaves

            all_leaves = walk(facet, vocab.facets[facet])
            sort, consts = EnumSort(f"{facet}_sort", all_leaves)
            const = dict(zip(all_leaves, consts))
            self.var[facet] = Const(facet, sort)
            self.cover[facet] = {t: [const[l] for l in ls] for t, ls in names.items()}
        self.situation = {s: Bool(f"sit_{s}") for s in vocab.terms("situation")}
        self.action = {}                        # name -> (type, z3 variable, {value name: z3 value})
        for name, spec in vocab.actions.items():
            if spec["type"] == "bool":
                self.action[name] = ("bool", Bool(f"act_{name}"), {})
            elif spec["type"] == "int":
                self.action[name] = ("int", Int(f"act_{name}"), {})
            else:
                sort, consts = EnumSort(f"act_{name}_sort", spec["values"])
                self.action[name] = ("enum", Const(f"act_{name}", sort), dict(zip(spec["values"], consts)))

    def _in(self, facet, terms):
        """The facet variable is under ANY of the terms (empty list = no restriction)."""
        if not terms:
            return BoolVal(True)
        return Or([self.var[facet] == leaf for t in terms for leaf in self.cover[facet][t]])

    def scope(self, rec):
        parts = [self._in("actor", [rec["actor"]])]
        parts += [self._in(f, rec["scope"].get(f, [])) for f in SCOPE_FACETS]
        for c in rec.get("when") or []:
            v = self.situation[c["situation"]]
            parts.append(v if c["value"] else Not(v))
        for c in rec.get("unless") or []:
            v = self.situation[c["situation"]]
            parts.append(Not(v) if c["value"] else v)
        return And(parts)

    def canonical(self, act):
        """(action name, enum value or None) after applying merges."""
        kind = self.action[act["name"]][0]
        key = f"{act['name']}={act['value']}" if kind == "enum" else act["name"]
        name, _, value = self.alias.get(key, key).partition("=")
        return name, (value or None)

    def content(self, rec):
        act = rec["action"]
        name, value = self.canonical(act)
        kind, var, values = self.action[name]
        if kind == "bool":
            return var
        if kind == "enum":
            return var == values[value]
        bounds = []
        if act.get("min") is not None:
            bounds.append(var >= act["min"])
        if act.get("max") is not None:
            bounds.append(var <= act["max"])
        return And(bounds)

    def effect(self, rec):
        """What the rule demands. F negates the behavior. P is encoded as the permitted
        behavior itself: a permission conflicts only if the other rule makes it impossible."""
        c = self.content(rec)
        return Not(c) if rec["modality"] == "F" else c
