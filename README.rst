Data-Driven Ontology Toolkit v2 (ddotontology)
------------------------------------------------

The Data-Driven Ontology Toolkit (DDOT) facilitates the inference, analysis, and
visualization of biological hierarchies using a data structure called an ontology.

- Open-source Python package under MIT license. Supports Python >=3.6.
- The `HiView <http://hiview.ucsd.edu>`__ web application visualizes
  hierarchical structure and the biological evidence for that structure.

.. note::

    This is an **updated** version of `DDOT <https://github.com/michaelku/ddot>`__.
    Changes from original:

    * Renamed from ``ddot`` to ``ddotontology`` to enable Pypi installation.
    * Updates to maintain compatibility with new version of
      `HiView <https://github.com/idekerlab/hiview>`__
    * A new script ``tohiview.py`` and a
      `tutorial <https://github.com/idekerlab/ddot/blob/master/examples/1.0.1_HiView_tutorial/hiview_tutorial.ipynb>`__
      of uploading to HiView server has been added
    * Running `CliXO 0.3 <https://github.com/mhk7/clixo_0.3>`__,
      `CliXO 1.0 <https://github.com/fanzheng10/CliXO-1.0>`__ and
      `alignOntology <https://github.com/mhk7/alignOntology>`__ from DDOT is
      no longer supported (in order to make this package lighter and more "Pythonic").
      Please visit the original repositories of these programs.
    * Support for Python 2 has been dropped

Documentation
*********************

For a quick start on DDOT's functionality, please see the `tutorial <examples/Tutorial.ipynb>`__ and other Jupyter notebooks in the [examples](examples) folder.


DDOT requires the following software

* Python >=3.6
* `numpy <https://docs.scipy.org/doc>`__
* `scipy <https://docs.scipy.org/doc>`__
* `pandas>=0.20 <http://pandas.pydata.org>`__
* `networkx>2.0 <https://networkx.github.io>`__
* `ndex2-client <https://pypi.org/project/ndex2/>`__
* `python-igraph <https://pypi.python.org/pypi/python-igraph>`__
* `tulip-python <https://pypi.python.org/pypi/tulip-python>`__


Citing DDOT
--------------

If you find DDOT helpful in your research, please cite

Michael Ku Yu, Jianzhu Ma, Keiichiro Ono, Fan Zheng, Samson H Fong,
Aaron Gary, Jing Chen, Barry Demchak, Dexter Pratt, Trey Ideker.
`DDOT: A Swiss Army Knife for Investigating Data-Driven Biological Ontologies <https://doi.org/10.1016/j.cels.2019.02.003>`__. Cell Systems. 2019 Mar 27;8(3):267-273.
