====================
nethserver-antivirus
====================

Manage default options for all clamav instances.

The configuration is saved inside the ``configuration`` database in the ``clamd`` key.

Properties:

- ``OfficialSignatures``: can be ``enabled`` or ``disabled``. If set to ``disabled``, all default signatures will be deleted and freshclam will be disabled.

Database example: ::

 clamd=configuration
    OfficialSignatures=disabled
