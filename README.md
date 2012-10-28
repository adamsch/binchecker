binchecker
==========

Binchecker is a simple utility script written in Python for injecting CRC checksums in small binary files.

v0.1
- supports only one checksum word (32bit) at the end of the binary
- processes small files (<10MB)
- not speed or memory optimal
- little-endian only
- CRC-32 (CCITT-32)