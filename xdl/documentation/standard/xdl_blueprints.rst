==============
XDL Blueprints
==============

What is a Blueprint?
********************
A blueprint is an ordered template of steps that can be reused multiple times
throughout a synthesis.
A blueprint allows for general reagents, hardware and experimental conditions to
be defined and mapped to specific values when the blueprint is declared.

General Blueprint Structure
***************************
As with standard XDL files, :doc:`/standard/xdl_file_structure`, blueprints follow
the XML syntax and can include four sections: 'Hardware', 'Reagents', 'Parameters'
and 'Procedure'.
All blueprint sections are wrapped in an enclosing ``Blueprint`` tag,
which has an associated ``id``.

``Synthesis`` and ``Blueprint`` sections can be in the same .xdl file.
The ``Blueprint`` and ``Synthesis`` sections are enclosed in a ``XDL`` tag (see :ref:`bp_eg`).

For information on using blueprints from different locations, please see :ref:`wd_bps`.

An example blueprint for a basic Grignard reaction is shown below.

.. code-block:: xml

   <Blueprint id='Grignard'>
        <Hardware>
            <Component id='reactor' type='reactor'/>
        </Hardware>

        <Parameters>
            <Parameter id='reaction_time' type='time' value='12 h'/>
            <Parameter id='reaction_temp' type='temp'/>
        </Parameters>

        <Reagents>
            <Reagent id='grignard_reagent'/>
            <Reagent id='carbonyl'/>
            <Reagent id='reaction_solvent'/>
        </Reagents>

        <Procedure>
            <Add reagent='carbonyl' vessel='reactor' amount='2 eq'/>
            <Add reagent='solvent' vessel='reactor' amount='2 mL'/>
            <Add reagent='grignard_reagent' vessel='reactor' amount='1 eq' time='5 min'/>

            <!-- Parameter values used for temp and time -->
            <HeatChill
                vessel='reactor'
                temp='reaction_temp'
                time='reaction_time'
                stir='true'/>
        </Procedure>
    </Blueprint>

The above blueprint example uses parameter values for the reaction time and
temperature, for more information on internal blueprint parameter please
see :ref:`bp_params`.
It also uses equivalents as a unit for the addition of reagents, for more
information on the equivalents unit please see :doc:`/standard/using_equivalents`.

Using a Blueprint in A Synthesis
********************************

A blueprint can be used as a standard step in the ``Procedure`` section of the
``Synthesis``.
It is here that general blueprint values, such as components, parameters and
reagents can be mapped to a standard component from the ``Synthesis`` section.

.. code-block:: xml

    <Synthesis>
         <Hardware>
            <Component id='reactor' type='reactor'/>
         </Hardware>

         <Reagents>
            <Reagent name='phenylmagnesium bromide' molecular_weight='181.31 g/mol' density='1.14 g/mL'/>
            <Reagent name='sodium methyl carbonate' solid=True molecular_weight='98.03 g/mol'/>
            <Reagent name='HCl' concentration="2M" molecular_weight='36.458 g/mol'/>
            <Reagent name='THF' role="solvent"/>
         </Reagents>

         <Procedure>

            <!-- use of blueprint step -->
            <Grignard
               grignard_reagent='phenylmagnesium bromide'
               carbonyl='sodium methyl carbonate'
               reaction_solvent='THF'
               reaction_time='24 h'
               reaction_temp='25 °C'
               equiv_reference="grignard_reagent"
               equiv_amount="1 mmol"
            />

            <!-- use of non-blueprint step -->
            <Add
               vessel="reactor"
               reagent="HCl"
               volume="15 mL"
               stir="True"
               stir_speed="350" />

         </Procedure>
   </Synthesis>

Using Default Reagents within a Blueprint
*****************************************
If a reagent will not change throughout use of the blueprint, it can be set as a 'default' reagent.
Default reagents can be defined in the ``Reagents`` section of the blueprint.

They must be defined with a ``name`` that is unique (not the same as a Reagent, Component or Parameter ``id`` within the blueprint).
The ``name`` must also correspond to a vessel on a graph that is used alongside the blueprint.

In the following example 'THF' is defined as a default Reagent. It will not need to be mapped to ``Synthesis`` section reagent
during blueprint use.

.. code-block:: xml

   <Blueprint id='Grignard'>
      ...
        <Reagents>
            <Reagent id='grignard_reagent'/>
            <Reagent id='carbonyl'/>

            <!-- Default reagent 'THF' defined -->
            <Reagent name="THF" id="BP_solvent" molecular_weight="72.11 g/mol" density="0.889 g/mL" role="solvent"/>

        </Reagents>

        <Procedure>
            <Add reagent='carbonyl' vessel='reactor' amount='2 eq'/>
            <Add reagent='THF' vessel='reactor' amount='2 mL'/>
            <Add reagent='grignard_reagent' vessel='reactor' amount='1 eq' time='5 min'/>
            <HeatChill
                vessel='reactor'
                temp='30 °C'
                time='24 h'
                stir='true'/>
            ...
        </Procedure>
    </Blueprint>

Default reagents can be overwritten by explicitly mapping it's ``id`` during blueprint use.
This can be useful for updating properties of a reagent, e.g. concentration or swapping a reagent entirely.

In the example below, 'THF', which has ``id = BP_solvent`` is replaced with 'DMF' for the reaction (in the second Add step, 2 mL of DMF will be added).

.. code-block:: xml

    <Synthesis>
         <Hardware>
            <Component id="reactor" type="reactor"/>
         </Hardware>

         <Reagents>
            <Reagent name="phenylmagnesium bromide" molecular_weight="181.31 g/mol" density="1.14 g/mL"/>
            <Reagent name="sodium methyl carbonate" solid=True molecular_weight="98.03 g/mol"/>
            <Reagent name="HCl" concentration="2M" molecular_weight="36.458 g/mol"/>
            <Reagent name="DMF" role="solvent"/>
         </Reagents>

         <Procedure>

            <!-- use of blueprint step -->
            <Grignard
               reactor="reactor"
               grignard_reagent="phenylmagnesium bromide"
               carbonyl="sodium methyl carbonate"
               BP_solvent="DMF"
               equiv_reference="grignard_reagent"
               equiv_amount="1 mmol"
            />
            <!-- overwriting THF default reagent using its 'id' by setting BP_solvent="DMF" -->
            ...
         </Procedure>
   </Synthesis>

.. _bp_eg:

Complete Blueprint XDL Example
******************************
As mentioned above, in this current version of XDL, blueprints must be in the same .xdl file as the Synthesis that utilises them.
A complete example of a blueprint-containing XDL file, based on the previous examples in this section is shown below.

.. code-block:: xml

   <XDL>
      <!-- blueprint defined -->
      <Blueprint id='Grignard'>
         <Hardware>
            <Component id='reactor' type='reactor'/>
         </Hardware>

         <Parameters>
            <Parameter id='reaction_time' type='time' value='12 h'/>
            <Parameter id='reaction_temp' type='temp'/>
         </Parameters>

         <Reagents>
            <Reagent id='grignard_reagent'/>
            <Reagent id='carbonyl'/>
            <Reagent id='reaction_solvent'/>
         </Reagents>

         <Procedure>
            <Add reagent='carbonyl' vessel='reactor' amount='2 eq'/>
            <Add reagent='solvent' vessel='reactor' amount='2 mL'/>
            <Add reagent='grignard_reagent' vessel='reactor' amount='1 eq' time='5 min'/>
            <!-- Parameter values used for temp and time -->
            <HeatChill
               vessel='reactor'
               temp='reaction_temp'
               time='reaction_time'
               stir='true'/>
         </Procedure>
      </Blueprint>

      <!-- synthesis section -->
      <Synthesis>
         <Hardware>
            <Component id='reactor' type='reactor'/>
         </Hardware>

         <Reagents>
            <Reagent name='phenylmagnesium bromide' molecular_weight='181.31 g/mol' density='1.14 g/mL'/>
            <Reagent name='sodium methyl carbonate' solid=True molecular_weight='98.03 g/mol'/>
            <Reagent name='HCl' concentration="2M" molecular_weight='36.458 g/mol'/>
            <Reagent name='THF' role="solvent"/>
         </Reagents>

         <Procedure>

            <!-- use of blueprint step -->
            <Grignard
               grignard_reagent='phenylmagnesium bromide'
               carbonyl='sodium methyl carbonate'
               reaction_solvent='THF'
               reaction_time='24 h'
               reaction_temp='25 °C'
               equiv_reference="grignard_reagent"
               equiv_amount="1 mmol"
            />

            <!-- use of non-blueprint step -->
            <Add
               vessel="reactor"
               reagent="HCl"
               volume="15 mL"
               stir="True"
               stir_speed="350" />

         </Procedure>
      </Synthesis>
   </XDL>

Scaling Values Based on Equivalents
***********************************
New to XDL 1, equivalents can now be used as a unit for steps: :ref:`bp_equivs`.

For blueprint steps, you may also scale values by equivalents, based on a
``base_scale`` defined in the ``Procedure`` section of a given blueprint.

The ``base_scale`` refers to scale in which procedure has been developed / scale
in which solvent volumes etc. have been determined
The units of base scale must be in moles per equivalent (mol / eq).

By using 'unit/eq' as a unit for amount, where unit may be 'mL', 'g', 'mmol',
quantities can be scaled based on the ratio between the ``'base_scale'`` of a
procedure and the 'amount per equivalent' for the blueprint, which is determined
by the equivalence reference and amount.
Add, Dissolve, Transfer and Precipiate are amongst the steps compatible with this unit.

In the following example, we have ``equiv_reference='PPh3'`` and  ``equiv_amount='2.62 g'``.
Therefore, the moles per equivalent for this blueprint is ``0.001 mol`` (mass = 2.62 g, molecular weight = 262.29 g/mol).

The ``base_scale`` for the blueprint is ``"0.005 mol / eq"``, five times the value for moles per equivalent.
This means that every quantity in steps using the "unit / eq" unit will be scaled by 0.2 (divided by 5).

.. code-block:: xml

   <XDL>
      <Blueprint id="example_scaling">
         <Hardware>
            <Component
               id="reactor"
               type="reactor" />
         </Hardware>

         <Reagents>
            <Reagent id="reagent"/>
            <Reagent id="phosphine"/>
         </Reagents>

         <!-- base scale defined-->
         <Procedure base_scale="0.005 mol / eq">

            <!-- scaled amount used -->
            <Add reagent="phosphine" vessel="reactor" amount="20 mg / eq"/>
            <Add reagent="reagent" vessel="reactor" amount="15 mg / eq"/>

            <!-- scaled volume used -->
            <Dissolve
               vessel="reactor"
               solvent="THF"
               amount="2 mL / eq"
               time="60 s" />
         </Procedure>
      </Blueprint>

      <Synthesis>
         <Hardware>
            <Component
               id="reactor"
               type="reactor" />
         </Hardware>

         <Reagents>
            <Reagent name="Z-Hyp-OH" molecular_weight="265.26 g/mol" solid="true" role="reagent"/>
            <Reagent name="PPh3" molecular_weight="262.29 g/mol" solid="true" role="reagent"/>
            <Reagent name="THF" molecular_weight="72.11 g/mol" density="0.889 g/mL" role="solvent"/>
         </Reagents>

         <Procedure>
            <example_scaling
               reagent="Z-Hyp-OH"
               phosphine="PPh3"
               equiv_reference="phosphine"
               equiv_amount="2.62 g"
            />
         </Procedure>
      </Synthesis>
   </XDL>

The final amounts for the above example will be:

.. code-block:: xml

   <Add reagent="phosphine" vessel="reactor" amount="4 mg"/>

   <Add reagent="reagent" vessel="reactor" amount="3 mg"/>

   <Dissolve
      vessel="reactor"
      solvent="THF"
      amount="0.4 mL"
      time="60 s" />

Nested Blueprints
*****************
It is possible to use another blueprint as a step in a blueprint.
Values for blueprint substeps are defined when the 'parent' blueprint is declared (as above).

.. code-block:: xml

   <XDL>
      <Blueprint id="parent_blueprint">

         <Reagents>
            <Reagent id="reagent"/>
            <Reagent id="phosphine"/>
         </Reagents>

         <Procedure>

            <!-- mapping of blueprint substep values-->
            <child_blueprint
               reagent="reagent"
               phosphine="phosphine"
            />

         </Procedure>
      </Blueprint>

      <Blueprint id="child_blueprint">

         <Hardware>
            <Component
               id="reactor"
               type="reactor" />
         </Hardware>

         <Reagents>
            <Reagent id="reagent"/>
            <Reagent id="phosphine"/>
         </Reagents>

         <!-- base scale defined-->
         <Procedure base_scale="0.005 mol/eq">

            <!-- scaled amount used -->
            <Add reagent="phosphine" vessel="reactor" amount="20 mg / eq"/>
            <Add reagent="reagent" vessel="reactor" amount="15 mg / eq"/>

            <!-- scaled volume used -->
            <Dissolve
               vessel="reactor"
               solvent="THF"
               amount="2 mL / eq"
               time="60 s" />
         </Procedure>
      </Blueprint>

      <Synthesis>
         <Hardware>
            <Component
               id="reactor"
               type="reactor" />
         </Hardware>

         <Reagents>
            <Reagent name="Z-Hyp-OH" molecular_weight="265.26 g/mol" solid="true" role="reagent"/>
            <Reagent name="PPh3" molecular_weight="262.29 g/mol" solid="true" role="reagent"/>
            <Reagent name="THF" molecular_weight="72.11 g/mol" density="0.889 g/mL" role="solvent"/>
         </Reagents>

         <Procedure>
            <parent_blueprint
               reagent="Z-Hyp-OH"
               phosphine="PPh3"
               equiv_reference="phosphine"
               equiv_amount="2.62 g"
            />
         </Procedure>
      </Synthesis>
   </XDL>

.. _wd_bps:

Using Blueprints From Different Locations
*****************************************
In previous examples, we have seen blueprints define in the same file as the synthesis section that invokes them.
It is also possible to use blueprints from the other locations by specifying a ``working_directory`` or setting up the environment variable ``XDLPATH``.

For a given XDL file (.xdl), if blueprint is used as a step in the Synthesis section but the blueprint cannot be found in the same file, it will look for
the blueprint in other locations.

You can specify a specific folder to resolve blueprints from by providing the xdl constructor with the argument ``working_directory``:

.. code-block:: python

   from xdl import XDL

   x = XDL(
       xdl="example_xdl.xdl",
       platform,
       working_directory="C:/Documents/the_folder_with_all_my_blueprints_in",
   )

   x.prepare_for_execution(
       graph_file,
       equiv_reference="example_reference",
       equiv_amount="1 g",
   )

You can also set up an environment variable called ``XDLPATH`` to define a 'default' folder to search for blueprints.

If a blueprint with matching ``id`` to the unknown step in the synthesis section cannot be found in the same .xdl file,
XDL will try to search for missing blueprints in the following order:

1. If a ``working_directory`` was specified to the XDL constructor, look in the working_directory folder.
2. If ``XDLPATH`` is set as an environment variable, look in ``XDLPATH``.
3. Look for the blueprint in the same folder as the current file.
4. If the above fail, raise an error that the step is not valid.

An error will also be raised if there is more than one blueprint with an 'id' that matches the unknown step.
