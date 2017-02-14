---
layout: api-command
language: JavaScript
permalink: api/javascript/merge/
command: merge
io:
    -   - sequence
        - stream
    -   - array
        - array
    -   - object
        - object
    -   - singleSelection
        - object
related_commands:
    pluck: pluck/
    without: without/
    map: map/
---

# Command syntax #

{% apibody %}
singleSelection.merge([object | function, object | function, ...]) &rarr; object
object.merge([object | function, object | function, ...]) &rarr; object
sequence.merge([object | function, object | function, ...]) &rarr; stream
array.merge([object | function, object | function, ...]) &rarr; array
{% endapibody %}

# Description #

Merge two or more objects together to construct a new object with properties from all. When there is a conflict between field names, preference is given to fields in the rightmost object in the argument list. `merge` also accepts a subquery function that returns an object, which will be used similarly to a [map](/api/javascript/map/) function.

__Example:__ Equip Thor for battle.

```javascript
r.table('marvel').get('thor').merge(
    r.table('equipment').get('hammer'),
    r.table('equipment').get('pimento_sandwich')
).run(conn, callback)
```

__Example:__ Equip every hero for battle, using a subquery function to retrieve their weapons.

```javascript
r.table('marvel').merge(function (hero) {
    return { weapons: r.table('weapons').get(hero('weaponId')) };
}).run(conn, callback)
```

__Example:__ Use `merge` to join each blog post with its comments.

Note that the sequence being merged&mdash;in this example, the comments&mdash;must be coerced from a selection to an array. Without `coerceTo` the operation will throw an error ("Expected type DATUM but found SELECTION").

```javascript
r.table('posts').merge(function (post) {
    return {
        comments: r.table('comments').getAll(post('id'),
            {index: 'postId'}).coerceTo('array')
    }
}).run(conn, callback)
```

__Example:__ Merge can be used recursively to modify object within objects.

```javascript
r.expr({weapons : {spectacular_graviton_beam : {dmg : 10, cooldown : 20}}}).merge(
    {weapons : {spectacular_graviton_beam : {dmg : 10}}}).run(conn, callback)
```


__Example:__ To replace a nested object with another object you can use the literal keyword.

```javascript
r.expr({weapons : {spectacular_graviton_beam : {dmg : 10, cooldown : 20}}}).merge(
    {weapons : r.literal({repulsor_rays : {dmg : 3, cooldown : 0}})}).run(conn, callback)
```


__Example:__ Literal can be used to remove keys from an object as well.

```javascript
r.expr({weapons : {spectacular_graviton_beam : {dmg : 10, cooldown : 20}}}).merge(
    {weapons : {spectacular_graviton_beam : r.literal()}}).run(conn, callback)
```

