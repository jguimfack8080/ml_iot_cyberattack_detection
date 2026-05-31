# Label Mapping Documentation

Project: ml_iot_cyberattack_detection
Source: `src/data/constants.py:LABEL_TO_CATEGORY`
Dataset: CICIoT2023 (Neto et al. 2023, DOI: 10.3390/s23135941)

---

## Overview

The CICIoT2023 MERGED_CSV files use ALL_CAPS raw labels (33 specific attack types
+ Benign). These are mapped to 8 hierarchical categories for the classification task.

Raw labels verified from files: Merged01.csv to Merged04.csv (spot check).
All labels appear in uppercase, e.g. "DDOS-ICMP_FLOOD", "BENIGN".

---

## Mapping Table

### DoS/DDoS (Stage 1 positive class: is_dos_ddos = 1)

| Raw Label | Category |
|-----------|----------|
| DDOS-ICMP_FLOOD | DDoS |
| DDOS-UDP_FLOOD | DDoS |
| DDOS-TCP_FLOOD | DDoS |
| DDOS-SYN_FLOOD | DDoS |
| DDOS-RSTFINFLOOD | DDoS |
| DDOS-PSHACK_FLOOD | DDoS |
| DDOS-SYNONYMOUSIP_FLOOD | DDoS |
| DDOS-ICMP_FRAGMENTATION | DDoS |
| DDOS-ACK_FRAGMENTATION | DDoS |
| DDOS-UDP_FRAGMENTATION | DDoS |
| DDOS-SLOWLORIS | DDoS |
| DDOS-HTTP_FLOOD | DDoS |
| DOS-UDP_FLOOD | DoS |
| DOS-TCP_FLOOD | DoS |
| DOS-SYN_FLOOD | DoS |
| DOS-HTTP_FLOOD | DoS |

Combined DDoS + DoS = Stage 1 positive class (is_dos_ddos = 1).
In the full dataset (838,602 instances): approximately 58.4% DoS/DDoS.

### Non-DoS Categories (Stage 1 negative class: is_dos_ddos = 0)

#### Mirai
| Raw Label | Category |
|-----------|----------|
| MIRAI-GREETH_FLOOD | Mirai |
| MIRAI-GREIP_FLOOD | Mirai |
| MIRAI-UDPPLAIN | Mirai |

#### Reconnaissance
| Raw Label | Category |
|-----------|----------|
| RECON-HOSTDISCOVERY | Reconnaissance |
| RECON-OSSCAN | Reconnaissance |
| RECON-PORTSCAN | Reconnaissance |
| RECON-PINGSWEEP | Reconnaissance |
| VULNERABILITYSCAN | Reconnaissance |

#### Spoofing
| Raw Label | Category |
|-----------|----------|
| MITM-ARPSPOOFING | Spoofing |
| DNS_SPOOFING | Spoofing |

#### Brute-Force
| Raw Label | Category |
|-----------|----------|
| DICTIONARYBRUTEFORCE | Brute-Force |

#### Web-based
| Raw Label | Category |
|-----------|----------|
| BROWSERHIJACKING | Web-based |
| COMMANDINJECTION | Web-based |
| SQLINJECTION | Web-based |
| UPLOADING_ATTACK | Web-based |
| XSS | Web-based |

#### Benign
| Raw Label | Category |
|-----------|----------|
| BENIGN | Benign |

---

## Excluded Labels

| Raw Label | Reason |
|-----------|--------|
| BACKDOOR_MALWARE | Fewer than 0.01% of total instances (3,078 rows). Not part of the 8 standard categories from Raturi et al. (2026). Dropped before training. |

---

## Stage Structure

```
Stage 1 (binary)
  Positive (1) : DDoS + DoS      -- ~58.4% of data
  Negative (0) : all other 6 categories

Stage 2 (multiclass, non-DoS only)
  Classes : Mirai, Reconnaissance, Spoofing, Brute-Force, Web-based, Benign
```

---

## Feature Columns (39 normalized names)

Original MERGED_CSV columns with spaces are normalized (space -> underscore):

```
Header_Length, Protocol_Type, Time_To_Live, Rate,
fin_flag_number, syn_flag_number, rst_flag_number, psh_flag_number,
ack_flag_number, ece_flag_number, cwr_flag_number,
ack_count, syn_count, fin_count, rst_count,
HTTP, HTTPS, DNS, Telnet, SMTP, SSH, IRC,
TCP, UDP, DHCP, ARP, ICMP, IGMP, IPv, LLC,
Tot_sum, Min, Max, AVG, Std, Tot_size, IAT, Number, Variance
```

Note: The CLAUDE.md and cited papers mention 46 features. The actual CSV files
contain 39 features. This discrepancy is documented in the paper (Methodik section).
