"""epoch's refuters: ground-only, replay-proof, frame-internal proxies cannot move it."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import epoch  # noqa: E402


def _row(ev, **detail):
    return {"event": ev, "detail": detail}


def test_ground_only():
    gen = [
        _row("mint", term="a . b", reason="novel"),
        _row("mint", term="c . d", reason="novel"),
        _row("settle", term="a . b", status="accepted"),
        _row("refuse", term="x", reason="no"),
    ]
    s = epoch.summarise(gen)
    assert s["settles"] == 1 and s["refusals"] == 1
    assert s["sentences_formed"] == ["a . b"]       # the mints alone counted for nothing
    assert s["words_grounded"] == []
    print("ground-only: OK")


def test_replay_not_new():
    g1 = [_row("settle", term="inc", status="accepted")]
    g2 = [_row("settle", term="inc", status="accepted"),
          _row("settle", term="inc . dec", status="accepted")]
    t = epoch.trend([epoch.summarise(g1), epoch.summarise(g2)])
    assert t["new_words_per_generation"] == [1, 0], t   # replay contributes 0
    assert t["new_sentences_per_generation"] == [0, 1]
    assert t["total_new_words"] == 1 and t["total_new_sentences"] == 1
    print("replay-proof: OK")


def test_no_agent_import():
    # Fig 10: the verifier must not be able to reconstruct the claim from agent state.
    src = Path(epoch.__file__).read_text(encoding="utf-8")
    assert "import tether" not in src and "from tether" not in src
    assert "import gamma" not in src and "from gamma" not in src
    print("no-agent-import: OK")


def test_must_fail_frame_proxy():
    # A mint-only generation reads ZERO words/sentences; if this assertion can pass with a
    # mint count as progress, the instrument is a proxy and the test cannot detect it.
    proxy = [_row("mint", term="a . b"), _row("mint", term="c . d")]
    s = epoch.summarise(proxy)
    assert s["words_n"] == 0 and s["sentences_n"] == 0 and s["ground_rows"] == 0, s
    print("MF frame-proxy cannot move progress: OK")


def test_correction_size_trend():
    # Isaiah's "Decoding Tacit Knowledge": watch the trend in correction SIZE, not the
    # count of lessons given. Fewer corrections arriving later = tacit transfer.
    early = [_row("refuse"), _row("refuse"), _row("settle", term="inc")]
    late = [_row("bet"), _row("bet"), _row("refuse"), _row("settle", term="inc")]
    t = epoch.trend([epoch.summarise(early), epoch.summarise(late)])
    assert t["corrections_per_generation"] == [2, 1], t
    assert t["first_correction_at_per_generation"] == [0, 2], t
    assert t["correction_size_trend_down"] is True, t
    print("correction-size trend: OK")


def test_wall_recorded_beside_not_netted():
    g1 = epoch.summarise([_row("settle", term="inc", status="accepted")])
    g2 = epoch.summarise([_row("settle", term="inc", status="accepted"),
                          _row("win_credit", how="WIN")])
    t = epoch.trend([g1, g2])
    assert t["wins_per_generation"] == [0, 1]
    assert t["ground_rows_per_generation"] == [1, 2]
    assert t["new_words_per_generation"] == [1, 0]   # win is not a word
    print("two currencies beside, not netted: OK")


if __name__ == "__main__":
    test_ground_only()
    test_replay_not_new()
    test_no_agent_import()
    test_must_fail_frame_proxy()
    test_correction_size_trend()
    test_wall_recorded_beside_not_netted()
    print("epoch: OK")
