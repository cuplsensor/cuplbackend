.. _BoxConsumerAPI:

Box
---
.. openapi:: api.yaml
   :include:
      /box/*
   :exclude:
      /box/{serial}/scanned
   :encoding: utf-8
   :examples:

.. _BoxScannedConsumerAPI:

Scanned
^^^^^^^^^^^^
Determines if a box has been scanned by the current user.

.. openapi:: api.yaml
   :include:
      /box/{serial}/scanned
   :encoding: utf-8
   :examples:
