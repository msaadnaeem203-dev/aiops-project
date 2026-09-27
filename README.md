# AIOPS Monitoring and Health Dashboard

## Overview

This project is an Artificial Intelligence for IT Operations (AIOps) monitoring system built with Python.

It monitors system health, detects anomalies, classifies alerts, and displays the results through a Flask web dashboard.

## Features

- System CPU monitoring
- RAM monitoring
- Website health checking
- Anomaly detection
- Alert logging
- Alert severity classification
- Health summary
- Flask web dashboard
- Automatic dashboard refresh

## Alert Severity

- INFO - normal system activity
- WARNING - elevated system usage
- CRITICAL - very high system usage

## Project Files

- 'monitor.py' - system monitoring
- 'anomaly_detector.py' - anomaly detection
- 'alert_classifier.py' - alert severity classification
- 'health_summary.py' - overall health summary
' 'dashboard.py' - Flask dashboard
- 'alerts.log' - recorded alerts
- 'requirements.txt' - Python dependencies

## Technologies

- Python
- Flask
- psutil
- Linux / Ubuntu
- Git and GitHub

## Dashboard

The dashboard displays:

- System status
- CPU usage
- RAM usage
- Website status
- Total alerts
- Alert severity counts
- Alert classification

## Project Status

The monitoring pipeline and web dashboard are working successfully.
