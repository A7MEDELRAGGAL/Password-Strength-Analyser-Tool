# 🔐 Password Analyser & Cracking Tool

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)
![Flask](https://img.shields.io/badge/Framework-Flask-green?style=flat&logo=flask)
![Security](https://img.shields.io/badge/Security-SHA256-red)

> **University Project** | Department of Information Technology
> **Team:** Ships Group
> **Leader:** Ahmed Mohammed Saad El-Raggal (ID: 2221300)

## 📖 Overview
This project is an educational cybersecurity tool designed to demonstrate the difference between weak and secure authentication mechanisms. It serves two main purposes:
1.  **Defensive Analysis:** Real-time evaluation of password strength (Brute-force resistance).
2.  **Secure Storage Simulation:** Demonstrating how modern databases store passwords using **Salting** and **SHA-256 Hashing**.

## 🚀 Key Features
* **Strength Checker:** Evaluates passwords based on length, numbers, uppercase letters, and symbols.
* **Salting Implementation:** Generates a unique 16-byte random salt for every input to prevent Rainbow Table attacks.
* **SHA-256 Hashing:** Converts the salted password into a secure fixed-size 256-bit string.
* **Dual Interface:** Includes both a Command Line Interface (CLI) and a Web Interface (Flask).

## 🛠️ Project Architecture

![Flowchart](assets/Flowchart.jpg)
*Figure 1: The logic flow from user input to secure storage.*

### The Security Formula Used:
$$FinalHash = SHA256(RandomSalt + UserPassword)$$

## 📂 Repository Structure
```text
├── src/
│   ├── 1_cli_tool.py       # Simple Command Line Tool
│   ├── 2_local_server.py   # Standalone Local Server (No Flask required)
│   └── 3_flask_web_app.py  # Full Web Application (Requires Flask)
├── assets/                 # Project Diagrams & Screenshots
└── README.md               # Documentation
