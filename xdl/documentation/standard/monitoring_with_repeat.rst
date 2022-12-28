======================
Monitoring with Repeat
======================

In previous versions of XDL (< XDL 1.0), Repeat could be used to repeat a set of steps 'n' number of times.
In the example below, the Add step would be Repeated 3 times:

.. code-block:: xml

   <Repeat repeats="3">
      <Add reagent="reagent" vessel="reactor"/>
   </Repeat>

The Repeat step can now be executed until a given condition is met, similar to a ``while`` loop.

A 'monitoring' step can be defined with a measurement and corresponding threshold value.
This can be included within a ``<Repeat>`` and the loop body (Repeat substeps) will be executed
until the desired threshold is met.

*Note: this is a beta feature and behaviour is subject to change.*

Creating a Monitoring Step
**************************

All monitoring steps should inherit from ``AbstractMonitorStep``, which requires the following properties to be defined:

- target (str): target vessel to measure.
- quantity (str): Quantity of the reading.
- min (float): Minimum threshold that must be reached to continue.
- max (float): Maximum threshold that should not be exceeded.

The step **must** also return the constant ``DONE`` (found in xdl/constants.py) once the threshold is reached.
To terminate a loop with multiple Monitor steps, all Monitor steps must return ``DONE`` within the same iteration.
A Repeat loop will execute all remaining substeps within that iteration before stopping its execution.

Example Implementation: Monitor
*******************************

A general monitoring step, ``Monitor``, is currently implemented in ChemputerXDL for use with Chemputer platforms.

When a 'target' vessel (e.g ' reactor') and 'quantity' (e.g. 'pH') is defined, ``Monitor`` will find a sensor
connected to the 'target' capable of performing the desired reading.

*Note:* Sensors must be directly connected to the target vessel on the graph.

It will read the sensor until all declared thresholds are met, then return the constant ``DONE``. This will terminate the execution of the ``Repeat``
loop that ``Monitor`` is within.

In the following example, the Add step will be repeated until pH is below 3.

.. code-block:: xml

   <Repeat>
      <Add reagent='acid' vessel='reactor' amount='1 mL'/>
      <Monitor target='reactor' quantity='pH' min='3'/>
   </Repeat>

Supported sensors are those implemented on the Chemputer Platform (defined in Chempiler).
Currently, only 'temperature' and 'pH' are supported measurements, more measurements will be allowed in the upcoming release **XDL1.6**.

*Note:* If more than one suitable sensor is connected, the first one will be chosen and the user will be informed of the final sensor choice.

Example Usage: Monitor
**********************

The following example will add base until the pH is between 5 and 7.

.. code-block:: xml

   <Repeat>
      <Add reagent='base' vessel='reactor' amount='1 mL'/>
      <Monitor target='reactor' quantity='pH' min='5' max='7'/>
   </Repeat>

The example below will add water and then measure the temperature.
If the temperature is below 40 °C, it will add ether and exit the loop.

If the measured temperature is above 40 °C, it will add ether and start the next loop iteration, adding water, and measuring again.
It will continue to execute these three steps until the measurement is below 40 °C (crossing the min limit of 40 °C), at which point it will still add the ether, before exiting the loop and continue with other steps.

.. code-block:: xml

    <Repeat>
        <Add reagent="water" vessel="reactor_1" amount="5 mL"/>
        <Monitor target="reactor" quantity="temperature" min="40 °C" />
        <Add reagent="ether" vessel="reactor" amount="5 mL"/>
    </Repeat>

In the following example, the Transfer step will only be performed after the temperature
in both reactors has fallen below a threshold of 30 °C in reactor_1 and 40 °C in
reactor_2.

.. code-block:: xml

   <Repeat>
      <Monitor target='reactor_1' quantity='temperature' min='30 °C'/>
      <Monitor target='reactor_2' quantity='temperature' min='40 °C'/>
   </Repeat>
   <Transfer from_vessel='reactor_1' to_vessel='reactor_2' volume='all' flush_tubing='True'>
