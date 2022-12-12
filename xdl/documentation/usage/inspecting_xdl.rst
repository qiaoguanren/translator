==============
Inspecting XDL Objects
==============

In theory, you should be able to load a XDL file and run it without any issues.

However, XDL is still in development, so it is wise to inspect everything, make
sure it is what you want, and make adjustments accordingly. If you do make
adjustments, please raise an issue on GitLab so the adjustment can be made
automatically in future.

Viewing internal procedure
**************************

Example
-------

.. code-block:: xml

    <Synthesis>

      <Hardware>
        <Component
          id="reactor"
          type="reactor"
        />
      </Hardware>

      <Reagents>
        <Reagent
          id="water" />
      </Reagents>

      <Procedure>
        <Add
          vessel="reactor"
          reagent="water"
          volume="10 mL"
        />
      </Procedure>

    </Synthesis>

The easiest way to see the internal working of this XDL file is by looking at the .xdlexe file produced
during compilation when :code:`xdl_obj.prepare_for_execution(graph)` is called.
These files show a super detailed breakdown of every step in the procedure,
and all the nested steps that make up every step of the procedure. The steps that
will actually be executed are the innermost steps of every nested block, in this example
all the steps with names beginning with the "C" prefix.

Generate .xdlexe
----------------
.. code-block:: Python

    from xdl import XDL
    x = XDL('procedure.xdl')
    x.prepare_for_execution(x.graph())

xdlexe file
-----------
.. code-block:: xml

    <?xdl version="0.2.0" ?>

    <Synthesis
      graph_sha256="7e6677bc110375bad0945052a8f6a6626998fe294823bffbf5d54ddbd7649496"
    >
    <Hardware>
      <Component
        id="reactor"
        type="reactor"
      />
    </Hardware>

    <Reagents>
      <Reagent
        id="water"
      />
    </Reagents>

    <Procedure>
      <CleanBackbone
        solvent="water"
        waste_vessels="waste_Z waste_H waste_G waste_Y waste_K waste_X"
        solvent_vessel="flask_water"
      >
        <CMove
          from_vessel="flask_water"
          to_vessel="waste_Z"
          volume="3 mL"
          move_speed="40"
          aspiration_speed="10"
          dispense_speed="40"
          from_port="0"
          to_port="0"
          unique="False"
          through=""
          use_backbone="True" />
        <CMove
          from_vessel="flask_water"
          to_vessel="waste_H"
          volume="3 mL"
          move_speed="40"
          aspiration_speed="10"
          dispense_speed="40"
          from_port="0"
          to_port="0"
          unique="False"
          through=""
          use_backbone="True" />
        <CMove
          from_vessel="flask_water"
          to_vessel="waste_G"
          volume="3 mL"
          move_speed="40"
          aspiration_speed="10"
          dispense_speed="40"
          from_port="0"
          to_port="0"
          unique="False"
          through=""
          use_backbone="True" />
        <CMove
          from_vessel="flask_water"
          to_vessel="waste_Y"
          volume="3 mL"
          move_speed="40"
          aspiration_speed="10"
          dispense_speed="40"
          from_port="0"
          to_port="0"
          unique="False"
          through=""
          use_backbone="True" />
        <CMove
          from_vessel="flask_water"
          to_vessel="waste_K"
          volume="3 mL"
          move_speed="40"
          aspiration_speed="10"
          dispense_speed="40"
          from_port="0"
          to_port="0"
          unique="False"
          through=""
          use_backbone="True" />
        <CMove
          from_vessel="flask_water"
          to_vessel="waste_X"
          volume="3 mL"
          move_speed="40"
          aspiration_speed="10"
          dispense_speed="40"
          from_port="0"
          to_port="0"
          unique="False"
          through=""
          use_backbone="True" />
      </CleanBackbone>
      <CConnect
        from_vessel="flask_nitrogen"
        to_vessel="filter"
        from_port="None"
        to_port="bottom"
        unique="True" />
      <Add
        reagent="water"
        vessel="reactor"
        volume="10 mL"
        mass="None"
        port="0"
        through="None"
        move_speed="40"
        aspiration_speed="10"
        dispense_speed="40"
        viscous="False"
        time="None"
        stir="False"
        stir_speed="250 RPM"
        anticlogging="False"
        anticlogging_solvent="None"
        anticlogging_solvent_volume="2 mL"
        anticlogging_reagent_volume="10 mL"
        anticlogging_solvent_vessel="None"
        reagent_vessel="flask_water"
        waste_vessel="waste_H"
        flush_tube_vessel="flask_nitrogen"
        vessel_type="reactor">
        <StopStir
          vessel="reactor"
          vessel_type="reactor"
          vessel_has_stirrer="True">
          <CStopStir
          vessel="reactor" />
        </StopStir>
        <PrimePumpForAdd
          reagent="water"
          volume="3 mL"
          reagent_vessel="flask_water"
          waste_vessel="waste_H">
          <CMove
            from_vessel="flask_water"
            to_vessel="waste_H"
            volume="3 mL"
            move_speed="40"
            aspiration_speed="10"
            dispense_speed="40"
            from_port="0"
            to_port="0"
            unique="False"
            through=""
            use_backbone="True" />
        </PrimePumpForAdd>
        <CMove
          from_vessel="flask_water"
          to_vessel="reactor"
          volume="10 mL"
          move_speed="40"
          aspiration_speed="10"
          dispense_speed="40"
          from_port="0"
          to_port="0"
          unique="False"
          through="None"
          use_backbone="True" />
        <Wait
          time="10 secs"
          wait_recording_speed="2000"
          after_recording_speed="14">
          <CSetRecordingSpeed
            recording_speed="2000" />
          <CWait
            time="10 secs" />
          <CSetRecordingSpeed
            recording_speed="14" />
        </Wait>
        <CMove
          from_vessel="flask_nitrogen"
          to_vessel="reactor"
          volume="5 mL"
          move_speed="40"
          aspiration_speed="10"
          dispense_speed="40"
          from_port="0"
          to_port="0"
          unique="False"
          through=""
          use_backbone="True" />
      </Add>
    </Procedure>

    </Synthesis>

Inspecting XDL object in Python
-------------------------------
If this is too much information, there are other ways to look at the contents of
a XDL object in Python.

::

   >>> from xdl import XDL
   >>> x = XDL('procedure.xdlexe')
   >>> for step in x.steps:
            print(step.name, step.properties, '\n')

   CleanBackbone {'solvent': 'water', 'waste_vessels': ['waste_Z', 'waste_H', 'waste_G', 'waste_Y', 'waste_K', 'waste_X'], 'solvent_vessel': 'flask_water'}

   CConnect {'from_vessel': 'flask_nitrogen', 'to_vessel': 'filter', 'from_port': None, 'to_port': 'bottom', 'unique': True}

   Add {'reagent': 'water', 'vessel': 'reactor', 'volume': 10.0, 'mass': None, 'port': 0, 'through': None, 'move_speed': 40, 'aspiration_speed': 10, 'dispense_speed': 40, 'viscous': False, 'time': None, 'stir': False, 'stir_speed': 250, 'anticlogging': False, 'anticlogging_solvent': None, 'anticlogging_solvent_volume': 2, 'anticlogging_reagent_volume': 10, 'anticlogging_solvent_vessel': None, 'reagent_vessel': 'flask_water', 'waste_vessel': 'waste_H', 'flush_tube_vessel': 'flask_nitrogen', 'vessel_type': 'reactor'}

   >>> x.log_human_readable()

   Synthesis Description
   ---------------------

   1) Clean backbone with water.
   2) CConnect
   3) Add water (10 mL) to reactor.
