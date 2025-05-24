# TSACKINGS-NUMBER: Advanced Phone Number OSINT Framework

<p align="center">
  <img src="https://raw.githubusercontent.com/sentinelzxofc/TSACKINGS-NUMBER/logo.png" alt="TSACKINGS-NUMBER Logo" width="150"/> 

<p align="center">
    <a href="https://github.com/sentinelzxofc/TSACKINGS-NUMBER/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License"></a>
    <img src="https://img.shields.io/badge/Python-3.x-blue.svg" alt="Python Version">
    <img src="https://img.shields.io/badge/Platform-Linux%20%7C%20Termux-brightgreen.svg" alt="Platform">
    <img src="https://img.shields.io/badge/Status-Active-success.svg" alt="Status">
    <!-- Add more badges as needed -->
</p>

<p align="center">
    <i>"Unveiling public data, one number at a time. Ethically."</i>
</p>

---

**TSACKINGS-NUMBER** is a powerful, command-line OSINT (Open Source Intelligence) tool meticulously crafted for security researchers, penetration testers, and technology enthusiasts. It specializes in gathering publicly available information linked to phone numbers, operating seamlessly within **Termux (Android, no root needed!)** and standard Linux environments.

This tool leverages the `phonenumbers` library and suggests further investigation paths through generated search engine links, empowering users to explore the digital footprint associated with a phone number using **strictly legal and ethical OSINT methodologies.**

## ✨ Core Features

*   📱 **Comprehensive Analysis:** Extracts key data points:
    *   International/National Formatting
    *   E.164 Standard Format
    *   Country Code & National Number
    *   Geographical Clues (Region/City based on prefix)
    *   Mobile Carrier Information
    *   Associated Time Zone(s)
    *   Number Type (Mobile, Fixed, VoIP, Toll-Free etc.)
    *   Basic Validity & Possibility Checks
*   🌐 **OSINT Search Integration:** Automatically generates direct search links for:
    *   Google
    *   DuckDuckGo
    *   Bing
    *   *(Facilitates deeper manual investigation)*
*   🚀 **Termux Ready:** Optimized for flawless execution on Android via Termux, **without requiring root privileges.**
*   🐧 **Linux Compatible:** Runs smoothly on most Linux distributions.
*   🎨 **Enhanced CLI:** Features a visually appealing interface with color-coded output and a clear, structured display of information.
*   🛡️ **Ethical by Design:** Developed with a strong emphasis on responsible usage, education, and adherence to ethical OSINT principles.
*   ⚙️ **Simple Setup:** Includes a user-friendly, animated installer (`install.sh`) that handles dependencies.
*   🌍 **Multilingual Support:** Core prompts and warnings available in English & Portuguese.

## ⚠️ IMPORTANT: Disclaimer & Ethical Use

**❗ READ CAREFULLY BEFORE USE ❗**

This tool is designed **EXCLUSIVELY** for educational purposes, research, and performing Open Source Intelligence gathering using **data already available in the public domain.**

*   🚫 **NO ILLEGAL USE:** This tool does **NOT** facilitate hacking, unauthorized access, wiretapping, surveillance, or any form of privacy invasion. It does **NOT** access private databases.
*   ⚖️ **YOUR RESPONSIBILITY:** You are **100% responsible** for your actions. Ensure compliance with all local, national, and international laws regarding data privacy, telecommunications, and OSINT activities.
*   💀 **PROHIBITED ACTIONS:** Using this tool for harassment, stalking, doxxing, intimidation, or any malicious/unethical purpose is **STRICTLY FORBIDDEN.**
*   📄 **NO WARRANTY:** Provided "AS IS". The developers assume **ZERO liability** for misuse, damages, or consequences arising from the use or inability to use this software.
*   🎯 **DATA ACCURACY:** Information accuracy depends entirely on public sources and the `phonenumbers` library data, which may be outdated or incomplete.

**By cloning, installing, or using TSACKINGS-NUMBER, you explicitly acknowledge, understand, and agree to these terms. You affirm that you will use this tool legally, ethically, and responsibly.**

Full disclaimers are available in the repository:
*   [English Disclaimer](./DISCLAIMER_EN.md)
*   [Portuguese Disclaimer](./DISCLAIMER_PT.md)

## 🚀 Getting Started: Installation

Setting up is quick and easy:

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/sentinelzxofc/TSACKINGS-NUMBER.git
    ```
2.  **Navigate into the Directory:**
    ```bash
    cd TSACKINGS-NUMBER
    ```
3.  **Grant Execution Permissions:**
    ```bash
    chmod +x install.sh
    ```
4.  **Run the Installer:**
    ```bash
    ./install.sh
    ```
    Follow the on-screen prompts. The installer will:
    *   Display the legal disclaimers (read them!).
    *   Ask for your agreement to proceed.
    *   Detect your system (Termux/Linux).
    *   Install necessary dependencies (Python3, pip, libraries).

## 💻 How to Use

Once installation is complete:

1.  **Launch the tool:**
    ```bash
    python3 main.py
    ```
2.  **Read the Disclaimer (Again!):** Confirm you understand the terms.
3.  **Enter the Target Number:** Provide the phone number in international format (including `+` and country code).
    ```
    [?] Digite o número de telefone (formato +DDIxxxx): +14155552671
    ```
4.  **Analyze Results:** The tool will process the number and display the gathered OSINT data in a structured format, including suggested search links.
5.  **Exit:** Type `exit`, `quit`, `sair`, or `0` and press Enter, or use `Ctrl+C`.

## 🖼️ Conceptual Demo

```
# Imagine a sleek terminal screenshot here showcasing:
# 1. The banner
# 2. The input prompt
# 3. The structured, colorful output with basic info and search links
```

## 📜 License

This project is distributed under the MIT License. See the [LICENSE](./LICENSE) file for more details.

## 👤 Author & Contact

*   **sentinelzxofc**
    *   GitHub: [https://github.com/sentinelzxofc](https://github.com/sentinelzxofc)
    *   Instagram: [@sentinelzxofc](https://instagram.com/sentinelzxofc)

---

*Use your OSINT capabilities wisely and ethically.*

