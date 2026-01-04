from .media import open_english, open_spiderman, open_supernatural, open_vnature
from .system import shutdown_computer

AVAILABLE_ACTIONS = {
    "open_english": open_english,
    "open_spiderman": open_spiderman,
    "open_vnature": open_vnature,
    "open_supernatural": open_supernatural,
    "shutdown_computer": shutdown_computer,
}
