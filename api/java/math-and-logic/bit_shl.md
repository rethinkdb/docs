---
layout: api-command
language: Java
permalink: api/java/bit_shl/
command: bitShl
related_commands:
    bit_and: bit_and/
    bit_not: bit_not/
    bit_or: bit_or/
    bit_sar: bit_sar/
    bit_sal: bit_sal/
    bit_shr: bit_shr/
    bit_xor: bit_xor/
---

# Command syntax #

{% apibody %}
r.bitShl(number) &rarr; number
r.bitShl(number[, number, ...]) &rarr; number
{% endapibody %}

# Description #

In a logical shift instruction (also referred to as unsigned shift), the bits that slide off the end disappear (except for the last, which goes into the carry flag), and the spaces are always filled with zeros. Logical shifts are best used with unsigned numbers.

__Note:__ SHL and SAL are the same, and differentiation only happens because SAR and SHR (right shifting) has differences in their implementation.

__Example:__

```java
r.expr(5).bitShl(4).run(conn);

// Result:
80
```
