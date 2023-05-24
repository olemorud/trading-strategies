

def normalize_filename(filename: str) -> str:
    # there are many platform dependent rules for
    # legal filenames, but only keeping alphanumeric
    # characters plus underscores and dots is sufficient
    # for our purposes
    return "".join([c for c in filename if c.isalnum() or c in "_."])
