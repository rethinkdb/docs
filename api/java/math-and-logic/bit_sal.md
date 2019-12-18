---
layout: api-command
language: Java
permalink: api/java/bit_sal/
command: bitSal
related_commands:
    bit_and: bit_and/
    bit_not: bit_not/
    bit_or: bit_or/
    bit_sar: bit_sar/
    bit_shl: bit_shl/
    bit_shr: bit_shr/
    bit_xor: bit_xor/
---

# Command syntax #

{% apibody %}
r.bitSal(number) &rarr; number
r.bitSal(number[, number, ...]) &rarr; number
{% endapibody %}

# Description #

In an arithmetic shift (also referred to as signed shift), like a logical shift, the bits that slide off the end disappear (except for the last, which goes into the carry flag). But in an arithmetic shift, the spaces are filled in such a way to preserve the sign of the number being slid. For this reason, arithmetic shifts are better suited for signed numbers in two's complement format.

__Note:__ SHL and SAL are the same, and differentiation only happens because SAR and SHR (right shifting) has differences in their implementation.

__Example:__

```java
r.expr(5).bitSal(4).run(conn);

// Result:
80
```
