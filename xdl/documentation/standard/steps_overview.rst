Steps Overview
==============

Here is an overview of all the steps implemented in this version of the XDL standard.

.. csv-table:: Implemented Steps
   :header: "Liquid Handling","Stirring","Temperature Control","Inert Gas","Filtration","Special","Other"

   "Add","StartStir","HeatChill","EvacuateAndRefill","Filter","Wait","CleanVessel"
   "Separate","Stir","HeatChillToTemp","Purge","FilterThrough","Repeat","Crystallize"
   "Transfer","StopStir","StartHeatChill","StartPurge","WashSolid","","Dissolve"
   "","","StopHeatChill","StopPurge","","","Dry"
   "","","","","","","Evaporate"
   "","","","","","","Irradiate"
   "","","","","","","Precipitate"
   "","","","","","","ResetHandling"
   "","","","","","","RunColumn"
