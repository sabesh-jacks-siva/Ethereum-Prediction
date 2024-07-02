#

## ETH Price Prediction

This project predicts Ethereum (ETH) prices using SARIMA, Holt-Winters, and LSTM models. Data fetching, preprocessing, and model training are handled with `yfinance`, `pmdarima`, `holtwinters`, and `keras`. A Gradio interface is included for LSTM predictions.

### Installation

Install dependencies:
```bash
pip install yahoofinancials yfinance pmdarima holtwinters keras gradio
```

### Usage

1. Fetch ETH-USD data and preprocess.
2. Train SARIMA, Holt-Winters, and LSTM models.
3. Evaluate models with RMSE and MAPE.
4. Launch Gradio interface for LSTM predictions.

### Files

- `main.py`: Contains all code for data handling, modeling, and interface setup.
- `README.md`: Project overview and usage instructions.

### Acknowledgements

- Libraries used: `yfinance`, `pmdarima`, `holtwinters`, `keras`, `gradio`.

### Conclusion

LSTM provides accurate ETH price predictions. Gradio interface simplifies model interaction.
