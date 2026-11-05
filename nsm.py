"""7 / 7b, THE NSM TRACE AND ITS TRANSLATION (the reviewer r894 2, r895 1-2, r953 4, r1001; Isaiah
2026-11-03 15:34 "just allow it to speak in both ... it definitely should translate"): the ledger's
rows said in the grammar the library is written in, one line each, to nsm.log beside the ledger.
It reads rows and writes nothing back: the ledger is the same with it ON or OFF (Fig 13: "That
record is not documentation of the term. It is the term."). Every line cites its row's seq.

  SPEAK      c<cycle> #<seq> <KIND> <slot>: <sentence>. Every capitalised word of a sentence is
             an NSM prime or operator word library/grammar.json lists (primes(); r1001), or an
             inflection of one (ALLOLEX); the agent's own names are fillers, in backticks. One
             line per kind per cycle, as narrate does; the rest are said "+n MORE" with their seqs.
  NO WINDOW  a row read over a window (bond_tests, molecule_apply) whose frames are 0 is said as
             "no window", never as a count (r953 4: "no window" is a reason, not a count).
  TRANSLATE  say_term / say_node: a Term or a Bonded tree as a sentence; read_term / read_node: a
             sentence back to a Term over THIS Gamma's atoms, typed as compile_term types a
             chain, or a Refusal whose reason is one of REFUSALS (r895 2: "Every sentence compiles
             back to the same Term, or is refused with a listed typing reason").
  GUARD      as narrate: nothing raises into play; the first error turns the trace off, counted.
"""
from __future__ import annotations

import collections
import functools
import re
from pathlib import Path

import armflag
import store

_NSM = armflag.arm("TETHER_NSM_SPEAK", default=True)
# 7c (a) (the reviewer 2026-11-04 r1050, r1052, r1070, r1073 "describe only what varied"): a slot's
# line is said only when its text differs from that slot's last said line of the same kind, across
# cycles, and every (kind, cycle) gets ONE count line ("n slots, k said, m the same as before")
# citing its seq range, so every row is either said or counted; LOOKUP one line per (slot, cycle)
# per offer (its held_digest), its first held bond and the count. The row and pipeline.log keep the
# detail. OFF: one line per kind per cycle, LOOKUP every held bond.
_DEDUPE = armflag.arm("TETHER_NSM_DEDUPE", default=True)
_NEGATE_GUARD = armflag.arm("TETHER_NEGATE_GUARD", default=True)   # ¬ wired (tether's arm)
_SUBTRACT = armflag.arm("TETHER_SUBTRACT", default=True)   # − is AGENT|subtract (r1160)
SAMPLE = 50           # the LOOKUP row keeps its first 50 held bonds (b2, 10-18); never widened here
WIDTH = 240
UNKNOWN = "?"
# Inflections said for a prime (NSM's allolexes); each maps to the primes it inflects.
ALLOLEX = {"HAPPENED": ("HAPPEN",), "SAW": ("SEE",), "WAS": ("BE",), "CAN'T": ("CAN", "NOT")}
# The listed refusals of read_node / read_term; a reason outside this list is a defect (MF-T).
# r1052 (b), r1059: "has no atom" only where implemented_by is empty; a condition bond (≡ ⋛ +) says
# where it is routed; ¬ (AGENT|negate) is not wired as a term.
REFUSALS = ("has no NSM word (open item)", "BECAUSE has no atom (r896)", "has no atom",
            "not wired as a term", "a condition, routed to the guard offer",
            "a negated condition, routed to the guard offer",
            "Gamma holds no atom", "does not accept", "the sentence does not parse",
            "an unknown bond is not a term")
CAPS = re.compile(r"\b[A-Z][A-Z']*\b")


@functools.cache
def primes() -> frozenset:
    """Every NSM word grammar.json lists: frames_nsm's substantives, frames and connectives, its
    primes_full, and the operators' nsm words; a word written 'A/B' or with '(...)' gives each."""
    g = store.grammar()
    f = g.get("frames_nsm") or {}
    src = [s for k in ("substantives", "frames", "connectives") for s in f.get(k, [])]
    src += [s for v in (f.get("primes_full") or {}).values() if isinstance(v, list) for s in v]
    src += [str(op.get("nsm") or "") for op in (g.get("operators") or {}).values()]
    return frozenset(t for s in src for t in CAPS.findall(re.sub(r"[()/]", " ", s)))


def unlisted(sentence: str) -> list:
    """The capitalised words of a sentence (fillers in backticks dropped) that are neither a prime
    nor an inflection of one."""
    bare = re.sub(r"`[^`]*`", " ", sentence)
    return [w for w in CAPS.findall(bare)
            if w not in primes() and not all(p in primes() for p in ALLOLEX.get(w, ("?",)))]


@functools.cache
def words() -> dict:
    """bond -> its NSM word, from grammar.json's operators (the one door); None where the grammar
    gives none. "BEFORE / AFTER" is said AFTER: a chain applies left to right."""
    out = {}
    for sym, op in (store.grammar().get("operators") or {}).items():
        w = str(op.get("nsm") or "")
        if not w or w.startswith("("):
            out[sym] = None
        elif "/" in w:
            out[sym] = w.split("/")[-1].strip()
        else:
            out[sym] = w.split("(")[0].strip()
    return out


# ---------------------------------------------------------------- 7b: Term / Node <-> sentence

def say_term(t) -> str:
    """'DO `a1` AFTER `a2`[ OTHER `x`| OTHER (DO `b1`) `x`][ IF `guard`[ WHERE `ref`]]': the chain
    in order, its operand as the OTHER slot (with the chain that reads it), its guard as IF."""
    s = "DO " + " AFTER ".join(f"`{a.name}`" for a in t.atoms)
    if t.operand is not None:
        s += (f" OTHER ({say_term(t.operand_term)}) `{t.operand}`" if t.operand_term is not None
              else f" OTHER `{t.operand}`")
    if t.guard is not None:
        s += f" IF `{t.guard}`" + (f" WHERE `{t.guard_ref}`" if t.guard_ref is not None else "")
    return s


def say_node(node) -> str:
    """A Bonded tree: '(<left> <bond word> <right>)'; an unsettled junction keeps '?' (the renderer
    never picks a bond, composer.render_node); a bond with no word is said by its symbol."""
    if hasattr(node, "bond") and hasattr(node, "left"):
        w = UNKNOWN if node.bond == UNKNOWN else (words().get(node.bond) or node.bond)
        return f"({say_node(node.left)} {w} {say_node(node.right)})"
    return f"[{say_term(node)}]" if hasattr(node, "atoms") else str(node)


_NAME = r"`([^`]+)`"
_TERM = re.compile(rf"^DO (?P<chain>`[^`]+`(?: AFTER `[^`]+`)*)"
                   rf"(?: OTHER (?:\((?P<opterm>DO [^()]*)\) {_NAME}|{_NAME}))?"
                   rf"(?: IF {_NAME}(?: WHERE {_NAME})?)?$")


class Refused(Exception):
    pass


def _names(chain: str) -> list:
    return re.findall(_NAME, chain)


def _chain(names: list, atoms: dict) -> tuple:
    missing = [n for n in names if n not in atoms]
    if missing:
        raise Refused(f"Gamma holds no atom {missing}")
    chain = tuple(atoms[n] for n in names)
    import gamma
    for a, b in zip(chain, chain[1:], strict=False):
        if not gamma.accepts_type(b, a.out_type):
            raise Refused(f"{a.name} gives {a.out_type}, which {b.name} does not accept")
    return chain


def read_term(sentence: str, atoms: dict):
    """A sentence from say_term back to a Term over `atoms`, or a compile_term.Refusal."""
    import compile_term
    import gamma
    try:
        m = _TERM.match(sentence.strip())
        if m is None:
            raise Refused(f"the sentence does not parse: {sentence[:80]!r}")
        g = m.groups()       # chain, opterm, opterm's slot, operand, guard, guard_ref
        op_t = None
        if g[1]:
            om = _TERM.match(g[1])
            if om is None or any(om.groups()[1:]):
                raise Refused(f"the sentence does not parse: {g[1][:80]!r}")
            op_t = gamma.Term(_chain(_names(om["chain"]), atoms))
        return gamma.Term(_chain(_names(g[0]), atoms), operand=g[2] or g[3], guard=g[4],
                          guard_ref=g[5], operand_term=op_t)
    except Refused as e:
        return compile_term.Refusal(str(e))


def _split_node(s: str) -> tuple:
    """'(<left> <word> <right>)' -> (left, word, right) at the top level."""
    body, depth = s[1:-1], 0
    for i, ch in enumerate(body):  # noqa: B007  i is read after the loop
        depth += (ch in "([") - (ch in ")]")
        if depth == 0:
            break
    else:
        raise Refused(f"the sentence does not parse: {s[:80]!r}")
    rest = body[i + 1:].strip()
    j = min((k for k in (rest.find("("), rest.find("[")) if k > 0), default=-1)
    if body[:1] not in "([" or j < 0:
        raise Refused(f"the sentence does not parse: {s[:80]!r}")
    return body[:i + 1], rest[:j].strip(), rest[j:]


def read_node(sentence: str, atoms: dict):
    """A sentence from say_node back to ONE Term (→ junctions flatten into one chain, as molecule
    apply composes them), or a compile_term.Refusal with a listed reason."""
    import compile_term
    import gamma
    by_word = {w: b for b, w in words().items() if w}

    def walk(s: str):
        s = s.strip()
        if s.startswith("[") and s.endswith("]"):
            t = read_term(s[1:-1], atoms)
            if isinstance(t, compile_term.Refusal):
                raise Refused(t.reason)
            return t
        if not (s.startswith("(") and s.endswith(")")):
            raise Refused(f"the sentence does not parse: {s[:80]!r}")
        left, w, right = _split_node(s)
        bond = by_word.get(w, w)
        if bond == UNKNOWN:
            raise Refused("an unknown bond is not a term")
        if bond == "⇒":
            raise Refused("⇒ BECAUSE has no atom (r896)")
        if bond == "−" and not _SUBTRACT:
            raise Refused("− has no atom")
        if bond != "→":
            impl = (store.grammar().get("operators") or {}).get(bond, {}).get("implemented_by")
            if not impl:
                raise Refused(f"{bond} has no atom")
            if bond in ("≡", "⋛", "+", "∥"):
                raise Refused(f"{bond} implemented_by {impl[0]}: a condition, routed to the "
                              "guard offer")
            if bond == "¬" and _NEGATE_GUARD:
                raise Refused(f"¬ implemented_by {impl[0]}: a negated condition, routed to the "
                              "guard offer")
            raise Refused(f"{bond}: implemented_by {impl[0]} not wired as a term")
        a, b = walk(left), walk(right)
        if a.operand is not None or a.guard is not None:
            raise Refused(f"{b.atoms[0].name} does not accept a chain that carries an operand "
                          f"or a guard ({a.name})")
        _chain([x.name for x in a.atoms + b.atoms], atoms)
        return gamma.Term(a.atoms + b.atoms, operand=b.operand, guard=b.guard,
                          guard_ref=b.guard_ref, operand_term=b.operand_term)
    try:
        return walk(sentence)
    except Refused as e:
        return compile_term.Refusal(str(e))


def listed(reason: str) -> bool:
    return any(r in reason for r in REFUSALS)


# ---------------------------------------------------------------- 7: the trace

def _f(v) -> str:
    """A filler: the agent's own name or value, in backticks, cut to fit."""
    s = (v if isinstance(v, str) else repr(v)).replace("`", "'")
    return f"`{s if len(s) <= 90 else s[:87] + '...'}`"


def say_row(event: str, d: dict, ends: tuple) -> list:
    """[(KIND, sentence)] for a row, or []. Several for a LOOKUP row (its held bonds)."""
    win, advance = ends
    w = words()
    if event in ("bond_tests", "molecule_apply") and d.get("frames") == 0:
        return [("NO_WINDOW", f"I CAN'T SAY SOMETHING TRUE HERE: no window ({_f(event)}, 0)")]
    if event == "lookup":
        out = []
        for h in (d.get("held_sample") or [])[:SAMPLE]:
            bw = " ".join(w.get(b) or b for b in h.get("held") or []) or UNKNOWN
            out.append(("LOOKUP", f"I THINK THIS IS LIKE {_f(h.get('molecule'))}: "
                                  f"{_f(h.get('left'))} {_f(h.get('left_reading'))} {bw} "
                                  f"{_f(h.get('right'))} {_f(h.get('right_reading'))}"))
        n = d.get("held_n") or 0
        if n > len(out):
            note = _f(f"held_n {n}, the row keeps {SAMPLE}")
            out.append(("LOOKUP", f"+{n - len(out)} MORE ({note})"))
        return out
    if d.get("status") == "refuted":
        return [("REFUTE", f"I DON'T THINK {_f(d.get('term') or d.get('asked'))} IS TRUE NOW")]
    if event == "mint":
        return [("MINT", f"SOMETHING HAPPENED HERE; I THINK {_f(d.get('term'))} CAN SAY THIS")]
    if event == "molecule_offer":
        bond = w.get(d.get("bond")) or d.get("bond")
        out = [("COMPOSE", f"I THINK PART AND PART CAN BE ONE THING: {_f(d.get('term'))} "
                           f"({_f(d.get('molecule'))}, {bond})")]
        if d.get("seen"):
            out.append(("SEEN", f"I SAW {_f(d.get('molecule'))} BE TRUE WHERE "
                                f"{_f(d.get('object'))} IS"))
        else:
            out.append(("GENERALISED", f"I THINK {_f(d.get('molecule'))} CAN BE TRUE WHERE "
                                       f"{_f(d.get('object'))} IS, BECAUSE I SAW THIS "
                                       f"SOMEWHERE ELSE"))
        return out
    if event == "bet":
        return [("BET", f"I THINK: IF I DO THIS NOW, AFTER THIS I SEE {_f(d.get('predicted'))}"
                        + (f" ({_f(d['meant'])})" if d.get("meant") else ""))]
    if event == "settle":
        return [("SETTLE", f"THIS IS TRUE: {_f(d.get('term'))}. I KNOW THIS NOW")]
    if event == "demote":
        return [("REFUTE", f"I DON'T THINK {_f(d.get('term'))} IS TRUE NOW")]
    if event == "park":
        v = d.get("verdict")
        if v == "not found within budget":
            return [("PARK", "SOMETHING HAPPENED HERE; I CAN'T SAY THIS NOW; MAYBE AFTER MORE "
                             "TIME I CAN")]
        if v == "closure cannot cover R":
            return [("PARK", "SOMETHING HAPPENED HERE; NOT ONE THING I CAN SAY IS LIKE THIS")]
        return [("PARK", f"SOMETHING HAPPENED HERE; I CAN'T SAY THIS ({_f(v)})")]
    if event == "want":
        return [("WANT", f"I WANT {_f(d.get('objective'))}")]
    if event == "routine":
        return [("PLAN", f"I WANT THIS: I DO {_f(d.get('routine'))}")]
    if event == "ending" and d.get("how") in (win, advance):
        return [("WIN" if d["how"] == win else "LEVEL", "SOMETHING GOOD HAPPENED: I WANT THIS")]
    return []


class Speaker:
    def __init__(self, path: Path | None, ends: tuple) -> None:
        self.on = _NSM and path is not None
        self._log = path.with_name("nsm.log") if self.on else None
        if self._log is not None:
            self._log.write_text("", encoding="utf-8")
        self._ends = ends
        self._cyc = None
        self._said: set = set()
        self._over: dict = collections.defaultdict(list)
        self._last: dict = {}                              # 7c: (kind, slot) -> last said text
        self._offer: dict = {}                             # 7c: slot -> its said LOOKUP digest
        self._cnt: dict = {}                               # 7c: kind -> this cycle's tally
        self.counts: collections.Counter = collections.Counter()
        self.faults = 0
        self.fault: str | None = None

    def see(self, seq: int, cycle: int, step: str, slot: str, event: str, d: dict) -> None:
        if not self.on:
            return
        try:
            self._see(seq, cycle, step, slot, event, d)
        except Exception as e:           # the trace must never reach play
            self.on = False
            self.faults += 1
            self.fault = repr(e)[:200]

    def _emit(self, line: str) -> None:
        line = line if len(line) <= WIDTH else line[:WIDTH - 3] + "..."
        with self._log.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")

    def _flush(self) -> None:
        for kind, c in sorted(self._cnt.items()):
            self._emit(f"c{self._cyc} #{c['seqs'][0]}..#{c['seqs'][-1]} {kind} @: "
                       f"{len(c['slots'])} slots, {c['said']} said, {c['same']} the same as before")
        self._cnt = {}
        for kind, seqs in sorted(self._over.items()):
            self._emit(f"c{self._cyc} #{seqs[0]}..#{seqs[-1]} {kind} @: +{len(seqs)} MORE")
        self._said, self._over = set(), collections.defaultdict(list)
        self._offer = {}

    def _see(self, seq: int, cycle: int, _step: str, slot: str, event: str, d: dict) -> None:
        said = say_row(event, d, self._ends)
        if not said:
            return
        if cycle != self._cyc:
            self._flush()
            self._cyc = cycle
        if _DEDUPE:
            self._dedupe(seq, cycle, slot, event, d, said)
            return
        for kind, text in said:
            self.counts[kind] += 1
            if kind in self._said and kind != "LOOKUP":
                self._over[kind].append(seq)
                continue
            self._said.add(kind)
            self._emit(f"c{cycle} #{seq} {kind} {slot}: {text}")

    def _dedupe(self, seq: int, cycle: int, slot: str, event: str, d: dict, said: list) -> None:
        """7c: a slot's line only when its text changed since its last said line of the kind
        (r1073), every row tallied into its (kind, cycle) count line; LOOKUP one line per (slot,
        cycle) per offer: its first held bond and how many more the row holds."""
        def tally(kind: str, said_it: bool) -> None:
            c = self._cnt.setdefault(kind, {"slots": set(), "said": 0, "same": 0, "seqs": []})
            c["slots"].add(slot)
            c["seqs"].append(seq)
            c["said" if said_it else "same"] += 1
        if event == "lookup":
            n = sum(1 for k, _t in said if k == "LOOKUP")
            self.counts["LOOKUP"] += n
            dig = d.get("held_digest")
            if slot in self._offer and self._offer[slot] == dig:
                tally("LOOKUP", False)
                return
            self._offer[slot] = dig
            tally("LOOKUP", True)
            held = int(d.get("held_n") or 0)
            text = said[0][1]
            if held > 1:
                text += f"; +{held - 1} MORE ({_f(f'held_n {held}, the row keeps {SAMPLE}')})"
            self._emit(f"c{cycle} #{seq} LOOKUP {slot}: {text}")
            return
        for kind, text in said:
            self.counts[kind] += 1
            key = (kind, slot)
            if self._last.get(key) == text:
                tally(kind, False)
                continue
            self._last[key] = text
            tally(kind, True)
            self._emit(f"c{cycle} #{seq} {kind} {slot}: {text}")

    def close(self) -> None:
        if self.on:
            try:
                self._flush()
                self._last = {}          # a game's last lines do not silence the next game's
            except Exception as e:
                self.on = False
                self.faults += 1
                self.fault = repr(e)[:200]
