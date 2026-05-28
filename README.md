# Nonlinear Observer for Vehicle Dynamics: Joint Front & Rear Cornering Stiffness Estimation

[![ROS 1 Hydro](https://img.shields.io/badge/ROS-Hydro-blue.svg)](http://wiki.ros.org/hydro)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository hosts a native, standalone **ROS 1 Hydro C++ node** implementing a high-performance **Nonlinear Observer Architecture**. Written entirely in `rospy`, this package executes real-time joint estimation of vehicle states along with unmeasured, time-varying parameters—specifically **front and rear tire cornering stiffnesses** ($C_{\alpha f}$ and $C_{\alpha r}$)—without relying on heavy mathematical prototyping suites.
