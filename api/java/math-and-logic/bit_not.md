---
layout: api-command
language: Java
permalink: api/java/bit_not/
command: bitNot
related_commands:
    bit_and: bit_and/
    bit_or: bit_or/
    bit_sal: bit_sal/
    bit_sar: bit_sar/
    bit_xor: bit_xor/
---

# Command syntax #

{% apibody %}
r.bitNot() &rarr; number
{% endapibody %}

# Description #

A bitwise NOT, or complement, is a unary operation that performs logical negation on each bit, forming the ones' complement of the given binary value. Bits that are 0 become 1, and those that are 1 become 0.

__Example:__

```java
r.expr(7).bitNot().run(conn);

// Result:
-8
```
