def get_mode_flags(mode: str) -> list:
    if mode == "normal":
        return ["--basic-crawler", "--rate-limit", "3"]
    elif mode == "silent":
        return ["--passive", "--max-depth", "2"]
    elif mode == "brutal":
        return ["--advanced-crawler", "--threads", "20"]
    else:
        return []
