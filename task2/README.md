# Classifier Quality Measurement

Goal: calculate classifier quality based on classifier results data file
and on file with right answers data

## Requirements

  - 'numpy' and 'scikit-learn' python packages must be installed
  
## Requirements installation

  - pip install numpy scikit-learn


## Getting help
  
  - python classifier_quality_measurement.py
  - python classifier_quality_measurement.py -h
  - python classifier_quality_measurement.py --help
  
## Launch for one classifier
  
  - python classifier_quality_measurement.py CLASSIFIER1_RESULTS_CSV_FILE  RIGHT_ANSWERS_CSV_FILE
  
## Launch for several classfiers

  - python classifier_quality_measurement.py CLASSIFIER1_RESULTS_CSV_FILE  CLASSIFIER2_RESULTS_CSV_FILE  RIGHT_ANSWERS_CSV_FILE