def _held_in_store(folder: str, key: str, role: str, snap: Any, con: Any = None) -> tuple | None:
    """One held row (gen, items) by key: through the load-time snapshot while it is open (the same
    rows as at load), else a read-only connection (the rows now: at load, plus this life's own merged
    entries, which the asker already holds locally)."""
    if snap is not None and not snap.closed:
        return snap.held(key, role)
    own = con is None
    con = _ro(folder) if own else con
    try:
        ids = [con.execute("SELECT id FROM sym WHERE s = ?", (s,)).fetchone() for s in (key, role)]
        if None in ids:
            return None
        return con.execute("SELECT gen, items FROM held WHERE key = ? AND role = ?",
                           (ids[0][0], ids[1][0])).fetchone()
    finally:
        if own:
            con.close()


def _ro(folder: str) -> Any:
    import sqlite3

    import lineage_store as ls
    con = sqlite3.connect("file:" + ls.path(folder).resolve().as_posix() + "?mode=ro", uri=True)
    con.execute("PRAGMA cache_size = -2048")
    return con


class _HeldKnown(set):
    """THE 20 MB CAP, part (ii) (TETHER_CAP_HELD): _CARRIED[folder] under the store load, answered
    from the held table instead of copied (11.8 MB at 33 saves). In = held under the load's
    signature, or added this life (write_index), and not discarded since (resolve's heal): the copied
    set's answers, which were the held rows at load plus the additions minus the discards. Holds only
    this life's additions (the set) and discards (gone)."""

    def __init__(self, folder: str, sig_repr: str, ag: Any) -> None:
        super().__init__()
        self.folder, self.sig_repr, self.ag, self.gone, self.con = folder, sig_repr, ag, set(), None

    def __contains__(self, k) -> bool:
        if k in self.gone:
            return False
        if set.__contains__(self, k):
            return True
        s, key, role = k
        return s == self.sig_repr and _held_in_store(
            self.folder, key, role, getattr(self.ag, "_dk_snap", None), self.con) is not None

    def add(self, k) -> None:
        self.gone.discard(k)
        set.add(self, k)

    def update(self, *its) -> None:
        for it in its:
            for k in it:
                self.add(k)

    def discard(self, k) -> None:
        set.discard(self, k)
        self.gone.add(k)

    def reader(self, on: bool) -> None:
        """write_index's asks after the snapshot closed (a game's end): one connection for the
        loop, closed before the merge so no reader holds the checkpoint."""
        if on and self.con is None:
            self.con = _ro(self.folder)
        elif not on and self.con is not None:
            self.con.close()
            self.con = None


# part (ii)'s _LAZY under the store load: each held key is asked at its first resolve, not copied
# (4.6 MB, 13,034 keys at 33 saves). The load's folder and signature, the held keys already in
# tether._INDEX_STORE at load (never lazy, as before), and the keys taken (popped) since.
_LAZY_BASE: dict = {}
_CAP_SPENT: list = []     # a second store load in this process: copied from then on


def _lazy_take(k: tuple, key: str, role: str, snap: Any) -> dict | None:
    """_LAZY.pop(k) under part (ii): {gen, folder} for a key held at load and not in _INDEX_STORE
    then, at its first ask; None for any other key, and for every later ask."""
    lz = _LAZY.pop(k, None)
    b = _LAZY_BASE
    if lz is not None or not b or k[0] != b["sig"] or k in b["skip"] or k in b["taken"]:
        return lz
    row = _held_in_store(b["folder"], key, role, snap)
    if row is None:
        return None
    b["taken"].add(k)
    return {"gen": row[0], "folder": b["folder"]}


def _cap_copy() -> None:
    """A second store load in one process: the first load's answers are copied into the old sets
    (rows never leave held, and a row is rewritten only for a key this life added or took, so the
    rows now give the first load's answers), and every later load copies, as before."""
    b = _LAZY_BASE
    for folder, kn in list(_CARRIED.items()):
        if not isinstance(kn, _HeldKnown):
            continue
        kn.reader(False)
        con = _ro(folder)
        try:
            rows = con.execute("SELECT s1.s, s2.s, held.gen FROM held JOIN sym s1 ON s1.id = held.key"
                               " JOIN sym s2 ON s2.id = held.role").fetchall()
        finally:
            con.close()
        old = {(kn.sig_repr, key, role) for key, role, _g in rows} - kn.gone
        old.update(set.__iter__(kn))
        if b and b["folder"] == folder:
            for key, role, gh in rows:
                k = (b["sig"], key, role)
                if (k not in b["skip"] and k not in b["taken"]
                        and not set.__contains__(kn, (kn.sig_repr, key, role))):
                    _LAZY[k] = {"gen": gh, "folder": folder}
        _CARRIED[folder] = old
    _LAZY_BASE.clear()
    _CAP_SPENT.append(1)
