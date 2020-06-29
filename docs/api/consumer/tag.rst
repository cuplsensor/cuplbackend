.. _TagConsumerAPI:

Tag
---
.. openapi:: api.yaml
   :include:
      /tag/*
   :exclude:
      /tag/{serial}/scanned
   :encoding: utf-8
   :examples:

.. _TagScannedConsumerAPI:

Scanned
^^^^^^^^^^^^
Determines if a tag has been scanned by the current user.

.. openapi:: api.yaml
   :include:
      /tag/{serial}/scanned
   :encoding: utf-8
   :examples:
