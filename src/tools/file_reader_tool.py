

def read_jd_file(jd_path: str) -> str:
    """
    Reads the job description file from the given path and returns its content as a string.

    Args:
        jd_path (str): Path to the job description file.

    Returns:
        str: Content of the job description file.
    """
    with open(jd_path, 'r', encoding='utf-8') as f:
        return f.read()
    
    