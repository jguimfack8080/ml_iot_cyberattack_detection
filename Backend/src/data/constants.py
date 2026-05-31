"""
CICIoT2023 dataset constants.

Single source of truth for column names, label mappings, and dataset parameters.
All raw column names match the exact headers found in MERGED_CSV files.
"""
from typing import Final

# ---------------------------------------------------------------------------
# Column names — as they appear verbatim in MERGED_CSV
# Note: 3 columns contain spaces; they are normalized to underscores on load
# ---------------------------------------------------------------------------
LABEL_COL: Final[str] = "Label"
CATEGORY_COL: Final[str] = "category"
BINARY_COL: Final[str] = "is_dos_ddos"

FEATURE_COLUMNS_RAW: Final[tuple[str, ...]] = (
    "Header_Length",
    "Protocol Type",   # space → normalized to Protocol_Type
    "Time_To_Live",
    "Rate",
    "fin_flag_number",
    "syn_flag_number",
    "rst_flag_number",
    "psh_flag_number",
    "ack_flag_number",
    "ece_flag_number",
    "cwr_flag_number",
    "ack_count",
    "syn_count",
    "fin_count",
    "rst_count",
    "HTTP",
    "HTTPS",
    "DNS",
    "Telnet",
    "SMTP",
    "SSH",
    "IRC",
    "TCP",
    "UDP",
    "DHCP",
    "ARP",
    "ICMP",
    "IGMP",
    "IPv",
    "LLC",
    "Tot sum",   # space → normalized to Tot_sum
    "Min",
    "Max",
    "AVG",
    "Std",
    "Tot size",  # space → normalized to Tot_size
    "IAT",
    "Number",
    "Variance",
)

# Normalized names: spaces replaced by underscores (used after load)
FEATURE_COLUMNS: Final[tuple[str, ...]] = tuple(
    col.replace(" ", "_") for col in FEATURE_COLUMNS_RAW
)

N_FEATURES: Final[int] = len(FEATURE_COLUMNS)  # 39

# ---------------------------------------------------------------------------
# PCA configuration
# Pipeline A reduces 39 original features to 16 principal components.
# Divergence from Lastenheft (which cited 46 features): documented in Done.md.
# ---------------------------------------------------------------------------
N_PCA_COMPONENTS: Final[int] = 16

# ---------------------------------------------------------------------------
# Reproducibility
# ---------------------------------------------------------------------------
RANDOM_STATE: Final[int] = 42

# ---------------------------------------------------------------------------
# Label mapping: raw ALL_CAPS label → 8-category name
#
# Source: CICIoT2023 dataset (Neto et al. 2023, DOI: 10.3390/s23135941)
# Confirmed against: inspection of MERGED_CSV files Merged01–Merged04
#
# BACKDOOR_MALWARE is intentionally excluded (see EXCLUDED_LABELS).
# Decision documented in Backend/Done.md — Decision P1.5.
# ---------------------------------------------------------------------------
LABEL_TO_CATEGORY: Final[dict[str, str]] = {
    # DDoS — 12 sub-types
    "DDOS-ICMP_FLOOD":           "DDoS",
    "DDOS-UDP_FLOOD":            "DDoS",
    "DDOS-TCP_FLOOD":            "DDoS",
    "DDOS-SYN_FLOOD":            "DDoS",
    "DDOS-RSTFINFLOOD":          "DDoS",
    "DDOS-PSHACK_FLOOD":         "DDoS",
    "DDOS-SYNONYMOUSIP_FLOOD":   "DDoS",
    "DDOS-ICMP_FRAGMENTATION":   "DDoS",
    "DDOS-ACK_FRAGMENTATION":    "DDoS",
    "DDOS-UDP_FRAGMENTATION":    "DDoS",
    "DDOS-SLOWLORIS":            "DDoS",
    "DDOS-HTTP_FLOOD":           "DDoS",
    # DoS — 4 sub-types
    "DOS-UDP_FLOOD":             "DoS",
    "DOS-TCP_FLOOD":             "DoS",
    "DOS-SYN_FLOOD":             "DoS",
    "DOS-HTTP_FLOOD":            "DoS",
    # Mirai — 3 sub-types
    "MIRAI-GREETH_FLOOD":        "Mirai",
    "MIRAI-GREIP_FLOOD":         "Mirai",
    "MIRAI-UDPPLAIN":            "Mirai",
    # Reconnaissance — 5 sub-types
    "RECON-HOSTDISCOVERY":       "Reconnaissance",
    "RECON-OSSCAN":              "Reconnaissance",
    "RECON-PORTSCAN":            "Reconnaissance",
    "RECON-PINGSWEEP":           "Reconnaissance",
    "VULNERABILITYSCAN":         "Reconnaissance",
    # Spoofing — 2 sub-types
    "MITM-ARPSPOOFING":          "Spoofing",
    "DNS_SPOOFING":              "Spoofing",
    # Brute-Force — 1 sub-type
    "DICTIONARYBRUTEFORCE":      "Brute-Force",
    # Web-based — 5 sub-types
    "BROWSERHIJACKING":          "Web-based",
    "COMMANDINJECTION":          "Web-based",
    "SQLINJECTION":              "Web-based",
    "UPLOADING_ATTACK":          "Web-based",
    "XSS":                       "Web-based",
    # Benign — 1 label
    "BENIGN":                    "Benign",
}

# Labels dropped before training (not part of the 8 standard categories)
EXCLUDED_LABELS: Final[frozenset[str]] = frozenset({"BACKDOOR_MALWARE"})

# Ordered list of the 8 target categories
CATEGORIES: Final[tuple[str, ...]] = (
    "DDoS",
    "DoS",
    "Mirai",
    "Reconnaissance",
    "Spoofing",
    "Brute-Force",
    "Web-based",
    "Benign",
)

# Categories treated as Stage-1 positive class (hierarchical classifier)
DOS_DDOS_CATEGORIES: Final[frozenset[str]] = frozenset({"DDoS", "DoS"})

# Stage-2 target categories (non-DoS/DDoS)
STAGE2_CATEGORIES: Final[tuple[str, ...]] = tuple(
    c for c in CATEGORIES if c not in DOS_DDOS_CATEGORIES
)
