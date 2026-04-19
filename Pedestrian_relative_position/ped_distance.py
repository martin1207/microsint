import pandas as pd
from joblib import load, dump
import joblib


thredshold_dist=1000

def dist_est(c_x,c_y):
    distance_features, distance_model = joblib.load('/Users/martin.dejaeghere/PhD/Position_Estimation/Pedestrian/distance_predictor_small.joblib')
    image_data =pd.DataFrame([[c_x,c_y]], columns=["x_center","y2"])
    cur_dist = distance_model.predict(distance_features.transform(image_data))[0][0]
    if cur_dist >thredshold_dist:
        distance_features, distance_model = joblib.load('/Users/martin.dejaeghere/PhD/Position_Estimation/Pedestrian/distance_predictor_big.joblib')
        image_data =pd.DataFrame([[c_x,c_y]], columns=["x_center","y2"])

        cur_dist = distance_model.predict(distance_features.transform(image_data))[0][0]
 
    return cur_dist if 0 <= cur_dist <= 2400 else 2400

def ang_est(c_x):
    angle_raw = (c_x / 5376) * 360
    relative_angle = (angle_raw) % 360

    if relative_angle > 180:
        relative_angle -= 360

    return relative_angle




def get_ang_dist_pedestrian(c_x, c_y):
    width = 5376
    segment = width / 8  # 672

    cur_ang = ang_est(c_x)

    if 0 < c_x < segment:
        cur_dist = dist_est(c_x, c_y)
        

    elif segment <= c_x < 2 * segment:
        c_x = c_x - segment
        cur_dist = dist_est(c_x, c_y)
  
    elif 2 * segment <= c_x < 3 * segment:
        c_x = c_x - 2 * segment
        cur_dist = dist_est(c_x, c_y)
 

    elif 3 * segment <= c_x:
        c_x = c_x - 3 * segment
        cur_dist = dist_est(c_x, c_y)


    elif -segment < c_x < 0:
        c_x = -c_x
        cur_dist = dist_est(c_x, c_y)
 
    elif -2 * segment < c_x <= -segment:
        c_x = -c_x - segment
        cur_dist = dist_est(c_x, c_y)
  

    elif -3 * segment < c_x <= -2 * segment:
        c_x = -c_x - 2 * segment
        cur_dist = dist_est(c_x, c_y)
 

    elif c_x <= -3 * segment:
        c_x = -c_x - 3 * segment
        cur_dist = dist_est(c_x, c_y)
     

    else:
        cur_dist = float('inf')
        cur_ang = float('inf')

    return cur_ang, cur_dist
