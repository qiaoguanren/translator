Full Steps Specification
========================

Liquid Handling
***************

Add
^^^

Add liquid reagent.

.. csv-table::
   :quote: $
   :header: "Property", "Type", "Description"

   $``vessel``$, $``vessel``$, $Vessel to add reagent to.$
   $``reagent``$, $``reagent``$, $Reagent to add.$
   $``volume``$, $``float``$, $Volume of reagent to add.$
   $``dropwise``$, $``bool``$, $Optional. If ``True``, use dropwise addition speed.$
   $``time``$, $``float``$, $Optional. Time to add reagent over.$
   $``stir``$, $``bool``$, $Optional. If ``True``, stir vessel while adding reagent.$
   $``stir_speed``$, $``float``$, $Optional. Speed in RPM at which to stir at if stir is ``True``.$
   $``viscous``$, $``bool``$, $Optional. If ``True``, adapt process to handle viscous reagent, e.g. use slower addition speeds.$
   $``purpose``$, $``str``$, $Optional. Purpose of addition. If ``None`` assume that simply a reagent is being added. Roles of reagents can be specified in ``<Reagent>`` tag. Possible values: ``\"precipitate\"``, ``\"neutralize\"``, ``\"basify\"``, ``\"acidify\"`` or ``\"dissolve\"``.$


Transfer
^^^^^^^^

Transfer liquid from one vessel to another.

.. csv-table::
   :quote: $
   :header: "Property", "Type", "Description"

   $``from_vessel``$, $``vessel``$, $Vessel to transfer liquid from.$
   $``to_vessel``$, $``vessel``$, $Vessel to transfer liquid to.$
   $``volume``$, $``float``$, $Volume of liquid to transfer from from_vessel to to_vessel.$
   $``time``$, $``float``$, $Optional. Time over which to transfer liquid.$
   $``viscous``$, $``bool``$, $Optional. If ``True``, adapt process to handle viscous liquid, e.g. use slower move speed.$
   $``rinsing_solvent``$, $``reagent``$, $Optional. Solvent to rinse from_vessel with, and transfer rinsings to ``to_vessel``.$
   $``rinsing_volume``$, $``float``$, $Optional. Volume of ``rinsing_solvent`` to rinse ``from_vessel`` with.$
   $``rinsing_repeats``$, $``int``$, $Optional. Number of rinses to perform.$


FilterThrough
^^^^^^^^^^^^^

Filter liquid through solid, for example filtering reaction mixture through celite.

.. csv-table::
   :quote: $
   :header: "Property", "Type", "Description"

   $``from_vessel``$, $``vessel``$, $Vessel containing liquid to be filtered through solid chemical.$
   $``to_vessel``$, $``vessel``$, $Vessel to send liquid to after it has been filtered through the solid chemical.$
   $``through``$, $``reagent``$, $Solid chemical to filter liquid through.$
   $``eluting_solvent``$, $``reagent``$, $Optional. Solvent to elute with.$
   $``eluting_volume``$, $``float``$, $Optional. Volume of eluting_solvent to use.$
   $``eluting_repeats``$, $``int``$, $Optional. Number of elutions to perform.$
   $``residence_time``$, $``float``$, $Optional. Residence time of liquid in cartridge containing solid. If not given, default move speed is used.$




Stirring
********

StartStir
^^^^^^^^^

Start stirring vessel.

.. csv-table::
   :quote: $
   :header: "Property", "Type", "Description"

   $``vessel``$, $``vessel``$, $Vessel to start stirring.$
   $``stir_speed``$, $``float``$, $Optional. Speed in RPM at which to stir at.$
   $``purpose``$, $``str``$, $Optional. Purpose of stirring. Can be None or 'dissolve'. If None, assumed stirring is just to mix reagents.$


StopStir
^^^^^^^^

Stop stirring given vessel.

.. csv-table::
   :quote: $
   :header: "Property", "Type", "Description"

   $``vessel``$, $``vessel``$, $Vessel to stop stirring.$


Stir
^^^^

Stir vessel for given time.

.. csv-table::
   :quote: $
   :header: "Property", "Type", "Description"

   $``vessel``$, $``vessel``$, $Vessel to stir.$
   $``time``$, $``float``$, $Time to stir vessel for.$
   $``stir_speed``$, $``float``$, $Optional. Speed in RPM at which to stir at.$
   $``continue_stirring``$, $``bool``$, $Optional. If ``True``, leave stirring on at end of step. Otherwise stop stirring at end of step.$
   $``purpose``$, $``str``$, $Optional. Purpose of stirring. Can be ``None`` or ``'dissolve'``. If ``None``, assumed stirring is just to mix reagents.$




Temperature Control
*******************

HeatChill
^^^^^^^^^

Heat or chill vessel to given temp for given time.

.. csv-table::
   :quote: $
   :header: "Property", "Type", "Description"

   $``vessel``$, $``vessel``$, $Vessel to heat or chill.$
   $``temp``$, $``float``$, $Temperature to heat or chill vessel to.$
   $``time``$, $``float``$, $Time to heat or chill vessel for.$
   $``stir``$, $``bool``$, $Optional. If True, stir while heating or chilling.$
   $``stir_speed``$, $``float``$, $Optional. Speed in RPM at which to stir at if stir is ``True``.$
   $``purpose``$, $``str``$, $Optional. Purpose of heating/chilling. One of ``\"reaction\"``, ``\"control-exotherm\"``, ``\"unstable-reagent\"``.$


HeatChillToTemp
^^^^^^^^^^^^^^^

Heat or chill vessel to given temperature.

.. csv-table::
   :quote: $
   :header: "Property", "Type", "Description"

   $``vessel``$, $``vessel``$, $Vessel to heat or chill.$
   $``temp``$, $``float``$, $Temperature to heat or chill vessel to.$
   $``active``$, $``bool``$, $Optional. If True, actively heat or chill to temp. If False, allow vessel to warm or cool to temp.$
   $``continue_heatchill``$, $``bool``$, $Optional. If True, leave heating or chilling on after steps finishes. If False, stop heating/chilling at end of step.$
   $``stir``$, $``bool``$, $Optional. If True, stir while heating or chilling.$
   $``stir_speed``$, $``float``$, $Optional. Speed in RPM at which to stir at if stir is True.$
   $``purpose``$, $``str``$, $Optional. Purpose of heating/chilling. One of \"reaction\", \"control-exotherm\", \"unstable-reagent\".$


StartHeatChill
^^^^^^^^^^^^^^

Start heating/chilling vessel.

.. csv-table::
   :quote: $
   :header: "Property", "Type", "Description"

   $``vessel``$, $``vessel``$, $Vessel to start heating/chilling.$
   $``temp``$, $``float``$, $Temperature to heat or chill vessel to.$
   $``purpose``$, $``str``$, $Optional. Purpose of heating/chilling. One of \"reaction\", \"control-exotherm\", \"unstable-reagent\".$


StopHeatChill
^^^^^^^^^^^^^

Heat or chill vessel.

.. csv-table::
   :quote: $
   :header: "Property", "Type", "Description"

   $``vessel``$, $``vessel``$, $Vessel to stop heating/chilling.$


Precipitate
^^^^^^^^^^^

Cause precipitation by optionally adding a reagent, then changing temperature and stirring.

.. csv-table::
   :quote: $
   :header: "Property", "Type", "Description"

   $``vessel``$, $``vessel``$, $Vessel to heat/chill and stir to cause precipitation.$
   $``temp``$, $``float``$, $Optional. Temperature to heat/chill vessel to.$
   $``time``$, $``float``$, $Optional. Time to stir vessel for at given temp.$
   $``stir_speed``$, $``float``$, $Optional. Speed in RPM at which to stir.$
   $``reagent``$, $``str``$, $Optional. Optional reagent to add to trigger precipitation.$
   $``volume``$, $``float``$, $Optional. Volume of reagent to add to trigger precipitation.$
   $``add_time``$, $``float``$, $Optional. Time to add reagent over.$


Crystallize
^^^^^^^^^^^

Crystallize dissolved solid by ramping temperature to given temp over given time.

.. csv-table::
   :quote: $
   :header: "Property", "Type", "Description"

   $``vessel``$, $``vessel``$, $Vessel to crystallize.$
   $``ramp_time``$, $``float``$, $Optional. Time over which to ramp to temp.$
   $``ramp_temp``$, $``float``$, $Optional. Temp to ramp to over time.$


Dissolve
^^^^^^^^

Dissolve solid in solvent.

.. csv-table::
   :quote: $
   :header: "Property", "Type", "Description"

   $``vessel``$, $``vessel``$, $Vessel containing solid to dissolve.$
   $``solvent``$, $``reagent``$, $Solvent to dissolve solid in.$
   $``volume``$, $``float``$, $Volume of solvent to use.$
   $``temp``$, $``float``$, $Optional. Temperature to heat vessel to while dissolving solid.$
   $``time``$, $``float``$, $Optional. Time to stir/heat for in order to dissolve solid.$
   $``stir_speed``$, $``float``$, $Optional. Speed in RPM at which to stir while dissolving solid.$


CleanVessel
^^^^^^^^^^^

Clean vessel.

.. csv-table::
   :quote: $
   :header: "Property", "Type", "Description"

   $``vessel``$, $``vessel``$, $Vessel to clean.$
   $``solvent``$, $``reagent``$, $Solvent to clean vessel with.$
   $``volume``$, $``float``$, $Optional. Volume of solvent to clean vessel with.$
   $``temp``$, $``float``$, $Optional. Temperature to heat vessel to while cleaning.$
   $``repeats``$, $``int``$, $Optional. Number of cleaning cycles to perform.$




Inert Gas
*********

StartPurge
^^^^^^^^^^

Start purging liquid by bubbling gas through it.

.. csv-table::
   :quote: $
   :header: "Property", "Type", "Description"

   $``vessel``$, $``vessel``$, $Vessel containing liquid to purge with gas.$
   $``gas``$, $``str``$, $Optional. Gas to purge vessel with. If not given use any available inert gas.$
   $``pressure``$, $``float``$, $Optional. Optional. Pressure of gas.$
   $``flow_rate``$, $``float``$, $Optional. Optional. Flow rate of gas in mL / min.$


StopPurge
^^^^^^^^^

Stop bubbling gas through vessel.

.. csv-table::
   :quote: $
   :header: "Property", "Type", "Description"

   $``vessel``$, $``vessel``$, $Vessel to stop bubbling gas through.$


Purge
^^^^^

Purge liquid by bubbling gas through it.

.. csv-table::
   :quote: $
   :header: "Property", "Type", "Description"

   $``vessel``$, $``vessel``$, $Vessel containing liquid to purge with gas.$
   $``gas``$, $``str``$, $Optional. Gas to purge vessel with. If not given use any available inert gas.$
   $``time``$, $``float``$, $Optional. Optional. Time to bubble gas through vessel.$
   $``pressure``$, $``float``$, $Optional. Optional. Pressure of gas.$
   $``flow_rate``$, $``float``$, $Optional. Optional. Flow rate of gas in mL / min.$


EvacuateAndRefill
^^^^^^^^^^^^^^^^^

Evacuate vessel and refill with inert gas.

.. csv-table::
   :quote: $
   :header: "Property", "Type", "Description"

   $``vessel``$, $``vessel``$, $Vessel to evacuate and refill.$
   $``gas``$, $``str``$, $Optional. Gas to refill vessel with. If not given use any available inert gas.$
   $``repeats``$, $``int``$, $Optional. Number of evacuation/refill cycles to perform.$




Filtration
**********

Filter
^^^^^^

Filter mixture.

.. csv-table::
   :quote: $
   :header: "Property", "Type", "Description"

   $``vessel``$, $``vessel``$, $Vessel containing mixture to filter.$
   $``filtrate_vessel``$, $``vessel``$, $Optional. Vessel to send filtrate to. If not given, filtrate is sent to waste.$
   $``stir``$, $``bool``$, $Optional. Stir vessel while adding reagent.$
   $``stir_speed``$, $``float``$, $Optional. Speed in RPM at which to stir at if stir is ``True``.$
   $``temp``$, $``float``$, $Optional. Temperature to perform filtration at. Defaults to RT.$
   $``continue_heatchill``$, $``bool``$, $Optional. Only applies if temp is given. If ``True`` continue temperature control after step has finished. Otherwise stop temperature control at end of step.$
   $``volume``$, $``float``$, $Optional. Volume of liquid to withdraw. If not given, volume should be calculated internally in the step.$


WashSolid
^^^^^^^^^

Wash solid with by adding solvent and filtering.

.. csv-table::
   :quote: $
   :header: "Property", "Type", "Description"

   $``vessel``$, $``vessel``$, $Vessel containing solid to wash.$
   $``solvent``$, $``reagent``$, $Solvent to wash solid with.$
   $``volume``$, $``float``$, $Volume of solvent to use.$
   $``filtrate_vessel``$, $``vessel``$, $Optional. Vessel to send filtrate to. If ``None``, filtrate is sent to waste.$
   $``temp``$, $``float``$, $Optional. Temperature to apply to vessel during washing.$
   $``stir``$, $``Union[bool, str]``$, $Optional. If ``True``, start stirring before solvent is added and stop stirring after solvent is removed. If ``'solvent'``, start stirring after solvent is added and stop stirring before solvent is removed. If ``False``, do not stir at all.$
   $``stir_speed``$, $``float``$, $Optional. Speed at which to stir at.$
   $``time``$, $``float``$, $Optional. Time to wait for between adding solvent and removing solvent.$
   $``repeats``$, $``int``$, $Optional. Number of washes to perform.$


Dry
^^^

Dry solid.

.. csv-table::
   :quote: $
   :header: "Property", "Type", "Description"

   $``vessel``$, $``vessel``$, $Vessel containing solid to dry.$
   $``time``$, $``float``$, $Optional. Time to apply vacuum for.$
   $``pressure``$, $``float``$, $Optional. Vacuum pressure to use for drying.$
   $``temp``$, $``float``$, $Optional. Temp to heat vessel to while drying.$
   $``continue_heatchill``$, $``bool``$, $Optional. If True, continue heating after step has finished. If False, stop heating at end of step.$




Other
*****

Separate
^^^^^^^^

Perform separation.

.. csv-table::
   :quote: $
   :header: "Property", "Type", "Description"

   $``purpose``$, $``str``$, $``'wash'`` or ``'extract'``. ``'wash'`` means that product phase will not be the added solvent phase, ``'extract'`` means product phase will be the added solvent phase. If no solvent is added just use ``'extract'``.$
   $``product_phase``$, $``str``$, $``'top'`` or ``'bottom'``. Phase that product will be in.$
   $``from_vessel``$, $``vessel``$, $Contents of ``from_vessel`` are transferred to ``separation_vessel`` and separation is performed.$
   $``separation_vessel``$, $``vessel``$, $Vessel in which separation of phases will be carried out.$
   $``to_vessel``$, $``vessel``$, $Vessel to send product phase to.$
   $``waste_phase_to_vessel``$, $``vessel``$, $Optional. Vessel to send waste phase to.$
   $``solvent``$, $``reagent``$, $Optional. Solvent to add to separation vessel after contents of ``from_vessel`` has been transferred to create two phases.$
   $``solvent_volume``$, $``float``$, $Optional. Volume of solvent to add.$
   $``through``$, $``reagent``$, $Optional. Solid chemical to send product phase through on way to ``to_vessel``, e.g. ``'celite'``.$
   $``repeats``$, $``int``$, $Optional. Number of separations to perform.$
   $``stir_time``$, $``float``$, $Optional. Time stir for after adding solvent, before separation of phases.$
   $``stir_speed``$, $``float``$, $Optional. Speed to stir at after adding solvent, before separation of phases.$
   $``settling_time``$, $``float``$, $Optional. Time to allow phases to settle after stopping stirring, before separation of phases.$


Evaporate
^^^^^^^^^

Evaporate solvent.

.. csv-table::
   :quote: $
   :header: "Property", "Type", "Description"

   $``vessel``$, $``vessel``$, $Vessel to evaporate solvent from.$
   $``pressure``$, $``float``$, $Optional. Vacuum pressure to use for evaporation.$
   $``temp``$, $``float``$, $Optional. Temperature to heat contents of vessel to for evaporation.$
   $``time``$, $``float``$, $Optional. Time to evaporate for.$
   $``stir_speed``$, $``float``$, $Optional. Speed at which to stir mixture during evaporation. If using traditional rotavap, speed in RPM at which to rotate evaporation flask.$


AddSolid
^^^^^^^^

Add solid reagent.

.. csv-table::
   :quote: $
   :header: "Property", "Type", "Description"

   $``vessel``$, $``vessel``$, $Vessel to add reagent to.$
   $``reagent``$, $``reagent``$, $Reagent to add.$
   $``mass``$, $``float``$, $Mass of reagent to add.$
   $``time``$, $``float``$, $Optional. Time to add reagent over.$
   $``portions``$, $``int``$, $Optional. Number of portions to add reagent in.$
   $``stir``$, $``bool``$, $Optional. If ``True``, stir vessel while adding reagent.$
   $``stir_speed``$, $``float``$, $Optional. Speed in RPM at which to stir at if stir is ``True``.$


Irradiate
^^^^^^^^^

Irradiate reaction mixture with light of given wavelength.

.. csv-table::
   :quote: $
   :header: "Property", "Type", "Description"

   $``vessel``$, $``vessel``$, $Vessel to irradiate.$
   $``wavelength``$, $``float``$, $Wavelength of light to irradiate vessel with.$
   $``time``$, $``float``$, $Time to stir vessel for at given temp.$
   $``temp``$, $``float``$, $Optional. Temperature to heat/chill vessel to.$
   $``stir``$, $``bool``$, $Optional. If ``True`` then stir vessel.$
   $``stir_speed``$, $``float``$, $Optional. Speed in RPM at which to stir.$
