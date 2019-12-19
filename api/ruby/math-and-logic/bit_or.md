---
layout: api-command
language: Ruby
permalink: api/ruby/bit_or/
command: bit_or
related_commands:
    bit_and: bit_and/
    bit_not: bit_not/
    bit_sal: bit_sal/
    bit_sar: bit_sar/
    bit_xor: bit_xor/
---

# Command syntax #

{% apibody %}
r.bit_or(number) &rarr; number
r.bit_or(number[, number, ...]) &rarr; number
{% endapibody %}

# Description #

A bitwise OR is a binary operation that takes two bit patterns of equal length and performs the logical inclusive OR operation on each pair of corresponding bits. The result in each position is 0 if both bits are 0, while otherwise the result is 1.

__Example:__

```rb
> r.expr(5).bit_or(3).run(conn)

7
```
