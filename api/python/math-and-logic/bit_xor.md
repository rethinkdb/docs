---
layout: api-command
language: Python
permalink: api/python/bit_xor/
command: bit_xor
related_commands:
    bit_and: bit_and/
    bit_not: bit_not/
    bit_or: bit_or/
    bit_sal: bit_sal/
    bit_shl: bit_shl/
    bit_sar: bit_sar/
    bit_shr: bit_shr/
---

# Command syntax #

{% apibody %}
r.bit_xor(number) &rarr; number
r.bit_xor(number[, number, ...]) &rarr; number
{% endapibody %}

# Description #

A bitwise XOR is a binary operation that takes two bit patterns of equal length and performs the logical exclusive OR operation on each pair of corresponding bits. The result in each position is 1 if only the first bit is 1 or only the second bit is 1, but will be 0 if both are 0 or both are 1. In this we perform the comparison of two bits, being 1 if the two bits are different, and 0 if they are the same.

__Example:__

```py
r.expr(6).bit_xor(4).run(conn)

# Result:
2
```
