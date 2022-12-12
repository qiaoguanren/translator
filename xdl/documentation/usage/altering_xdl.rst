==============
Altering XDL Objects
==============

In theory, you should be able to load a XDL file and run it without any issues.

However, XDL is still in development, so it is wise to inspect everything, make
sure it is what you want, and make adjustments accordingly. If you do make
adjustments, please raise an issue on GitLab so the adjustment can be made
automatically in future.

The XDL procedure is a Python list, containing Step objects. These steps can be
added, removed, or moved in any way. The step list will always execute from start
to finish in order.

Any of the properties in these step objects can be altered, which in turn will change the way these
steps behave internally.

Example
*******

::

    <Synthesis auto_clean="false">

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

Removing a step
^^^^^^^^^^^^^^^

A quick look at the steps and properties shows that there is a :code:`CConnect` step before
the addition step will connect the filter to inert gas. This is unnecessary as the procedure is
only using the reactor, so you may want to remove it.

::

   >>> from xdl import XDL
   >>> x = XDL('procedure.xdl')
   >>> x.prepare_for_execution(x.graph())
   >>> for step in x.steps:
            print(step.name, step.properties, '\n')

   CConnect {'from_vessel': 'flask_nitrogen', 'to_vessel': 'filter', 'from_port': None, 'to_port': 'bottom', 'unique': True}

   Add {'reagent': 'water', 'vessel': 'reactor', 'volume': 10.0, 'mass': None, 'port': 0, 'through': None, 'move_speed': 40, 'aspiration_speed': 10, 'dispense_speed': 40, 'viscous': False, 'time': None, 'stir': False, 'stir_speed': 250, 'anticlogging': False, 'anticlogging_solvent': None, 'anticlogging_solvent_volume': 2, 'anticlogging_reagent_volume': 10, 'anticlogging_solvent_vessel': None, 'reagent_vessel': 'flask_water', 'waste_vessel': 'waste_H', 'flush_tube_vessel': 'flask_nitrogen', 'vessel_type': 'reactor'}

To remove the :code:`CConnect` step simply pop it from the list.

::

    >>> x.steps.pop(0)
    >>> for step in x.steps:
            print(step.name, step.properties, '\n')

   Add {'reagent': 'water', 'vessel': 'reactor', 'volume': 10.0, 'mass': None, 'port': 0, 'through': None, 'move_speed': 40, 'aspiration_speed': 10, 'dispense_speed': 40, 'viscous': False, 'time': None, 'stir': False, 'stir_speed': 250, 'anticlogging': False, 'anticlogging_solvent': None, 'anticlogging_solvent_volume': 2, 'anticlogging_reagent_volume': 10, 'anticlogging_solvent_vessel': None, 'reagent_vessel': 'flask_water', 'waste_vessel': 'waste_H', 'flush_tube_vessel': 'flask_nitrogen', 'vessel_type': 'reactor'}

After doing this, you should create an issue on the XDL GitLab page titled
something like "Unnecessary filter connection to vacuum added when filter not used."

Changing a property
^^^^^^^^^^^^^^^^^^^

For example, imagine you used a graph that contained two reagent flasks containing
water, 'flask_water' and 'flask_water2', and for the :code:`Add` step you want to use 'flask_water2'.

Inspecting the :code:`Add` step shows that the :code:`CMove` substep that actually transfers the
water uses 'flask_water'.

::

    >>> for step in x.steps[0].steps:
            print(step.name, step.properties, '\n')

    StopStir {'vessel': 'reactor', 'vessel_type': 'reactor', 'vessel_has_stirrer': True}

    PrimePumpForAdd {'reagent': 'water', 'volume': 3, 'reagent_vessel': 'flask_water', 'waste_vessel': 'waste_H'}

    CMove {'from_vessel': 'flask_water', 'to_vessel': 'reactor', 'volume': 10.0, 'move_speed': 40, 'aspiration_speed': 10, 'dispense_speed': 40, 'from_port': 0, 'to_port': 0, 'unique': False, 'through': None, 'use_backbone': True}

    Wait {'time': 10, 'wait_recording_speed': 2000, 'after_recording_speed': 14}

    CMove {'from_vessel': 'flask_nitrogen', 'to_vessel': 'reactor', 'volume': 5, 'move_speed': 40, 'aspiration_speed': 10, 'dispense_speed': 40, 'from_port': 0, 'to_port': 0, 'unique': False, 'through': [], 'use_backbone': True}

To use 'flask_water2, you could change directly the 'from_vessel' property of the :code:`CMove` step.

::

    >>> x.steps[0].steps[3].from_vessel = 'flask_water2'

Alternatively, you could change the 'reagent_vessel' property of the parent level :code:`Add` step.

::

    >>> x.steps[0].reagent_vessel = 'flask_water2'

There are two things it is important to note:

1) Any changes made in this way are very likely to be overwritten by a call to
:code:`prepare_for_execution`. Only non-internal properties are safe from :code:`prepare_for_execution` ('reagent_vessel' is an internal property).

2) The change must be made this way :code:`step.property = new_val` for the step to update its step list.
:code:`step.properties[property] = new_val` will not update the step list.
