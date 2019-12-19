---
layout: api-command
language: Python
permalink: api/python/bit_and/
command: bit_and
related_commands:
    bit_not: bit_not/
    bit_or: bit_or/
    bit_sal: bit_sal/
    bit_sar: bit_sar/
    bit_xor: bit_xor/
---

# Command syntax #

{% apibody %}
r.bit_and(number) &rarr; number
r.bit_and(number[, number, ...]) &rarr; number
{% endapibody %}

# Description #

A bitwise AND is a binary operation that takes two equal-length binary representations and performs the logical AND operation on each pair of the corresponding bits, which is equivalent to multiplying them. Thus, if both bits in the compared position are 1, the bit in the resulting binary representation is 1 (1 × 1 = 1); otherwise, the result is 0 (1 × 0 = 0 and 0 × 0 = 0).

__Example:__

```py
r.expr(5).bit_and(3).run(conn)

# Result:
1
```
