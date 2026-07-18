# Research Notes — Week 14: Industrial Network Monitoring System

## Brief Excel
- Week: 14
- Judul: Industrial Network Monitoring System
- Primary Keyword: industrial network monitoring
- Secondary Keywords: network monitoring OT
- Search Intent: Informational
- Target Internal Link: monitoring jaringan industri → /industrial-network-redundancy
- Anchor Text: monitoring jaringan industri
- Cluster: redundancy
- Type: support

## Perpustakaan Internal (GDrive)

### Buku yang Dikutip:

1. **Spurgeon, Charles E. & Zimmerman, Joann. *Ethernet Switches: An Introduction to Network Design with Switches*. O'Reilly Media, 2013.**
   - Halaman 23-24: Switch management, SNMP, port mirroring, traffic filters
   - Halaman 53: Traffic Flow Monitoring, sFlow, NetFlow/IPFIX
   - Kutipan: "Many switch management systems also use the Simple Network Management Protocol (SNMP) to provide a vendor-neutral way to extract operational information from a switch"
   - Kutipan: "Another useful feature for monitoring and troubleshooting switches is called a packet mirror port"

2. **Kurose, James F. & Ross, Keith W. *Computer Networking: A Top-Down Approach*. 8th Edition. Pearson, 2021.**
   - Section 5.7: Network Management and SNMP, NETCONF/YANG (halaman 425-430)
   - SNMPv3 PDU types, MIB, trap messages
   - Arsitektur network management: managing server, agent, management protocol

3. **Donahue, Gary A. *Network Warrior*. 2nd Edition. O'Reilly Media, 2011.**
   - SNMP traps, management VLAN, RMON probes
   - RMON probe: "essentially a remote monitoring (RMON) probe and packet-capture device that allows you to monitor any port, VLAN, or combination of the two"

4. **Hanes, David; Salgueiro, Gonzalo; Grossetete, Patrick; Barton, Robert; & Henry, Jerome. *IoT Fundamentals: Networking Technologies, Protocols, and Use Cases for the Internet of Things*. Cisco Press, 2017.**
   - Flexible NetFlow and IPFIX for IoT network analytics
   - Network analytics for detecting irregular patterns in IoT data flows

### Buku yang Dikonsultasikan (tidak dikutip):
- Networking for Dummies (Lowe) — SNMP section consulted
- 1,001 CCNA Routing and Switching Practice Questions (Clarke) — SNMP, NetFlow, syslog referenced
- IoT Fundamentals with a Practical Approach (Batra & Goyal) — consulted

## Web Research

### Query:
1. "industrial network monitoring system OT network SNMP best practices"
2. "site:en.scodeno.com managed switch SNMP monitoring"
3. "site:en.scodeno.com alarm OR port mirror OR syslog OR RMON"
4. "industrial network monitoring tools OT ICS visibility downtime prevention 2024 2025"
5. "SNMP industrial Ethernet switch managed monitoring features port mirroring RMON alarm relay"

### Sumber Web yang Diekstrak:
- Optigo Networks. "6 Best OT Network Monitoring Tools for 2025." — OT monitoring tools comparison, BACnet focus

### Sumber Web (search snippets):
- Waterfall Security — OT vs IT network monitoring best practices
- Perle — Managed industrial switch monitoring features (SNMP, trap, RMON, syslog, port mirroring, alarm relay)
- TRENDnet — System monitoring features in managed switches
- Exabeam — Network monitoring with SNMP complete guide 2025

## Differentiator Scodeno

Fitur Scodeno relevan untuk monitoring:
- **SNMP** support di managed switches (XPTN-9000 series: WEB, CLI, Telnet, Console)
- **Alarm relay** — dry contact fisik untuk integrasi SCADA/DCS
- **Dual DC power input** — memastikan switch dan monitoring tetap berjalan saat primary power gagal
- **Fanless design** — tidak ada kipas yang harus dimonitor, lebih sedikit failure point
- **ERPS ring <20ms** — ring failure detection dan recovery cepat
- **Wide temperature -40°C to 75°C** — bertahan di lingkungan yang keras

Differentiator utama artikel:
1. Alarm relay + dual power sebagai failsafe fisik yang tidak bergantung pada jaringan
2. Fanless = fewer failure points to monitor
3. ERPS ring detection via trap untuk visibilitas penuh

## SEO Results

- Primary keyword "industrial network monitoring": 5 occurrences ✅
- Secondary keyword "network monitoring OT": 2 occurrences ✅
- Word count: 1,413
- Rhythm: Short 53%, Medium 39%, Long 8% ✅

## Output Files

- MD: `/home/ace_a/projects/scodeno-landing/articles/Week_14_industrial-network-monitoring-system.md`
- MD (Windows): `D:\Dokumen\Konexindo\4-SEO-Konten\artikel\Week_14_industrial-network-monitoring-system.md`
- HTML: `/home/ace_a/projects/scodeno-landing/articles/Week_14_industrial-network-monitoring-system-memantau-jaringan-ot-tanpa-henti.html`
