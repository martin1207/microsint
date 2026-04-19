def dist_est(c_x,c_y):
    
    # Distance estimation
    # Updated model 2023-07-30
    j,i,h,g,f,e,d,c,b,a = -44.03221541, -1.93430694e-03,  2.70958818e-01, -4.34406570e-07, 6.89074662e-06, -4.24327684e-04,  9.75791119e-11,  8.78823755e-11,  -5.62425486e-09,  2.44295321e-07
    cur_dist = j+i*c_x+h*c_y+g*c_x**2+f*c_x*c_y+e*c_y**2+d*c_x**3+c*c_x**2*c_y+b*c_x*c_y**2+a*c_y**3
    
    # If the cur_dist is greater than 10 then the model output is not valid

    if cur_dist < 0 or cur_dist > 10:
        cur_dist = float('inf')
    return cur_dist

def ang_est(c_x,c_y):
    
    # Angle estimation
    # Updated model 2023-07-30
    j,i,h,g,f,e,d,c,b,a = 1.51174613, 9.61013989e-02, -1.24417307e-02, -7.35819553e-05, 2.20966501e-05,  5.45097506e-06,  3.41136461e-08,  1.24628781e-09, -1.55499928e-08,  2.83309812e-09
    cur_angle = j+i*c_x+h*c_y+g*c_x**2+f*c_x*c_y+e*c_y**2+d*c_x**3+c*c_x**2*c_y+b*c_x*c_y**2+a*c_y**3

    # If the angle is not between 0 and 90 then the model output is not valid
    if cur_angle < 0 or cur_angle > 90:
        cur_angle = float('inf')
    return cur_angle

def get_ang_dist(c_x, c_y):
    # Back right quadrant
    if  c_x > 4032:
        c_x = c_x - 4032
        cur_dist = dist_est(c_x, c_y)
        cur_ang = ang_est(c_x, c_y)

        cur_ang = cur_ang + 90

    # Front right quadrant
    elif c_x >= 2668:
        c_x = c_x - 2688
        cur_dist = dist_est(c_x, c_y)
        cur_ang = ang_est(c_x, c_y)

    # Back left quadrant
    elif c_x < 1344:
        c_x = 1344 - c_x
        cur_dist = dist_est(c_x, c_y)
        cur_ang = ang_est(c_x, c_y)

        cur_ang = -1 * ( cur_ang + 90)

    # Front left quadrant
    elif c_x <2668:
        c_x = 2688-c_x
        cur_dist = dist_est(c_x, c_y)
        cur_ang = ang_est(c_x, c_y)

        cur_ang = -1 * cur_ang

# Change this and check if the output is correct:
c_x = 5300
c_y = 1000
cur_dist = dist_est(c_x, c_y)
cur_ang = ang_est(c_x, c_y)

print(f"Distance: {cur_dist}")
print(f"Angle: {cur_ang}")