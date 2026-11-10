"""The ending's identifiers that carry "game_loss" as the OUTCOME word (r1571), for the no-game-
identity guards (test_how_soon h6, test_reflex r6, test_musing_chosen m6, test_think_chooser).
game_loss is the ending's word, not a game's identity; exact names only, so a game identity can
never hide behind it (r1575)."""

GAME_LOSS_NAMES = frozenset({
    "GAME_LOSS", "GAME_LOSS_ALIASES", "GAME_LOSS_WORDS", "UNDECLARED_GAME_LOSS", "game_loss_word",
    "_game_loss_n", "_GAME_LOSS_VOTE", "_GAME_LOSS_KEEPS", "game_loss_possible", "game_losses",
    "game_loss_at",
})


def game_name_ok(name: str) -> bool:
    """True unless the name reads a game's identity: no "game" in it, or an exact ending name."""
    return "game" not in name.lower() or name in GAME_LOSS_NAMES
