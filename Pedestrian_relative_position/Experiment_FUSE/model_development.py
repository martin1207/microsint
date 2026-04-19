from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from tqdm import tqdm

# # Values from the training pictures
horizontal_values = pd.DataFrame(data={'horizontal': [1391, 1360, 1367, 1370, 1373, 1372, 1379, 991, 980, 988, 978, 964, 968, 966, 658, 689, 685, 692, 691, 685, 682, 438, 430, 412, 421, 417, 420, 407, 19, 38, 34, 25, 19, 25, 18]})
vertical_values = pd.DataFrame(data={'vertical': [379, 671, 850, 956, 1033, 1082, 1128, 362, 663, 845, 954, 1028, 1086, 1117, 368, 668, 857, 962, 1031, 1080, 1119, 358, 667, 845, 955, 1025, 1076, 1113, 364, 671, 841, 944, 1021, 1076, 1121]})
angle_values = pd.DataFrame(data={'angle': [90, 90, 90, 90, 90, 90, 90, 60, 60, 60, 60, 60, 60, 60, 45, 45, 45, 45, 45, 45, 45, 30, 30, 30, 30, 30, 30, 30, 0, 0, 0, 0, 0, 0, 0]})
distance_values = pd.DataFrame(data={'distance': [10, 20, 30, 40, 50, 60, 70, 10, 20, 30, 40, 50, 60, 70, 10, 20, 30, 40, 50, 60, 70, 10, 20, 30, 40, 50, 60, 70, 10, 20, 30, 40, 50, 60, 70]})

# Calculate the lidar_x and lidar_y from the distance and angle
x_values = distance_values["distance"]*np.sin(np.deg2rad(angle_values["angle"]))
y_values = distance_values["distance"]*np.cos(np.deg2rad(angle_values["angle"]))

# Values from a test picture
horizontal_test_values = pd.DataFrame(data={'horizontal': [1129, 1140, 1148, 792, 809, 831, 529, 558, 551, 200, 212, 212]})
vertical_test_values = pd.DataFrame(data={'vertical': [527, 913, 1013, 532, 905, 999, 527, 903, 996, 529, 895, 994]})
angle_test_values = pd.DataFrame(data={'angle': [75, 75, 75, 53, 53, 53, 38, 38, 38, 15, 15, 15]})
distance_test_values = pd.DataFrame(data={'distance': [15, 35, 45, 15, 35, 45, 15, 35, 45, 15, 35, 45]})

# Calculate the lidar_x and lidar_y from the distance and angle
x_test_values = distance_test_values["distance"]*np.sin(np.deg2rad(angle_test_values["angle"]))
y_test_values = distance_test_values["distance"]*np.cos(np.deg2rad(angle_test_values["angle"]))

# Concatination of array to form. (Independent variables of the equation)
calibration_values = pd.concat([horizontal_values,vertical_values], axis=1)
calibration_test_values = pd.concat([horizontal_test_values,vertical_test_values], axis=1)


# Root mean square values for checking which order is the best fit
Rsqu_ang_test = []
Rsqu_dist_test = []
mean_squared_error_dist = []
mean_squared_error_ang = []

# create an array with order 1 to 5 initially
# The order having the highest score will provide the best fit
# https://en.wikipedia.org/wiki/Coefficient_of_determination

order = [2,3,4,5,6]
for n in tqdm(order):
    
    # converting each of the point to fit the order n equation
    pr = PolynomialFeatures(degree=n)

    x_train_pr = pr.fit_transform(calibration_values)
    x_test_pr = pr.fit_transform(calibration_test_values)

    # Fitting the polynomial equation for the angles
    poly_ang = LinearRegression()
    poly_ang.fit(x_train_pr, angle_values)
    
    # Fitting the polynomial equation for the distance
    poly_dist = LinearRegression()
    poly_dist.fit(x_train_pr, distance_values)

    # Calculating the performance of the model and appending to the list
    Rsqu_ang_test.append(poly_ang.score(x_test_pr, angle_test_values))
    Rsqu_dist_test.append(poly_dist.score(x_test_pr, distance_test_values))

    # Calculating the mean squared error and appending to the list
    mean_squared_error_dist.append(mean_squared_error(distance_test_values, poly_dist.predict(x_test_pr)))
    mean_squared_error_ang.append(mean_squared_error(angle_test_values, poly_ang.predict(x_test_pr)))
    if n == 3:
        for ind, ang_pred in enumerate(poly_ang.predict(x_test_pr)):
            print(ang_pred, angle_test_values.values[ind][0])


# Plotting the mean squared error for the distance
plt.plot(order, mean_squared_error_dist)
plt.xlabel('order')
plt.ylabel('MSE')
plt.title('MSE for distance')
plt.show()

# Plotting the mean squared error for the angle
plt.plot(order, mean_squared_error_ang)
plt.xlabel('order')
plt.ylabel('MSE')
plt.title('MSE for angle')
plt.show()

# Plotting the R^2 for the distance
plt.plot(order, Rsqu_dist_test)
plt.xlabel('order')
plt.ylabel('R^2')
plt.title('R^2 for distance')
plt.show()

# Plotting the R^2 for the angle
plt.plot(order, Rsqu_ang_test)
plt.xlabel('order')
plt.ylabel('R^2')
plt.title('R^2 for angle')
plt.show()

print(mean_squared_error_dist)
print(mean_squared_error_ang)
print(Rsqu_dist_test)
print(Rsqu_ang_test)
print("Co-effecient for angle: ", poly_ang.coef_)
print("Intercept of the angle: ", poly_ang.intercept_)
print('-'*55)
print("Co-effecient for distance: ", poly_dist.coef_)
print("Intercept of the distance: ", poly_dist.intercept_)