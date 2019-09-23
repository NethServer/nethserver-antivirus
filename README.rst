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

Unofficial signatures can be selected using their rating.
To change the rating use: ::

  config setprop clamd UnofficialSignaturesRating medium
  signal-event nethserver-antivirus-update


Cockpit API
===========

dashboard/read
---------------

This api returns the information to show in dashboard page. The following data is retrieved for every ClamAV instance installed:

- current status of the instance
- number of malware found
- number of signatures loaded
- memory used by the ClamAV instance
- number of occurrences of malware by type

Input
^^^^^

- no input

Output example
^^^^^^^^^^^^^^
::

  {
    "rspamd": {
      "installed": true,
      "active": true,
      "malwareFound": 0,
      "signatures": 172557,
      "malwareStats": [],
      "memoryUsedKb": 250808,
      "sinceIso": "2019-09-23T12:19:01+0200"
    },
    "squidclamav": {
      "installed": true,
      "active": false,
      "malwareFound": 0,
      "signatures": 172557,
      "malwareStats": [],
      "memoryUsedKb": 0,
      "sinceIso": "2019-09-23T12:18:04+0200"
    }
  }

logs/read
---------------

This api returns the list of installed ClamAV instances

Input
^^^^^

- no input

Output example
^^^^^^^^^^^^^^
::

  {
    "installedInstances": [
      "clamd@rspamd",
      "clamd@squidclamav"
    ]
  }

settings/read
----------------------------

This api retrieves ``clamd`` configuration and the memory used by every ClamAV instance installed.

Input
^^^^^

- ``appInfo``: ``clamdConfig`` or ``totalMemory``

Input example (clamdConfig)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
::

  {
    "appInfo": "clamdConfig"
  }

Output example (clamdConfig)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
::

  {
    "configuration": {
      "type": "configuration",
      "name": "clamd",
      "props": {
        "OfficialSignatures": "enabled",
        "UnofficialSignaturesRating": "low"
      }
    }
  }

Input example (totalMemory)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
::

  {
    "appInfo": "totalMemory"
  }

Output example (totalMemory)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
::

  {
    "totalMemory": "991"
  }

settings/validate
--------------------------------

This api validates input for ``clamd`` configuration.

Input
^^^^^

- ``OfficialSignatures``: ``enabled`` if ClamAV official signatures should be enabled, else ``disabled``
- ``UnofficialSignaturesRating``: Third-party signatures rating, valid values are ``low``, ``medium`` or ``high``. Higher rating means more blocked threats but also a more possibility of false positive. Recommended ratings are ``low`` and ``medium``

Input example
^^^^^^^^^^^^^^^
::

  {
    "OfficialSignatures": "disabled",
    "UnofficialSignaturesRating": "low"
  }

Output example
^^^^^^^^^^^^^^^
::

  {
    "state": "success"
  }

settings/update
------------------------------

This api updates ``clamd`` configuration.

Input
^^^^^

- same as ``settings/validate``
