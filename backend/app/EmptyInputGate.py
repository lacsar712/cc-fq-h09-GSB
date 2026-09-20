from app.EmptyFastqBypass import accept_paste, accept_sample, normalize_paste, normalize_sample_content


def gate_paste(text):
    ok = accept_paste(text)
    return ok, normalize_paste(text) if ok else ""


def gate_sample(text):
    ok = accept_sample(text)
    return ok, normalize_sample_content(text) if ok else ""
