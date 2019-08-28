====================
nethserver-antivirus
====================

Manage default options for all clamav instances.

The configuration is saved inside the ``configuration`` database in the ``clamd`` key.

Properties:

- ``OfficialSignatures``: can be ``enabled`` or ``disabled``. If set to ``disabled``, all default signatures will be deleted and freshclam will be disabled.
- ``UnofficialSignaturesRating``: can be ``low``, ``medium`` or ``high``. Select the rating risk of all sources. An higher rating means more virus detected but also an increased
  probability of false positives.

Database example: ::

 clamd=configuration
    OfficialSignatures=disabled
    UnofficialSignaturesRating=low
