=====================
Iteration with Repeat
=====================

In previous versions of XDL (< XDL 1.0), Repeat could be used to repeat a set of steps 'n' number of times.
In the example below, the Add step would be Repeated 3 times:

.. code-block:: xml

   <Repeat repeats="3">
      <Add reagent="reagent" vessel="reactor"/>
   </Repeat>

The Repeat step can now be used for iteration, similar to a ``for`` loop.

'Loop variables' for Hardware or Reagents can be included within a ``<Repeat>`` and the loop body (Repeat substeps) will be executed
for all possible matching values.

Iteration Syntax
****************

A loop variable can be used within a ``Repeat`` substep.
The loop variable specifications must be included in the ``Repeat`` tag in the format ``loop_variable.specification = specification_value``.

The following example will add all liquid reagents to a fixed reactor.
The loop variable (``my_reagent``) will be used to match all liquid reagents (``solid="False"``) so the final syntax in the ``Repeat``
will be ``<Repeat my_reagent.solid="False">``.

.. code-block:: xml

   <Repeat my_reagent.solid="False">
      <Add reagent="my_reagent" vessel="reactor"/>
   </Repeat>

When multiple variables are included within the same ``Repeat``, we take
one of each in each iteration, behaving like a zip iterator in Python.
Iteration stops when the shortest match list has been exhausted.

The example below will match all available solvents and put them in different reactors.

.. code-block:: xml

   <Repeat my_reagent.role="solvent" rx_vessel.type="reactor">
      <Add reagent="my_reagent" vessel="rx_vessel"/>
   </Repeat>

``Repeat`` can also be nested in order to iterate over all combinations of matches.
The following example will add all combinations of Reagents with the role ``acid`` and ``base`` to a different ``reactor`` (
one acid and one base per reactor).

.. code-block:: xml

   <Repeat new_reactor.type="reactor">
      <Repeat my_acid.role="acid">
         <Repeat my_base.role="base">
            <Add reagent="my_acid" vessel="new_reactor"/>
            <Add reagent="my_base" vessel="new_reactor"/>
         </Repeat>
      </Repeat>
   </Repeat>

It is also possible to specify multiple clauses for the same loop variable.
In the example below, all Reagents with the role ``substrate`` that are liquids (``solid = False``) will be added.

.. code-block:: xml

   <Repeat my_reagent.solid="False" my_reagent.role="substrate">
      <Add reagent="my_reagent" vessel="reactor"/>
   </Repeat>

It is also possible to iterate through all ``Reagents`` or ``Hardware`` in a given XDL file
by specifying the ``kind`` of loop variable:

.. code-block:: xml

   <!-- Add all reagents to the same reactor -->
   <Repeat my_reagent.kind="Reagent">
      <Add reagent="my_reagent" vessel="reactor"/>
   </Repeat>

.. code-block:: xml

   <!-- Add the same acid into each Hardware component -->
   <Repeat my_reactor.kind="Hardware">
      <Add reagent="acid" vessel="my_reactor"/>
   </Repeat>

.. code-block:: xml

   <!-- Add all reagents into all reactors -->
   <Repeat my_reagent.kind="Reagent">
      <Repeat my_reactor.kind="Hardware">
         <Add reagent="my_reagent" vessel="my_reactor"/>
      </Repeat>
   </Repeat>

**Note:** It is currently possible to have only one match clause / specification per loop variable. In the XDL1.6 release, multiple matching clauses will be defined to act like logical ``and`` statements.

Full Iterative Repeat Examples
******************************

Example 1: Single reactor, single variable reagents
---------------------------------------------------
Run Grignard reactions using all possible halides in a single reactor:

.. code-block:: xml

   <Synthesis>

      <Hardware>
         <Component
            id="reactor1"
            type="reactor"
         />
      </Hardware>

      <Reagents>
         <Reagent
            name="3-methylbromobenzene"
            role="substrate" />
         <Reagent
            name="iodobenzene"
            role="substrate" />
         <Reagent
            name="magnesium" />
      </Reagents>

      <Procedure>
         <Repeat rx.role="substrate">
            <GrignardReaction
                  halide="rx"
                  reactor="reactor1"
                  equiv_reference="rx_substrate"
                  equiv_amount="1 mol" />
         </Repeat>
      </Procedure>

   </Synthesis>

Example 2: Multiple reactors, single variable reagent
-----------------------------------------------------
Run Grignard reactions using all possible halides in different reactors.

.. code-block:: xml

   <Synthesis>

      <Hardware>
         <Component
            id="reactor1"
            type="reactor"
         />
         <Component
            id="reactor2"
            type="reactor"
         />
      </Hardware>

      <Reagents>
         <Reagent
            name="3-methylbromobenzene"
            role="substrate" />
         <Reagent
            name="iodobenzene"
            role="substrate" />
         <Reagent
            name="magnesium" />
      </Reagents>

      <Procedure>
         <Repeat rx.role="substrate" reactor.type="reactor">
            <GrignardReaction
                  halide="rx"
                  reactor="reactor"
                  equiv_reference="rx_substrate"
                  equiv_amount="1 mol"
               />
         </Repeat>
      </Procedure>

   </Synthesis>

Example 3: Single reactor, multiple reagents
--------------------------------------------
Run all possible Ugi reactions (8 in this case).

.. code-block:: xml

   <Synthesis>

      <Hardware>
         <Component
            id="reactor1"
            type="reactor"
         />
      </Hardware>

      <Reagents>
         <Reagent
            name="allyl amine"
            role="amine" />
         <Reagent
            name="benzyl amine"
            role="amine" />
         <Reagent
            name="benzaldehyde"
            role="aldehyde" />
         <Reagent
            name="2-iodobenzaldehyde"
            role="aldehyde" />
         <Reagent
            name="cyclohexyl isocyanide"
            role="isocyanide" />
         <Reagent
            name="t-butyl isocyanide"
            role="isocyanide" />
         <Reagent
            name="2-iodobenzoic acid"
            role="acid" />
      </Reagents>

      <Procedure>
         <Repeat amine.role="amine">
            <Repeat aldehyde.role="aldehyde">
               <Repeat isocyanide.role="isocyanide">
                  <Repeat acid.role="acid">
                  <UgiReaction
                        amine="amine"
                        aldehyde="aldehyde"
                        isocyanide="isocyanide"
                        acid="acid"
                        reactor="reactor1" />
                  </Repeat>
            </Repeat>
         </Repeat>
      </Procedure>

   </Synthesis>
