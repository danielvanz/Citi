"""
Copyright 2022 shimst3r and hildeweerts

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0
    
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

sofascore computes the Sepsis-related Organ Failure Assessment (SOFA) score
according to Singer et al.:
    https://doi.org/10.1001%2Fjama.2016.0287
"""

import numpy as np

def compute_sofa(X, time):
    """
    Compute the SOFA scores based on pre-processed data.
    """
    # get values at time
    X = X.loc[:,X.columns.get_level_values('hours_in')==time].copy()
    
    # compute scores
    scores = {
        'cardiovescular' : compute_score_for_cardiovascular_system(X['systolic blood pressure'][time], X['diastolic blood pressure'][time]),
        'coagulation' : compute_score_for_coagulation(X['platelets'][time]), 
        'kidney' : compute_score_for_kidneys(X['creatinine'][time]),
        'liver' : compute_score_for_liver(bilirubin_level=X['bilirubin'][time]),
        'nervous' : compute_score_for_nervous_system(glasgow_coma_scale=X['glascow coma scale total'][time]),
        'respiratory' : compute_score_for_respiratory_system(X['partial pressure of oxygen'][time], X['vent'][time]),
    }
    return scores


def compute_score_for_cardiovascular_system(systolic_blood_pressure, diastolic_blood_pressure):
    """
    Computes lowerbound of the score based on mean arterial pressure.
    """
    mean_arterial_pressure = systolic_blood_pressure + 2 / 3 * diastolic_blood_pressure
    return np.where(mean_arterial_pressure < 70, 1, 0)


def compute_score_for_coagulation(platelets):
    """
    Computes score based on platelets count (unit is number per microliter).
    """
    conditions  = [platelets < 20, platelets < 50, platelets < 100, platelets < 150]
    choices     = [4, 3, 2, 1]
    return np.select(conditions, choices, default=0)


def compute_score_for_kidneys(creatinine_level):
    """Computes score based on Creatinine level (unit is mg/dl)."""
    conditions  = [creatinine_level >= 5.0, creatinine_level >= 3.5, creatinine_level >=2.0, creatinine_level >= 1.2]
    choices     = [4, 3, 2, 1]
    return np.select(conditions, choices, default=0)


def compute_score_for_liver(bilirubin_level):
    """Computes score based on Bilirubin level (unit is mg/dl)."""
    conditions  = [bilirubin_level >= 12.0, bilirubin_level >= 6.0, bilirubin_level >=2.0, bilirubin_level >= 1.2]
    choices     = [4, 3, 2, 1]
    return np.select(conditions, choices, default=0)


def compute_score_for_nervous_system(glasgow_coma_scale):
    """
    Computes score based on Glasgow Coma Scale, see paper by Teasdale et al.:
        https://doi.org/10.1016/S0140-6736(74)91639-0
    """
    conditions  = [glasgow_coma_scale < 6, glasgow_coma_scale < 10, glasgow_coma_scale < 13, glasgow_coma_scale < 15]
    choices     = [4, 3, 2, 1]
    return np.select(conditions, choices, default=0)


def compute_score_for_respiratory_system(partial_pressure_of_oxygen, is_mechanically_ventilated):
    """Computes score based on PaO2 (unit is mmHg)."""
    conditions  = [(partial_pressure_of_oxygen < 100) & (is_mechanically_ventilated==1), 
                   (partial_pressure_of_oxygen < 200) & (is_mechanically_ventilated==1),
                   partial_pressure_of_oxygen < 300, 
                   partial_pressure_of_oxygen < 400
                  ]
    choices     = [4, 3, 2, 1]
    return np.select(conditions, choices, default=0)
