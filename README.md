# Betting Predictor

## Overview

**Betting Predictor** is a comprehensive sports betting analysis platform that combines machine learning, statistical analysis, and classic betting strategies to help users make informed betting decisions. The app allows users to upload football match data, simulate various betting strategies, predict match outcomes and odds, and calculate arbitrage and expected value opportunities. The platform features a modern, interactive dashboard built with R Shiny, which communicates with a Python Flask backend for data processing and predictions.

---

## Features

- **Data Upload & Transformation**: Upload your own CSV files of football match data and automatically transform them for analysis.
- **Odds & Outcome Prediction**: Use machine learning models to predict match outcomes, over/under 2.5 goals, and odds for home/away teams.
- **Betting Strategy Simulation**: Simulate and compare classic betting strategies:
  - Martingale
  - Anti-Martingale
  - Fibonacci
  - D'Alembert
  - Oscar's Grind
  - Flat Betting
  - Percentage Betting
- **Arbitrage & Value Calculators**: Instantly calculate arbitrage opportunities, expected value (EV), and expected profit for your bets.
- **Interactive Visualizations**: View bankroll evolution, compare strategies, and analyze results with dynamic plots.
- **Modern Dashboard UI**: Built with R Shiny and shinydashboard for a user-friendly experience.

---

## Tech Stack

- **Backend**: Python, Flask, pandas, numpy, scikit-learn, joblib
- **Frontend**: R, Shiny, shinydashboard, plotly

---

## How It Works

1. **Data Processing**: Upload CSV files containing football match data. The backend processes and cleans the data, engineering features for analysis and prediction.
2. **Prediction**: The backend uses pre-trained machine learning models to predict match outcomes and odds based on the processed data.
3. **Strategy Simulation**: Users can select a team, season, and betting strategy to simulate how their bankroll would evolve over time.
4. **Calculators**: The app provides tools for arbitrage detection, EV calculation, and profit estimation.
5. **Visualization**: Results are displayed in the dashboard with interactive plots and tables.

---

## Usage

### 1. Install Dependencies

**Python Backend:**
```bash
pip install -r requirements.txt
```

**R Frontend:**
Install the following R packages if you don't have them:
```R
install.packages(c("shiny", "shinydashboard", "plotly", "jsonlite", "httr", "readr"))
```

### 2. Run the Backend
```bash
python main.py
```
This will start the Flask server (default: http://127.0.0.1:5000).

### 3. Run the Frontend
Open `R/ui.R` and `R/server.R` in RStudio and click "Run App". The dashboard will open in your browser.

---

## Betting Strategies Supported
- **Martingale**: Double your bet after each loss to recover losses.
- **Anti-Martingale**: Double your bet after each win to ride winning streaks.
- **Fibonacci**: Increase bets following the Fibonacci sequence after losses.
- **D'Alembert**: Increase bets by a fixed unit after a loss and decrease after a win.
- **Oscar's Grind**: A slow progression system increasing bets after a win but keeping them steady after a loss.
- **Flat Betting**: Bet a consistent amount each time.
- **Percentage Betting**: Bet a fixed percentage of your bankroll each time.

---

## API Endpoints

The backend exposes several endpoints for data processing, prediction, simulation, and calculators. See `main.py` for details.

---

## App Showcase

Below are screenshots of the Betting Predictor app in action:

### Dashboard & Features

![Dashboard Overview](images/Screenshot%202025-07-03%20000308.png)
*Main dashboard with navigation for analysis, strategies, and simulation.*

![Odds Prediction](images/Screenshot%202025-07-03%20000404.png)
*Odds prediction interface and results display.*

![Arbitrage Calculator](images/Screenshot%202025-07-03%20000437.png)
*Arbitrage calculator for risk-free betting opportunities.*

![Strategy Input](images/Screenshot%202025-07-03%20000519.png)
*Strategy selection and parameter input.*

![Strategy Results](images/Screenshot%202025-07-03%20000536.png)
*Results of a simulated betting strategy.*

![Compare Strategies](images/Screenshot%202025-07-03%20000603.png)
*Comparison of multiple strategies for a selected team and season.*

![Simulation Settings](images/Screenshot%202025-07-03%20000619.png)
*Simulation settings for match outcome and odds prediction.*

![Simulation Results](images/Screenshot%202025-07-03%20000703.png)
*Simulation results with probability and odds histograms.*

![Data Transformation](images/Screenshot%202025-07-03%20000721.png)
*Data upload and transformation interface.*

---

## License

This project is for educational and research purposes only. Please gamble responsibly. 