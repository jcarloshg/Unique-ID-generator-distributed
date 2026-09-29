# Unique ID generator distributed

## Requirements

- IDs must be unique and sortable.
- IDs are ordered by date.
- IDs are numerical values only.
- IDs fit into 64-bit.
- Ability to generate over 10,000 unique IDs per second.

![reference image 64 bits](<Captura de pantalla 2026-09-28 a las 11.45.31 p. m..png>)

Each section is explained below.

- Sign bit: 1 bit. It will always be 0. This is reserved for future uses. It can potentially be used to distinguish between signed and unsigned numbers.
- Timestamp: 41 bits. Milliseconds since the epoch or custom epoch. We use Twitter snowflake default epoch 1288834974657, equivalent to Nov 04, 2010, 01:42:54 UTC.
- Datacenter ID: 5 bits, which gives us 2 ^ 5 = 32 datacenters.
- Machine ID: 5 bits, which gives us 2 ^ 5 = 32 machines per datacenter.
- Sequence number: 12 bits. For every ID generated on that machine/process, the sequence number is incremented by 1. The number is reset to 0 every millisecond.

## technical

use: 
- docker
- nginx
- use one instance of postgres to save all ids
- 3 instances of tha service if generator
  - use python
  - implement integration tests
- use vite for small web app
