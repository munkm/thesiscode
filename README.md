# Thesis Code
This is where the scripts and code relevant to my thesis data generation,
acquisition, and processing resides. 

My dissertation repository that houses the content of my dissertation and
relevant .tex files is located here: https://github.com/munkm/dissertation

My other code that is publicly accessible is available on my [github user
profile page](munkm.github.io).


Features to add in `scripts`:
* reading function in run function to check for existence of pickle and .json
  file that holds previously processed data. 
* Modify logging messages to proper level. 
* add a `setup.py` file to make analysis a standalone package that can be
  built. 
* fix plotting functions so they can be used without screen. 
* Comment in more of code.
* Add docstrings for all functions and classes
* Modify `MCNPOutput` class in `analysis.py` to take the tally number in
  `get_tally_data` so multiple tallies can be read in under the same MCNPOutput
  object.
* Modify H5Output functions to be more flexible. Merge get_dataset_by_metric
  and get_dataset_by_energy into a single function that can read either or. 
* Build in handler in compare_runs so cadis and cadisangle-only can be
  compared. 


Recently added features:
* ~~method that checks method_type and sends a warning if user-define and found
  method are different.~~ 
* ~~compare runs function to compare mcnp data between angle-methods, standard
  methods, and naive monte carlo runs.~~ 
* ~~make single_run a function in a class that holds the single_run data (for
  easy access in a compare_run method.~~ 
* ~~pass kwargs objects into plotting functions for standardized formatting in
  angle methods, standard methods, and naive monte carlo.~~ 
* ~~fill out logging messages in `analysis.py`, `analysis_utils.py`, and
  `plotting_utils.py`~~
* ~~add a formatting dict for all methods that is callable from plotting_utils.~~ 

