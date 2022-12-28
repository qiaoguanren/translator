==========
Parameters
==========


Defining Parameters
*******************

The optional ``Parameters`` section can be used to define useful values (e.g. volumes, time or temperatures) that may be used multiple times in a given synthesis.
For details on the ``Parameter`` class, see :ref:`paramclass`.


General Parameters Syntax
-------------------------

Parameters are defined in their own section, see :doc:`/standard/xdl_file_structure`.
Each parameter needs to have an ``id`` and ``type`` defined. The `id`` must be completely unique
- two parameters in the same ``Parameters`` section cannot have the same ``id`` nor can the `id`` be duplicated in Parameters, Reagents, or Hardware.

Example ``type`` values for ``Parameter`` include ``'time'``, ``'volume'`` and ``'temp'``.
Both the ``id`` and ``type`` are required to map the correct value when a ``Parameter`` is used in a step.

A ``value`` can also be defined for a given ``Parameter``, but this is optional. If no other value for a parameter is given (during blueprint instantiation
or XDL compilation), this value will be used as a 'default'.

An example ``Parameters`` section is shown below.

.. code-block:: xml

   <Parameters>
      <Parameter id='rxn_time' type='time' value='8 h'/>
      <Parameter id='solvent_volume' type='volume' value='10 mL'/>
      <Parameter id='rxn_temp' type='temp' value='27°C'/>
   </Parameters>

Using Parameters
****************

General Syntax
--------------
The values for specific properties in a ``Step`` can be replaced by a parameter value.

The value for these properties must match the ``id`` of their target ``Parameter`` object. The ``type`` property in the parameter must match the type of attribute that the parameter value is being used for.

For example, to use a parameter which has ``type='volume'`` and an ``id='solvent_volume'`` for the ``volume`` attribute in an ``Add`` Step, the following syntax is required:

.. code-block:: xml

   <Add
      vessel='reactor'
      reagent='solvent'
      volume='solvent_volume'
   />

.. _Params:

Another example for clarification, where the property of the ``Step`` is different from the ``type``:

.. code-block:: xml

   <Distill
      vessel='reactor'
      vapour_temp='rxn_temp'
   />


Example 1: Using Parameters within a Synthesis
----------------------------------------------
For parameters in the ``<Synthesis>`` section of a XDL, a `value` can be supplied when the ``Parameter`` is defined.

.. code-block:: xml

   <Synthesis>
      <Hardware>
         <Component id='reactor_1' type='reactor'/>
      </Hardware>

      <!-- defining parameter values -->
      <Parameters>
         <Parameter id='rxn_time' type='time' value='8 h'/>
         <Parameter id='solvent_volume' type='volume' value='10 mL'/>
         <Parameter id='rxn_temp' type='temp' value='27°C'/>
      </Parameters>

      <Reagents>
         <Reagent name='solvent'/>
      </Reagents>

      <Procedure>

         <!-- use of parameter value for volume -->
         <Add
            vessel='reactor_1'
            reagent='solvent'
            volume='solvent_volume'/>


         <!-- use of parameter values for temperature and time -->
         <HeatChill
            vessel='reactor_1'
            temp='rxn_temp'
            time='rxn_time'
            stir='true'/>

      </Procedure>
   </Synthesis>


Alternatively, values can be supplied to the XDL constructor. In this case, a dictionary of the format ``{parameter id: parameter value}``
can be used to set any parameter values for parameters defined in the synthesis section.

.. code-block:: python

   x = XDL(
       xdl_file,
       platform,
       parameters={
           "parameter_1": "value_1",
           "parameter_2": "value_2",
           "parameter_3": "value_3",
       },
   )


If a parameter in the synthesis section is defined with a value, this 'default' value will be overwritten by the value provided to the XDL constructor.

.. _bp_params:

Example 2: Using Parameters in Blueprints
-----------------------------------------
Every ``Blueprint`` that uses parameter values must have its own ``<Parameters>`` section.

Parameter values can be assigned when a blueprint is used in the ``<Synthesis>`` section of a XDL, so defining ``value`` is optional for blueprint parameters.
If no value is provided when using the blueprint and there is a value defined in the blueprint parameter section, this 'default' value will be used.

If there is a 'default' value defined, and a 'new' value is assigned to a given parameter when the blueprint is used in the ``<Synthesis>`` section of a XDL, it is the 'new' value that will be used.

The parameter value is assigned by passing the ``id`` of the parameter as an argument when the blueprint is used.

For example:

.. code-block:: xml

   <XDL>
      <Blueprint id='simple_reaction'>
         <Hardware>
            <Component id='reactor' type='reactor'/>
         </Hardware>

         <Parameters>
            <Parameter id='rxn_time' type='time' value='8 h'/>
            <Parameter id='solvent_volume' type='volume'/>
            <Parameter id='rxn_temp' type='temp' value='27°C'/>
         </Parameters>

         <Reagents>
            <Reagent id='solid'/>
         </Reagents>

         <Procedure>
            <Add reagent='solid' vessel='reactor' amount='0.5 g'/>

            <!-- use of parameter values for solvent volume -->
            <Add reagent='solvent' vessel='reactor' volume='solvent_volume'/>

            <!-- use of parameter values for temperature and time -->
            <HeatChill
               vessel='reactor'
               temp='rxn_temp'
               time='rxn_time'
               stir='true'/>

         </Procedure>
      </Blueprint>

      <Synthesis>
         <Hardware>
            <Component id='reactor_1' type='reactor'/>
         </Hardware>

         <Reagents>
            <Reagent name='example_solid' solid='true' molecular_weight='155.155 g/mol'/>
            <Reagent name='acetonitrile'/>
         </Reagents>

         <Procedure>
            <!-- specifying values for rxn_time and solvent_volume -->
            <simple_reaction
               solid='example_solid'
               solvent='acetonitrile'
               reactor='reactor_1'
               rxn_time='10 h'
               solvent_volume='10 mL'
            />
            <!-- rxn_temp not specified here so default value (27°C) will be used -->
         </Procedure>
      </Synthesis>
   </XDL>


In the above example, there are three parameter values used in the ``simple_reaction`` blueprint:

* For ``rxn_time``, there is a default value of ``'8 h'`` but a value (``'10 h'``) is provided when the blueprint is invoked. The final value used will be ``'10 h'``.
* For ``solvent_volume``, there is no default value and a value (``'10 mL'``) is provided when the blueprint is invoked. The final value used will be ``'10 mL'``.
* For ``rxn_temp``, there is a default value (``'27°C'``) and no value is provided during the blueprint declaration. The final value will be ``'27°C'``.


Please see :doc:`/standard/xdl_blueprints` for more information on how to use ``Blueprints``.

Example 3: Using Parameters in Blueprint Steps
----------------------------------------------
Both the ``<Synthesis>`` section of a XDL and individual blueprints can have parameter sections.
It is possible to use ``<Synthesis>`` section parameters to specify values for blueprint parameters.

This can be done by using the blueprint parameter ``id`` as a value when the blueprint is used.

The example below illustrates this:

.. code-block:: xml

   <XDL>
      <Blueprint id='simple_reaction'>
         <Hardware>
            <Component id='reactor' type='reactor'/>
         </Hardware>

         <!-- blueprint parameters -->
         <Parameters>
            <Parameter id='rxn_time' type='time' value='8 h'/>
            <Parameter id='solvent_volume' type='volume'/>
            <Parameter id='rxn_temp' type='temp' value='27°C'/>
         </Parameters>

         <Reagents>
            <Reagent id='solid'/>
         </Reagents>

         <Procedure>
            <Add reagent='solid' vessel='reactor' amount='0.5 g'/>

            <!-- use of parameter values for solvent volume -->
            <Add reagent='solvent' vessel='reactor' volume='solvent_volume'/>

            <!-- use of parameter values for temperature and time -->
            <HeatChill
               vessel='reactor'
               temp='rxn_temp'
               time='rxn_time'
               stir='true'/>

         </Procedure>
      </Blueprint>

      <Synthesis>
         <Hardware>
            <Component id='reactor_1' type='reactor'/>
         </Hardware>

         <!-- parameters -->
         <Parameters>
            <Parameter id='time_1' type='time' value='15 h'/>
         </Parameters>

         <Reagents>
            <Reagent name='example_solid' solid='true' molecular_weight='155.155 g/mol'/>
            <Reagent name='acetonitrile'/>
         </Reagents>

         <Procedure>
            <simple_reaction
               solid='example_solid'
               solvent='acetonitrile'
               reactor='reactor_1'
               rxn_time='time_1'
               solvent_volume='10 mL'
            />
            <!-- parameter 'time_1' is used as a value for blueprint parameter 'rxn_time'-->
         </Procedure>
      </Synthesis>
   </XDL>

In the above example, parameter ``time_1`` is used as a value for the blueprint parameter ``rxn_time``.
The final value for ``rxn_time`` will be "``15 h``".

Deprecated Syntax (param. prefix)
---------------------------------
In previous version of the code, the prefix 'param.' could be used to annotate properties whose values are supplied by a ``Parameter`` object.
This syntax is still supported.

As with above examples, the value for these properties must match the ``id`` of their target ``Parameter`` object. The ``type`` property in the parameter must match the type of attribute that the parameter value is being used for.

For example, to use a parameter which has ``type='volume'`` and an ``id='solvent_volume'`` for the ``volume`` attribute in an ``Add`` Step, with the previous syntax:

.. code-block:: xml

   <Add
      vessel='reactor'
      reagent='solvent'
      param.volume='solvent_volume'
   />
