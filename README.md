# 🌍 Global Development Insights Chatbot

A conversational AI chatbot that translates natural language questions into SQL queries and retrieves data from a MySQL database on global development indicators. Built using Flask, MySQL, and custom NLP logic.

![Chatbot Preview](https://img.shields.io/badge/Flask-2.x-blue?logo=flask)
![License](https://img.shields.io/badge/license-MIT-green)
![Language](https://img.shields.io/badge/Python-3.11-yellow)

---

## 📂 Project Structure
project/
│
├── app.py
├── devmatric.py
├── datatransformation.py
├── cleaneddata.py
├── templates/
    └── index.html

## ✨ Features

- 🔍 Ask questions like:  
  _"What was the GDP of India in 2021?"_  
  _"Show top 5 countries by life expectancy in 2010."_  
  _"Which countries had birth rate above 50 in 2015?"_

- 🧠 Intelligent Natural Language Parsing
- 🔗 Live SQL Query Generation
- 📊 Real-time Results from MySQL
- 🌐 Clean Web UI with Flask + HTML
- ✅ Supports range filters, comparisons, top/bottom queries, and aggregations

### ✅ Sample Queries
Try the following:

- "What was GDP of India in 2021?"
- "Average life expectancy in Brazil from 2000 to 2020"
- "Top 10 countries by HDI in 2018"
- "Infant mortality above 50 in 2005"

### 📊 Dataset Info
This project uses a global development dataset that includes:

HDI, PHI, GDP, GNI, Education & Health Metrics

Cleaned, normalized, and loaded via MySQL

📁 datacleaning.py and datatransformation.py scripts prepare your data.

### 🔒 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙌 Author
Shubham P.
3rd Year B.Tech (Data Science)
📧 shubham30p@gmail.com

### ⭐️ Star this repo if you find it useful!
---


Visit http://localhost:5000 in your browser.
---






