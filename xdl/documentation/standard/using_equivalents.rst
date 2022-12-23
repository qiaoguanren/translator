=================
Using Equivalents
=================

New to XDL 1, equivalents (``'eq', 'equivalents', 'equivs'``) can now be used as a unit for the addition of solids and liquids. This enables stoichiometric addition of reagents.

Defining Equivalent References and Equivalent Amounts
*****************************************************
In order for equivalents to be used as a unit, a reference reagent (``equiv_reference``) and equivalent amount (``equiv_amount``) need to be defined when the XDL is compiled by calling the ``prepare_for_execution`` method (see :ref:`Defining Equivalence References <equiv-ref>`). ``equiv_reference`` is the reference reagent
for all stoichiometric calculations.

The ``equiv_reference`` should be a reagent present in the ``Reagents`` section.
The ``equiv_amount`` is the value that corresponds to one equivalent of that reagent (in 'moles', 'g' or 'L' etc.).

From these values, the number of moles per one equivalent of reference reagent is calculated. This enables stoichiometric addition of reagents via use of the equivalent (``'eq'``) unit.
When a stoichiometric reference reagent has been provided and the ``'eq'`` unit is used for additions, the final volume / mass of reagents added are automatically scaled to this stoichiometric reference (see :ref:`equivcalcs`).


.. _equiv-ref:

Equivalent References in prepare_for_execution
----------------------------------------------
Equivalent reference (``equiv_reference``) and equivalent amount (``equiv_amount``) can be defined during prepare for execution:

.. code-block:: python

   from xdl import XDL

   x = XDL("example_xdl.xdl", platform)

   x.prepare_for_execution(
       graph_file,
       equiv_reference="example_reference",
       equiv_amount="1 g",
   )

These values will be used as the equivalent reference for any step using ``eq`` that does not have a specific equivalent reference (i.e. no :ref:`bp_equivs`)

.. _bp_equivs:

Blueprint-Specific Equivalent References
----------------------------------------
Individual blueprints can have unique equivalent references.
The (``equiv_reference``) must be a ``Reagent`` defined in the blueprint itself, not a global ``Reagent`` from the main Synthesis section.

For more information on how to use blueprints, please see :doc:`/standard/xdl_blueprints`.

.. code-block:: xml

   <XDL>
      <Blueprint id="blueprint_1">
         <Hardware>
            <Component id="reactor" type="reactor"/>
         </Hardware>

         <Reagents>
            <Reagent id="solid"/>
         </Reagents>

         <Procedure>
            <Add reagent="solid" vessel="reactor" amount="1 eq"/>
            <Wait time="0.5 min"/>
         </Procedure>
      </Blueprint>

      <Synthesis>
         <Hardware>
            <Component id="reactor_1" type="reactor"/>
         </Hardware>

         <Reagents>
            <Reagent name="example_solid" solid="true" molecular_weight="155.155 g/mol"/>
         </Reagents>


         <Procedure>
            <blueprint_1
               solid="example_solid"
               reactor="reactor_1"
               equiv_reference="solid"
               equiv_amount="0.5 g"/>
         </Procedure>
      </Synthesis>
   </XDL>


Defining a global ``equiv_reference`` and ``equiv_amount`` (in ``prepare_for_execution``) will not overwrite blueprint-specific equivalents.
However, if a blueprint does not have a unique ``equiv_reference`` and ``equiv_amount`` defined when the blueprint is used, it will use the global ``equiv_reference`` and ``equiv_amount`` values.

Using the Equivalents Unit
**************************

The steps that currently support the use of the 'equivalence' units are ``Add``, ``Dissolve``, ``Precipitate`` and ``Transfer``.
Adding a certain number of equivalents of a given reagent can be specified using the amount property of the above steps.

For example,

.. code-block:: xml

   <Procedure>

      <Add reagent="reagent_1" vessel="reactor" amount="1 eq"/>

      <Transfer
         from_vessel="reagent_2"
         to_vessel="reactor"
         amount="100 eq"
         time="10 min"
         rinsing_volume="1 mL"
         rinsing_repeats="3"
         rinse_withdrawal_excess="0.0"/>

   </Procedure>

.. _equivcalcs:

Equivalence Calculations
************************
Depending on the scenario in which equivalents is used, certain combinations of ``Reagent`` properties are required to calculate the final amount.

.. _amountcalcs:

Calculating Mass and Volume from 'amount'
-----------------------------------------
Depending on the scenario in which amount is used, certain combinations of ``Reagent`` properties are required to calculate the final amount.

Calculations For Liquid Reagents
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

+---------------------------------------+------------------------------+-------------------+---------------------------+
|Amount Unit Conversion                 |``molecular_weight``          |``density``        |``concentration``          |
|                                       |                              |                   |                           |
+=======================================+==============================+===================+===========================+
|``mass (g)`` to ``volume (mL)``        |                              |   ✓               |                           |
|                                       +------------------------------+-------------------+---------------------------+
|                                       |✓                             |                   |✓                          |
+---------------------------------------+------------------------------+-------------------+---------------------------+
|``moles (mmol)`` to ``volume (mL)``    |                              |                   |   ✓                       |
|                                       +------------------------------+-------------------+---------------------------+
|                                       |✓                             |✓                  |                           |
+---------------------------------------+------------------------------+-------------------+---------------------------+
|``equivalents (eq)`` to ``volume (mL)``|                              |                   |   ✓                       |
|                                       +------------------------------+-------------------+---------------------------+
|                                       |✓                             |✓                  |                           |
+---------------------------------------+------------------------------+-------------------+---------------------------+

For example, to ``Add`` 5 g of a liquid reagent (convert to mL), you would need its density or both it's molecular weight and concentration.

Calculations For Solid Reagents
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

+---------------------------------------+------------------------------+-------------------+---------------------------+
| Amount Unit Conversion                |``molecular_weight``          |``density``        |``concentration``          |
+=======================================+==============================+===================+===========================+
|    ``moles (mmol)`` to ``mass (g)``   |✓                             |                   |                           |
+---------------------------------------+------------------------------+-------------------+---------------------------+
|``equivalents (eq)`` to ``mass (g)``   |✓                             |                   |                           |
+---------------------------------------+------------------------------+-------------------+---------------------------+
