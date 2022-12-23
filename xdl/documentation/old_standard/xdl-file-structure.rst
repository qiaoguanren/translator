
==================
XDL File Structure
==================

XDL files will follow XML syntax and consist of three mandatory sections: ``Hardware``, where virtual vessels that the reaction mixture can reside in are declared. ``Reagents``, where all reagents that are used in the procedure are declared, and ``Procedure``, where the synthetic actions involved in the procedure are linearly declared. An optional, but recommended Metadata section is also available for adding in extra information about the procedure. All sections are wrapped in an enclosing ``Synthesis`` tag.

XDL File Stub
*************

.. code-block:: xml

   <Synthesis>

    <Metadata>

    </Metadata>

    <Hardware>

    </Hardware>

    <Reagents>

    </Reagents>

    <Procedure>

    </Procedure>

   </Synthesis>

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
All steps included in the :doc:`/old_standard/full-steps-specification` may be given within the
``Procedure`` block of a XDL file. Additionally, the ``Procedure`` block may be, but does not have to be, divided up into ``Prep``, ``Reaction``, ``Workup`` and ``Purification`` blocks, each of which can contain any of the steps in the specification.

Example XDL snippet using optional Procedure subsections
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
