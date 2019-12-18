---
layout: api-command
language: Ruby
permalink: api/ruby/bit_shr/
command: bit_shr
related_commands:
    bit_and: bit_and/
    bit_not: bit_not/
    bit_or: bit_or/
    bit_sal: bit_sal/
    bit_shl: bit_shl/
    bit_sar: bit_sar/
    bit_xor: bit_xor/
---

# Command syntax #

{% apibody %}
r.bit_shr(number) &rarr; number
r.bit_shr(number[, number, ...]) &rarr; number
{% endapibody %}

# Description #

In an arithmetic shift (also referred to as signed shift), like a logical shift, the bits that slide off the end disappear (except for the last, which goes into the carry flag). But in an arithmetic shift, the spaces are filled in such a way to preserve the sign of the number being slid. For this reason, arithmetic shifts are better suited for signed numbers in two's complement format.

__Example:__

```rb
> r.expr(-43).bit_shr(2).run(conn)

1073741813
```
