# Shannon-Fano-visualizer
A python app to demonstrate the working principle of Shannon Fano Code 
# Shannon-Fano Coding Visualizer

## Overview
This Python Tkinter application visually demonstrates the Shannon-Fano coding algorithm, a fundamental lossless data compression method. It allows users to input messages, and showcases a step-by-step encoding process including frequency calculation, probability sorting, recursive division, and code assignment. The project features a professional two-panel GUI with interactive binary tree visualization and comprehensive compression statistics.

## Features
- User-friendly, modern GUI with dark/light themed panels  
- Step-by-step visualization of Shannon-Fano encoding  
- Interactive binary tree construction and display  
- Detailed compression statistics, including entropy and efficiency  
- Error-free real-time encoding for messages of varying length  

## Installation
1. Ensure Python 3.6+ is installed with Tkinter support  
2. Download or clone this repository  
3. Run the app:

## How to Use
1. Enter the message in the left panel input box  
2. Click “Generate Codes” to start encoding  
3. View each encoding step in the “Step-by-Step Process” tab  
4. Explore the binary tree in the “Tree Diagram” tab  
5. Check the final encoded output and stats in the “Final Results” tab  

## How Shannon-Fano Works
1. Calculate the frequency and probability of each symbol  
2. Sort symbols by probability in descending order  
3. Split symbols into two groups with near-equal total probability  
4. Assign '0' to upper group and '1' to lower group recursively  
5. Repeat until unique prefix-free binary codes are assigned to all symbols  

## Screenshots  

<img width="1920" height="1020" alt="Screenshot 2025-10-29 195740" src="https://github.com/user-attachments/assets/880f1b4d-789b-4c66-a068-e94c9c922cbb" />


<img width="1920" height="1020" alt="Screenshot 2025-10-29 195757" src="https://github.com/user-attachments/assets/819611ae-1063-4749-8af2-f849da00b2c4" />
<img width="1920" height="1020" alt="Screenshot 2025-10-29 195812" src="https://github.com/user-attachments/assets/cf7c470a-ca7a-49dc-bca0-855045f784cf" />

<img width="1920" height="1020" alt="Screenshot 2025-10-29 195839" src="https://github.com/user-attachments/assets/8bab82e6-54e9-4e4d-967c-f34df7eb91ea" />
<img width="1920" height="1020" alt="Screenshot 2025-10-29 195907" src="https://github.com/user-attachments/assets/fa27a7be-1623-4fa3-b0b1-92ba9f946256" />



## License
This project is licensed under the MIT License.

## Author
Shubham Yadav

---

⭐ Star this repo if you find this project helpful!
