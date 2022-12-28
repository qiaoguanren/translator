===========================
Parallel Execution of Steps
===========================

New to XDL 2.0, steps can be scheduled to run in parallel.
By taking advantage of idle moments during execution, multiple steps can be executed alongside one another.

Note: A state machine is used instead of multiple threads to ensure safe hardware access and to facilitate debugging.
This means that multiple steps can be running at the same time
but only one step can be actively controlling hardware at any given moment.

Scheduling Syntax
*****************

To schedule a step, you must specify the "queue" that the Step belongs to.

.. code-block:: xml

    <Add reagent="reagent_1" vessel="reactor_1" amount="2 mL" queue="A"/>
    <Stir vessel="filter" time="20 mins" queue="B"/>
    <Add reagent="reagent_2" vessel="reactor_2" amount="1 mL" queue="A"/>

"queue" defines which steps the current Step is dependent on. Steps in the same "queue" will run linearly
and each Step will depend on the step before it.
Steps in different queues will be run in parallel (where possible).

In the above example, the first Add step and the Stir will start at the same time.
The second Add will wait for the first Add to finish before starting execution.
During the execution of the second Add step, the Stir step will continue to run in the background.

If no queue is specified, the step will be dependent on the step directly before it.
This means that the default behavior will remain as linear execution of steps.

Rules of Scheduling
*******************

* Each step has a set of hardware locks that must be available before they can start.

   * During execution, the step will "acquire" these locks and make them unavailable for other steps to use.
   * This prevents multiple steps trying to control the same hardware at the same time.

* Steps in the same queue will run sequentially.

   * Each step is dependent on the step before it.
   * This means that the previous step must finish execution before it can begin.

* Steps in different queues can start at the same time.

   * If steps in different queues require the same locks and are scheduled to start at the same time, either could start first.
   * One step will grab the locks first and the other will have to wait for the locks to be released before it can start.

* If no queue is specified for a given step, it will be assigned to the 'root' queue.

   * Such steps will be dependent on the steps directly before them, independent of their queue.
   * All queues that succeed a root step will wait for the root step to execute, even if they have a "queue".
   * This means that if no queues are specified for any steps, previous behavior of linear execution of steps will be maintained.

* Blueprints and Repeat steps have their own namespace.

   * The parent step (Blueprint or Repeat) can be scheduled the same as other steps.
   * However, their children (substeps) will have local dependencies (only depend on other steps within the same step).
   * In the example below, the Add (queue A) and Transfer (queue B) within Repeat only take each other into account when scheduling execution.

      * The queue "A" of the child Add step and the parent Repeat step's queue "A" are in fact different queues.
      * Repeat is only dependent on the addition of reagent_1 (previous Add step).
      * The Transfer within Repeat is only dependent on the Stir before it, not the first Add (of reagent_1) in the Procedure.

.. code-block:: xml

    <Add reagent="reagent_1" vessel="reactor_1" queue="A"/>

    <Repeat repeats="2" queue="A">
      <Add vessel="reactor" reagent="water" volume="20 mL" queue="B"/>
      <Stir vessel="filter" time="5 mins" queue="A"/>
      <Transfer from_vessel="reactor" to_vessel="separator" volume="all" queue="A"/>
    </Repeat>

Examples
********

Example 1
---------
No queues are specified, steps will be assigned to the 'root' queue and will run sequentially.

.. raw:: html
    :file: example_1.svg

Example 2
---------

* Add (queue A) and Stir (queue B) begin execution at the same time.
* Stir (queue A) is dependent on Add (queue A) so it must wait for the Add to complete before starting execution.
* Add (queue A) will finish first and Stir (queue A) will start whilst Stir (queue B) continues in the background.
* Stir (queue A) will finish, followed by Stir (queue B).

.. raw:: html
    :file: example_2.svg

Example 3
---------
* A step without a queue is assigned to the 'root' queue.
* If a 'root' queue Step occurs mid-procedure, any step that follows will be dependent on the root queue step, even if it is in a separate queue.
* The following Adds will occur sequentially.
* Even though the second and fourth Add's are in separate queues (and could theoretically be executed in parallel), they must wait for the 'root' queue Add's to finish before them.

.. raw:: html
    :file: example_3.svg

Example 4
---------
Two reactions (Ugi_Blueprint) and their workups (Workup_Blueprint) can be scheduled to run in parallel.

.. raw:: html
    :file: example_4.svg

Example 5
---------

* Repeats and (Blueprints) have their own namespace (local queues) for their children.
* In the example below, an iterative Repeat step (see :doc:`/standard/iteration_with_repeat`) is used to iterate through hardware of type 'reactor' and reagents with role 'substrate'.
* For each pair of matches, the Repeat child steps (Rxn_BP, Stir, Workup_BP) will be executed.
* The Stir step (queue B) outside of the Repeat is carried out in parallel to the Repeat step (queue A).

   * The Stir step is outside of the scope of the Repeat children.
   * Repeat child steps in "queue B" will not depend on the Stir.

* As all iterations have the same parent step (Repeat), we need to have a blocking 'root' queue step (Wait for 2 s) to make sure steps from different iterations are not executed in parallel.
* In the example below, steps of a single iteration are executed before the next iteration begins.
* Without the Wait (root queue), all Stir steps would occur directly after one another.

.. raw:: html
    :file: example_5.svg
