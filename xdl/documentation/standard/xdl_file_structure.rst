==================
XDL File Structure
==================

XDL files will follow XML syntax and consist of three mandatory sections: ``Hardware``, where virtual vessels that the reaction mixture can reside in are declared. ``Reagents``, where all reagents that are used in the procedure are declared, and ``Procedure``, where the synthetic actions involved in the procedure are linearly declared. An optional, but recommended Metadata section is also available for adding in extra information about the procedure. All sections are wrapped in an enclosing ``Synthesis`` tag.

XDL File Stub
*************

.. code-block:: xml

    <Synthesis>
        <Metadata>
            <!-- ... -->
        </Metadata>

        <Hardware>
            <!-- ... -->
        </Hardware>

        <Reagents>
            <!-- ... -->
        </Reagents>

        <Parameters>
            <!-- ... -->
        </Parameters>

        <Procedure>
            <!-- ... -->
        </Procedure>
    </Synthesis>

Enhanced XDL 1+ File Stub
*************************

XDL 1 also has an enhanced XDL XML syntax for providing additional context to syntheses. As of version 1.0.0, this is used to provide XMLBlueprint templates for executing procedures in the ``Synthesis`` section (see :ref:`bp_eg`).For full use of XMLBlueprints, the root
node ``XDL`` must enclose the ``Synthesis`` node.

It is recommended to use the ``XDL`` root node (as below) for all XDL files going forward, including those which do not contain blueprints.
However, non-blueprint containing XDL files (``Synthesis`` section only) with no ``XDL`` root node (as above), will also still be compatible.

.. code-block:: xml

    <XDL>
        <Synthesis>
            <Metadata>
                <!-- ... -->
            </Metadata>

            <Hardware>
                <!-- ... -->
            </Hardware>

            <Parameters>
                <!-- ... -->
            </Parameters>

            <Reagents>
                <!-- ... -->
            </Reagents>

            <Procedure>
                <!-- ... -->
            </Procedure>
        </Synthesis>
    </XDL>

Metadata
********

The optional ``Metadata`` section should contain extra information about the procedure.

Metadata
^^^^^^^^

Metadata associated with procedure.

.. csv-table::
   :quote: $
   :header: "Property", "Type", "Description"

   $``description``$, $``str``$, $Optional. Brief description of the synthesis.$
   $``publication``$, $``str``$, $Optional. Publication synthesis was taken from.$
   $``smarts``$, $``str``$, $Optional. SMARTS string of the transformation.$
   $``product``$, $``str``$, $Optional. Name of product.$
   $``product_inchi``$, $``str``$, $Optional. INCHI string of product.$
   $``product_cas``$, $``int``$, $Optional. CAS number of the product.$
   $``product_vessel``$, $``str``$, $Optional. Vessel that the product ends up in.$
   $``reaction_class``$, $``str``$, $Optional. Type of reaction being carried out. At the moment not limiting this to specific options, as reaction classification can be ambiguous.$

.. _paramclass:

Parameters
**********

The optional ``Parameters`` section can be used to define useful values (e.g. volumes, time or temperatures) that may be used multiple times in a given synthesis.
For details on how to use parameters, see :doc:`/standard/parameters`

Parameter
^^^^^^^^^

.. csv-table::
   :quote: $
   :header: "Property", "Type", "Description"

   $``id``$, $``str``$, Brief description of the synthesis.$
   $``parameter_type``$, $``str``$, Type of the parameter i.e. 'volume', 'temp', 'time'.$
   $``value``$, $``str``$, $Optional. Value for parameter. If no other value is specified when this parameter is used, it will be used as a default value.$
   $``min``$, $``str``$, $Optional. Minimum value for parameter.$
   $``max``$, $``str``$, $Optional. Maximum value for parameter.$

Reagents
********

The ``Reagents`` section contains ``Reagent`` elements with the props below.

Reagent
^^^^^^^

Reagent used by procedure.

.. csv-table::
   :quote: $
   :header: "Property", "Type", "Description"

   $``name``$, $``str``$, $Name of reagent$
   $``inchi``$, $``str``$, $Optional. INCHI string of reagent$
   $``cas``$, $``str``$, $Optional. CAS number of reagent$
   $``role``$, $``str``$, $Optional. Role of reagent. One of ``'reagent'``, ``'substrate'``, ``'catalyst'``, ``'acid'``, ``'base'``, ``'solvent'``, ``'ligand'``, ``'quenching-agent'`` or ``'activating-agent'``.$
   $``preserve``$, $``bool``$, $Optional. If ``True``, reagent is expensive and should be used sparingly.$
   $``use_for_cleaning``$, $``bool``$, $Optional. If ``True``, the reagent is cheap and can be used for cleaning.$
   $``clean_with``$, $``reagent``$, $Optional. Name of another reagent that should be used when cleaning vessels that have come into contact with this reagent.$
   $``stir``$, $``bool``$, $Optional. Stir reagent flask for the entire procedure.$
   $``temp``$, $``float``$, $Optional. Cool (or heat) reagent flask to given temperature for the entire procedure.$
   $``atmosphere``$, $``str``$, $Optional. Store reagent under given gas for entire procedure.$
   $``purity``$, $``float``$, $Optional. Purity of reagent in %.$

Procedure
*********
All steps included in the :doc:`/standard/full-steps-specification` may be given within the
``Procedure`` block of a XDL file. Additionally, the ``Procedure`` block may be, but does not have to be, divided up into ``Prep``, ``Reaction``, ``Workup`` and ``Purification`` blocks, each of which can contain any of the steps in the specification.

Example XDL snippet using optional Procedure subsections
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: xml

    <Procedure>

        <Prep>
            <!-- Preparation steps here, reagent additions etc. -->
        </Prep>

        <Reaction>
            <!-- Reaction steps here, heating and stirring etc. -->
        </Reaction>

        <Workup>
            <!-- Workup steps here, separation, evaporation etc. -->
        </Workup>

        <Purification>
            <!-- Purification steps here, column, distillation etc. -->
        </Purification>

    </Procedure>
