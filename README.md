# Browser Fingerprinting Demo

## Overview
This GitHub repository contains the source code for a Browser Fingerprinting Demo. The project demonstrates how various browser attributes can be collected and used to generate a unique fingerprint of a user's browser. 

The aim is to use Machine Learning on the data collected by this algorithm to provide no more than 80% accuracy in the fingerprint, hence "Pseudo" fingerprinting.

## Features
- Collects a wide range of browser attributes using JavaScript.
- Includes a demo HTML page with a simple and clean UI to display the collected data.
- Utilises `FingerprintJS` for enhanced fingerprinting capabilities.
- Implements additional custom fingerprinting techniques.
- Generates a pseudo fingerprint hash using MD5 for uniqueness representation.
- (SoonTM): Machine Learning Code and stuff

## How It Works
The application collects information like user agent, language, platform, screen details, timezone, storage capabilities, and many other browser-specific data points. This data is then displayed on a webpage and can also be sent to a server for further analysis.

## Installation

1. **Clone the Repository**
   ```bash
   git clone git@github.com:babyygemperor/Pseudo-Fingerprinting.git
   ```
2. **Open the HTML File**
   - Simply open the `templates/index.html` file in any modern web browser.

## Usage
Once the HTML page is loaded, it automatically starts collecting data about the browser. The collected data is displayed in a grid format on the page. You can view the raw data sent to the server in the browser's console.

## Contributing
Contributions to this project are welcome. Please ensure that your code adheres to the existing style and that all tests pass.

## Note
Browser fingerprinting can have privacy implications. This demo is for educational purposes and should be used responsibly.

---

This README provides a basic template. You might need to adjust it according to your project's specific requirements and add additional sections like 'API Documentation', 'Known Issues', or 'Roadmap', depending on the complexity and scope of your project.