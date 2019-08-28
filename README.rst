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

Disable official signatures
===========================

Official signatures find only very few virus but have a big memory usage.
To disable the official signatures: ::

  config setprop clamd OfficialSignatures disabled
  signal-event nethserver-antivirus-update

Select signature rating
=======================

Unofficial signatures can be selected using their raiting.
To change the rating use: ::

  config setprop clamd UnofficialSignaturesRating medium
  signal-event nethserver-antivirus-update
