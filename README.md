# Základy Datových analýz
This repository contains materials for teaching data analytics concepts, focusing on clustering, regression, and panel data analysis using Python. It is designed to support coursework and practical exercises at ČVUT.

## 📁 Project Structure

```
cvut-zda/
├── data/                # Input datasets (e.g., mall customer data)
├── docs/                # Description of individual excercises
├── notebooks/           # Jupyter notebooks for exploratory and visual analysis
├── src/                 # Python scripts with reusable and modular logic
├── dockerfile           # Dockerfile for environment setup
├── requirements.txt     # Python package dependencies
└── README.md            # Project documentation (this file)
```

## 📊 Main Features

- **Customer Segmentation** using k-means clustering
- **Regression Analysis**: OLS, fixed effects, panel data
- **Silhouette & Elbow Methods** to evaluate clustering quality
- Visualizations with `matplotlib` and `seaborn`
- Dockerized Jupyter environment for reproducibility

## 🚀 Getting Started

The project is designed to run on system interpreter as well as dockerized environment via PyCharm. 


### Requirements

- Docker (for isolated Jupyter environment)
- PyCharm (optional, for managing run configurations)


### Build and Run with Pycharm and Docker

Build docker image from dockerfile as ussual, based on current PyCharm documentation available here: https://www.jetbrains.com/help/pycharm/docker-images.html#build-image
You will need to setup docker image configuration to run jupyter notebooks to make use of the exposed port int he dockerfile. For more information see here: https://www.jetbrains.com/help/pycharm/docker-image-run-configuration.html

#### Pycharm docker build config example:
Use the interpreter options to create a new docker image using the python interpreter window.
This can be added using Project settings -> Python interpreter.

Like this:

![ScreenshotDockerBuild.png](/img/ScreenshotDockerBuild.png)

You need to setup docker build environment in Pycharm, like this:

![ScreenshotDockerBuildDetail.png](/img/ScreenshotDockerBuildDetail.png)

#### Pycharm Run config example:
![ScreenshotDockerJupyterRun.png](/img/ScreenshotDockerJupyterRun.png)

### Build and Run with Docker 

```bash
docker build -t zdapython .
docker run -p 8888:8888 zdapython
```

Then, open the URL shown in the terminal (Jupyter token) in your browser.

### Manual Run

If you prefer to run scripts directly:

```bash
cd src/
python customerSegmentation.py
```

> Ensure the `data/` directory is correctly referenced in your scripts.

## 📂 Data

The main dataset used in the customer segmentation task is:

```
data/data_mall_customers.csv
```

This dataset includes fictional mall customer data with features like:
- Annual income
- Spending score

## 🧪 Notebooks

Notebooks under `/notebooks/` replicate or extend analysis from the Python scripts and can be run inside the Jupyter container.

## 📦 Dependencies

See `requirements.txt` for a list of Python packages. They include:

- `pandas`, `numpy`
- `matplotlib`, `seaborn`
- `scikit-learn`, `statsmodels`
- `linearmodels`, `scipy`
- `jupyter`

## 📌 License

This project is intended for educational purposes. No license or distribution rights are claimed.