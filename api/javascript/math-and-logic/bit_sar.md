---
layout: api-command
language: JavaScript
permalink: api/javascript/bit_sar/
command: bitSar
io:
    -   - number
        - number
related_commands:
    bit_and: bit_and/
    bit_not: bit_not/
    bit_or: bit_or/
    bit_sal: bit_sal/
    bit_xor: bit_xor/
---

# Command syntax #

{% apibody %}
r.bitSar(number) &rarr; number
r.bitSar(number[, number, ...]) &rarr; number
{% endapibody %}

# Description #

In an arithmetic shift (also referred to as signed shift), like a logical shift, the bits that slide off the end disappear (except for the last, which goes into the carry flag). But in an arithmetic shift, the spaces are filled in such a way to preserve the sign of the number being slid. For this reason, arithmetic shifts are better suited for signed numbers in two's complement format.

__Example:__

```js
r.expr(32).bitSar(3).run(conn);

// Result:
4
```
