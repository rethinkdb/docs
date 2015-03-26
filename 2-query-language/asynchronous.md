---
layout: documentation
title: Asynchronous connections
docs_active: async-connections
permalink: docs/async-connections/
---

Certain RethinkDB drivers support asynchronous connections by integrating with popular async libraries. This is particularly useful with [changefeeds][cf] and other real-time applications.

Due to its event-driven nature, JavaScript can easily execute RethinkDB queries in an asynchronous fashion. The official RethinkDB drivers currently support integration with EventMachine for Ruby and Tornado for Python.

{% toctag %}

# JavaScript

# Ruby and EventMachine

# Python and Tornado