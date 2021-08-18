.. _ontology-ref:

Ontology Class
==============

.. autoclass:: ddotkit.Ontology
	       
Read/write Ontology objects
--------------------------------

.. automethod:: ddotkit.Ontology.from_table
.. automethod:: ddotkit.Ontology.to_table
.. automethod:: ddotkit.Ontology.read_pickle
.. automethod:: ddotkit.Ontology.to_pickle
.. automethod:: ddotkit.Ontology.to_ndex
.. automethod:: ddotkit.Ontology.from_ndex
.. automethod:: ddotkit.Ontology.to_cx
.. automethod:: ddotkit.Ontology.to_graphml

NetworkX and igraph
-------------------

.. automethod:: ddotkit.Ontology.to_networkx
.. automethod:: ddotkit.Ontology.from_networkx
.. automethod:: ddotkit.Ontology.from_igraph
.. automethod:: ddotkit.Ontology.to_igraph	
		
Inspecting structure
--------------------

.. automethod:: ddotkit.Ontology.connected
.. automethod:: ddotkit.Ontology.get_best_ancestors
.. automethod:: ddotkit.Ontology.topological_sorting
		
Manipulating structure
-----------------------

.. automethod:: ddotkit.Ontology.unfold
.. automethod:: ddotkit.Ontology.delete
.. automethod:: ddotkit.Ontology.focus
.. automethod:: ddotkit.Ontology.propagate

Inferring data-driven ontology
------------------------------

.. automethod:: ddotkit.Ontology.flatten
.. automethod:: ddotkit.Ontology.run_clixo
		
Aligning ontologies
-------------------

.. automethod:: ddotkit.Ontology.align
