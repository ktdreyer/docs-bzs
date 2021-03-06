This script searches for BZs that are interesting to the RH Ceph Storage docs
team.

* All BZs that have [RFE] in the summary (our BZ rules always add the
  ``FutureFeature`` keyword here too)
* All BZs that were known issues in previous versions and are fixed in this
  version.
* All BZs that have a customer case attached.

TODO:
-----

* Find all BZs that remains known issues

* Automatically add candidate BZs to the Release Notes tracker bug

* Automatically determine the Release Notes tracker bug

* Automatically file a new Release Notes tracker bug if none can be found

Usage:
------

To run this::

  sudo yum -y install python-prettytable python-bugzilla

  git clone https://github.com/ktdreyer/docs-bzs

  cd docs-bzs

  ./find.py

Advanced usage:
---------------

You can also search for a specific targeted release::

  ./find.py 2.4

Or maybe this release does not yet have bugs in ``VERIFIED`` state, and you
want to preview what is ``ON_QA``::

  ./find.py 2.4 ON_QA

Sample output
-------------

::

  RFEs: 1
  +-------------------------------------+-----------------------------------+
  | url                                 | summary                           |
  +-------------------------------------+-----------------------------------+
  | https://bugzilla.redhat.com/1446338 | [Doc RFE] Add a new compatibility |
  |                                     |   matrix of RHCS with various     |
  |                                     |   products                        |
  +-------------------------------------+-----------------------------------+

  Customer Cases: ...

  Fixed Known Issues: ...
