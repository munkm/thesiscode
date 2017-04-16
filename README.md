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
* method that checks method_type and sends a warning if user-define and found
  method are different. 
* compare runs function to compare mcnp data between angle-methods, standard
  methods, and naive monte carlo runs. 
* make single_run a function in a class that holds the single_run data (for
  easy access in a compare_run method. 
* pass kwargs objects into plotting functions for standardized formatting in
  angle methods, standard methods, and naive monte carlo. 
* fill out logging messages in `analysis.py`, `analysis_utils.py`, and
  `plotting_utils.py`
* add a formatting dict for all methods that is callable from plotting_utils. 
