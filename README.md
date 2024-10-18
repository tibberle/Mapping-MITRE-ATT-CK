# Mapping-MITRE-ATT-CK
Reshape the MITRE ATT&amp;CK dataset for Tacts, Technique, and Adversary Group analysis. (Dataset can be found: https://attack.mitre.org/docs/enterprise-attack-v15.1/enterprise-attack-v15.1.xlsx)

## Overview
The Application is a web-based tool designed for displaying and analyzing various techniques used in cybersecurity. This application allows users to filter techniques based on tactics and platforms, visualize data analysis, and view detailed information about individual techniques.

## Version
- **Python - Recommended Versions:** 3.11.9 and/or 3.13.0

---
## Installation Instructions
### Step 1: Prerequisites
Ensure you have Python installed on your system. You can download it from the official [Python website](https://www.python.org/downloads/).
### Step 2: Install Required Packages
pip install dash pandas plotly openpyxl
### Step 3: Run the Application
python app.py
### Step 4: Access the Application
Open web browser and navigate to http://xxx.x.x.x:yyyy/ to access the application.

---
## User Manual and Documentation
This application is designed to provide a comprehensive overview of various cybersecurity techniques. Below is a brief documentation of its features:
- **Interactive Filtering:** Users can filter techniques based on multiple selections for tactics and platforms, enhancing the analysis process.
- **Detailed Exploration:** Each technique has a dedicated page that includes all relevant information, making it easier to understand its context, usages, and the MITRE ATT&amp;CK dataset.
- **Data Visualization:** The application provides visual insights into techniques categorized by platforms with customisation options for tailored data views, and exporting feature; aiding in data analysis and decision-making.

---
### Tools, Technologies, and Methods Used
- **Python**: The primary programming language used for developing the application. Python’s simplicity and readability make it an ideal choice for rapid application development.
- **Dash**: A powerful web application framework for Python, enabling the creation of interactive and dynamic web applications. Dash is built on top of Flask, Plotly, and React.
- **Pandas**: A data manipulation and analysis library for Python, used for handling data structures like DataFrames and performing data preprocessing tasks.
- **Plotly**: A graphing library that enables the creation of interactive visualizations. It is used to generate charts and graphs in the Data Analysis section of the application.
- **OpenPyXL**: A library used to read and write Excel files in Python. It is employed to load the Excel dataset containing techniques information.
- **Excel Files**: The application utilizes Excel files (`enterprise-attack-v15.1 1.xlsx`) as the primary data source for techniques and analysis, providing a structured format for data storage and access.
- **DataFrame Operations**: Data manipulation tasks such as filtering and grouping are performed using Pandas DataFrames, allowing for efficient data processing.
- **HTML/CSS**: The basic building blocks of web development are used to structure and style the application. Bootstrap is incorporated for responsive design and enhanced styling.
- **Bootstrap**: A front-end framework that provides a responsive grid system and various pre-designed components, ensuring a consistent and visually appealing layout.
