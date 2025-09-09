"""
Mapping vulnerability type to high-level safe recommendations.
No exploit steps provided.
"""
from typing import Dict

RECOMMENDER_MAP: Dict[str, Dict[str, str]] = {
    "sql_injection": {"rec_verify": "Verifikasi manual + sqlmap (verify only) di environment aman.", "rec_mitigate": "Gunakan parameterized queries/ORM, input validation."},
    "xss": {"rec_verify": "Proof-of-concept non-persistent; gunakan Burp Repeater untuk verifikasi.", "rec_mitigate": "Output encoding, CSP, sanitize input."},
    "ssrf": {"rec_verify": "Analisa alur request; hindari blind exploitation.", "rec_mitigate": "Allowlist host, batasi egress."},
    "open_redirect": {"rec_verify": "Periksa parameter redirect, pastikan tidak menerima domain arbitrary.", "rec_mitigate": "Allowlist URL redirect."},
    "lfi": {"rec_verify": "Verifikasi path handling; jangan eksploitasi di target produksi.", "rec_mitigate": "Normalize path, batasi akses file."},
    "rce": {"rec_verify": "Segera laporkan; verifikasi hanya di lab aman.", "rec_mitigate": "Validasi upload, sandbox, patch library."}
}

def recommend_for(vuln_type: str):
    key = str(vuln_type).lower()
    return RECOMMENDER_MAP.get(key, {"rec_verify": "Verifikasi manual pada environment aman.", "rec_mitigate": "Laporkan ke pemilik sistem dan ikuti pedoman mitigasi umum."})
