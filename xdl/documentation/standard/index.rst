XDL (the letter X pronounced /ˈkaɪ/ after the Greek 𝛘) is an
executable standard language for programming chemical synthesis,
optimization, and both material and molecular discovery. As a hardware
independent description of chemical operations, XDL can be compiled to
run on a variety of robotic hardware platforms. It can also be
translated to and from human natural language through the *SynthReader*
functionality in
`ChemIDE <https://croningroup.gitlab.io/chemputer/xdlapp/>`__.

================
XDL 2.0 Standard
================

The XDL standard defines the file format and standard steps and parameters
available for defining procedure. It provides a uniform specification that any
platform can adhere to in order to support execution of xdl scripts. Below is a
full declaration of the standard.

.. toctree::
   :maxdepth: 3

   xdl_file_structure
   steps_overview
   full_steps_specification
   using_equivalents
   parameters
   xdl_blueprints
   iteration_with_repeat
   monitoring_with_repeat
   scheduling_with_xdl
