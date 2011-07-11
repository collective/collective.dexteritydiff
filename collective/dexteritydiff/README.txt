Introduction
============

Provide the ``DexterityCompoundDiff`` diff type for `Products.CMFDiffTool`_, analogous to 
``ATCompoudDiff``.

This is a package to help enable content versioning for Dexterity_ content types. To enable 
versioning for a Dexterity content type you need to:

1. Install `plone.app.versioningbehavior`_ and use it on your content type.
2. Enable versioning for the type in the types control panel.
3. Install this package.
4. Go to the ``portal_diff`` tool ZMI page.
5. Add ``Compound Diff for Dexterity types`` for your content type. ``Field name`` can be anything,
   e.g: "any".

You can enable versioning on Dexterity content types without this package, but then you'll have
to add the correct "diff type" for each field of your content type.

.. References
.. _`Products.CMFDiffTool`: http://pypi.python.org/pypi/Products.CMFEditions
.. _Dexterity: http://pypi.python.org/pypi/plone.app.dexterity
.. _`plone.app.versioningbehavior`: http://pypi.python.org/pypi/plone.app.versioningbehavior
