

def read_jd_file(jd_path: str) -> str:
    with open(jd_path, 'r', encoding='utf-8') as f:
        return f.read()
    
    