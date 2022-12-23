# XDL 2.0 Release Notes

XDL 2.0 comes with several new features, as well as major refactoring to the code base.

## New Features

### Parallel Execution

New to XDL 2.0, steps can be scheduled to run in parallel!
By taking advantage of idle moments during execution, multiple steps can be executed alongside one another.

Note: Steps are actually executed concurrently. This means that multiple steps can be running at the same time
but only one step can be actively controlling hardware at any given moment.

To schedule a step, you must specify the "queue" that the Step belongs to.

```xml
    <Add reagent="reagent_1" vessel="reactor_1" amount="2 mL" queue="A"/>
    <Stir vessel="filter" time="20 mins" queue="B"/>
    <Add reagent="reagent_2" vessel="reactor_2" amount="1 mL" queue="A"/>
```

"queue" defines which steps the current Step is dependent on.

Steps in the same "queue" will run linearly and each Step will depend on the step before it.
Steps in different queues will be run in parallel (where possible).

In the above example, the first Add step and the Stir will start at the same time.
The second Add will wait for the first Add to finish before starting execution.
During the execution of the second Add step, the Stir step will continue to run in the background.

Please see the documentation for more details and examples for parallel execution in XDL: [Parallel Execution with XDL](https://croningroup.gitlab.io/chemputer/xdl/standard/scheduling_with_xdl.html)

### Iteration over reagents and hardware in `Repeat` using multiple clauses

With the XDL1.5 release, iteration over reagents and vessels was made possible.
However, only a single clause could be given for iteration (per loop variable):

```xml
<!-- Add all liquid reagents to fixed reactor -->
<Repeat my_reagent.solid="False">
    <Add reagent="my_reagent" vessel="reactor"/>
</Repeat>
```

The identifier `my_reagent` above is called a _loop variable_, constructed using the general syntax `<variable name>.<attribute> = <value>`, _e.g._ `my_vessel.type = "reactor"` matches all reactors.

It is now possible to specify multiple specification clauses for the same loop variable (similar behavior to conditional 'and'):

```xml
<!-- Add all liquid reagents, which have the role of solvent to fixed reactor -->
<Repeat my_reagent.solid="False" my_reagent.role="solvent">
    <Add reagent="my_reagent" vessel="reactor"/>
</Repeat>
```

## User Information

### Blueprints

Blueprints are now descendants of AbstractStep and are stored alongside other steps in the XDL object (in XDL.steps).

### Platform Controller Locks

The platform controller used to execute steps (e.g. Chempiler), now has a lock.

- By default, XDL waits for the platform controller lock to be released before executing the procedure (`lock_controller=True` by default).
- This behavior can be changed by using the 'lock_controller' argument during execution.

```python
x = XDL(xdl_file, platform=ChemputerPlatform)
x.prepare_for_execution(graph_file)

x.execute(platform_controller, lock_controller=False)
```

`lock_controller=False` means that XDL will not wait for the platform controller to be free before executing the procedure.

- This opens up the possibility to execute multiple XDL objects using the same platform controller.
- Use cautiously!!

### Using Jupyter Notebooks

It is now possible to run code in new cells whilst your XDL is executing (the running of code is no longer delayed until execution is finished).

However, the platform_controller lock (and default behavior of `lock_controller=True`) detailed above means that your platform controller will be locked by default.

This means you can still queue up running multiple XDLs in your notebook and not worry about them overlapping.

## Developer Information

### Implementation of Parallel Execution

XDL now uses the package Asyncio to schedule step execution.

A task is created from each step in the XDL procedure.

Before executing the step, dependencies need to be met (acquire all hardware locks necessary and wait for any step dependencies to finish).
Therefore care should be taken when creating new AbstractBase steps, to ensure that all required locks are specified in the lock function.

AbstractBaseSteps are now required to be coroutines during execution and need to be awaited to execute.
This means that their `execute` functions must now be async.

For example, for Wait:

```python
# previous code:
def execute(
    self, platform_controller: Any, logger: logging.Logger = None, level: int = 0
) -> bool:
    time.sleep(self.time)
    return True


# new code:
async def execute(
    self, platform_controller: Any, logger: logging.Logger = None, level: int = 0
) -> bool:
    await asyncio.sleep(self.time)
    return True
```

Also, as seen above, instances of `time.sleep` have been replaced with `asyncio.sleep` in Wait and similar steps.
`time.sleep` is blocking and does not allow asyncio to take advantage of the idle time whilst waiting.

As `asyncio.sleep` is also a coroutine, it's execution must be awaited (`await asyncio.sleep(self.time)`).

### Other Changes to Code Base

- Step logging has been unified. Special logging is no longer required for each step with children.
  - All logging is added in execute_step functions.
- XDLStepsList has been removed (previously in xdl.py).
- There is now only one list of locks instead of three (any Step lock function should return a single list of lock ids (str)).
- Major refactoring of Blueprint code.
  - Blueprints instantiated alongside other steps (previously were resolved during prepare for execution).
- Major refactoring of Repeat code.
- Linting / formatting: configured pre-commit with some sensible hooks.
  - Black (formatter)
  - isort (formatter)
  - Prettier (formatter)
  - Flake8 (linter)
  - Bandit (security auditing)
  - Validators for several file types (including config files)

## Known issues
