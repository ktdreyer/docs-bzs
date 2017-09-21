This script searches for BZs that are interesting to the RH Ceph Storage docs
team.

* All BZs that have [RFE] in the summary (BZ rules always add the
``FutureFeature`` keyword here too.)
* All BZs that were known issues in previous versions and are fixed in this
  version.
* All BZs that have a customer case attached.

TODO:

* Find all BZs that remains known issues

* Automatically add candidate BZs to the Release Notes tracker bug

* Automatically determine the Release Notes tracker bug

* Automatically file a new Release Notes tracker bug if none can be found

To run this::

  sudo yum -y install python-prettytable python-bugzilla

  git clone https://github.com/ktdreyer/docs-bzs

  cd docs-bzs

  ./find.py

  OR

  ./find.py 2.4
