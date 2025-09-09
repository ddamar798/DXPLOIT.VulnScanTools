def recommend(report_data: dict):
    mapping = {
        "sql_injection": "Gunakan parameterized queries, validasi input.",
        "xss": "Gunakan output encoding, Content-Security-Policy.",
        "ssrf": "Validasi URL, gunakan allowlist.",
        "rce": "Validasi file upload, sandboxing.",
        "open_redirect": "Gunakan allowlist URL redirect."
    }
    for f in report_data["findings"]:
        f["recommendation"] = mapping.get(f["vuln_type"], "Cek dokumentasi OWASP.")
    return report_data
