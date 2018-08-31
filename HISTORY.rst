.. :changelog:

History
-------

0.1.2 (2018-08-30)
~~~~~~~~~~~~~~~~~~

* Fix bug by attaching SQLAlchemy events at most once.
  Otherwise in some cases when multiple threads are used,
  event handlers ``deque`` would be mutated while
  other SQLAlchemy events are running since
  event handling is not thread-safe in SQA.

0.1.1 (2018-07-13)
~~~~~~~~~~~~~~~~~~

* Fix bug which did not correctly track plain string clauses.

0.1.0 (2017-10-04)
~~~~~~~~~~~~~~~~~~

* First release on PyPI.
