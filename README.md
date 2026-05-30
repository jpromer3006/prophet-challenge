# 📈 Forecasting Net Prophet

An interactive web app that explores **MercadoLibre** Google-search-trend
seasonality and forecasts near-term popularity using
[Prophet](https://facebook.github.io/prophet/). Built for a general audience —
every chart comes with a plain-language takeaway.

> ⚠️ Educational demo only. **Not financial advice.**

## What it does

- **🔮 Forecast** – pick a horizon (7–90 days) and see projected search interest with a confidence band.
- **🗓️ Seasonality** – when interest peaks by hour of day, day of week, and week of year.
- **💹 Search vs. stock** – compares search interest to MercadoLibre's stock price and shows that, on its own, search is *not* a reliable predictor of stock moves.

## Run locally

```bash
git clone https://github.com/<your-username>/forecasting-net-prophet-app.git
cd forecasting-net-prophet-app
pip install -r requirements.txt
streamlit run app.py
```

The app loads a pre-trained model from `models/prophet_model.joblib`, so it
starts instantly. To retrain on the cached data:

```bash
python model.py
```

## Deploy to Streamlit Community Cloud (free, public)

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app**, pick this repo, set the main file to `app.py`, and deploy.
4. Every `git push` to the default branch auto-redeploys the live app.

## Project structure

```
.
├── app.py             # Streamlit UI (3 tabs, interactive + plain-language)
├── data_loader.py     # load & clean the cached CSVs
├── analysis.py        # seasonality + correlation (pure functions)
├── model.py           # train / load Prophet, make forecasts
├── data/              # cached source CSVs (committed)
├── models/            # pre-trained Prophet model (committed)
├── notebook/          # original Jupyter analysis this app grew from
├── requirements.txt
└── .streamlit/config.toml
```

## The original analysis

This app started life as the Jupyter notebook in
[`notebook/forecasting_net_prophet.ipynb`](notebook/forecasting_net_prophet.ipynb)
(a Module 8 challenge). The notebook walks through the exploratory analysis —
seasonality mining, search-vs-stock correlation, and the Prophet forecast — that
the web app now packages up for a general audience.

## Credits

Originally adapted from a Jupyter notebook analysis. Data sourced from the edX
AI bootcamp dataset mirror. Forecasting by Prophet; UI by Streamlit; charts by Plotly.
