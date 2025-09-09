from .config import load_config

_conf = load_config()

def get_mode_flags(mode: str):
    mode = (mode or _conf["defaults"].get("mode", "normal")).lower()
    flags = _conf.get("flags", {}).get(mode, [])
    return mode, flags
