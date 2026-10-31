import json

notebook_content = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Probabilistic robotics lab: tracking a moving vehicle\n",
    "**Name:** Completed Solution\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "from IPython.display import display\n",
    "\n",
    "SEED = 42\n",
    "plt.rcParams['figure.dpi'] = 110\n",
    "print('Imports OK')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "rng = np.random.default_rng(SEED)\n",
    "dt = 1.0\n",
    "n_steps = 120\n",
    "time = np.arange(n_steps) * dt\n",
    "\n",
    "acceleration = np.zeros(n_steps)\n",
    "acceleration[30:40] = 0.18\n",
    "acceleration[75:85] = -0.12\n",
    "\n",
    "truth = np.zeros((n_steps, 2))\n",
    "truth[0] = [10.0, 1.0]\n",
    "for t in range(1, n_steps):\n",
    "    p, v = truth[t - 1]\n",
    "    a = acceleration[t]\n",
    "    truth[t, 0] = p + v * dt + 0.5 * a * dt**2 + rng.normal(0, 0.2)\n",
    "    truth[t, 1] = v + a * dt + rng.normal(0, 0.1)\n",
    "\n",
    "sensor_sd = 2.0\n",
    "z_position = truth[:, 0] + rng.normal(0, sensor_sd, n_steps)\n",
    "print('Data generation completed.')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "def predict(mu, P, F, Q):\n",
    "    mu_pred = F @ mu\n",
    "    P_pred = F @ P @ F.T + Q\n",
    "    return mu_pred, P_pred\n",
    "\n",
    "def correct_position(mu_pred, P_pred, z, H, R):\n",
    "    nu = z - H @ mu_pred\n",
    "    S = H @ P_pred @ H + R\n",
    "    K = (P_pred @ H) / S\n",
    "    mu = mu_pred + K * nu\n",
    "    P = P_pred - np.outer(K, H @ P_pred)\n",
    "    return mu, P\n",
    "\n",
    "def run_kf(z, F, H, Q, R, mu0, P0):\n",
    "    n = len(z)\n",
    "    means = np.zeros((n, 2))\n",
    "    covariances = np.zeros((n, 2, 2))\n",
    "    means[0] = mu0.copy()\n",
    "    covariances[0] = P0.copy()\n",
    "    for t in range(1, n):\n",
    "        mu_pred, P_pred = predict(means[t - 1], covariances[t - 1], F, Q)\n",
    "        if np.isnan(z[t]):\n",
    "            means[t] = mu_pred\n",
    "            covariances[t] = P_pred\n",
    "        else:\n",
    "            means[t], covariances[t] = correct_position(mu_pred, P_pred, z[t], H, R)\n",
    "    return means, covariances"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "mu0 = np.array([8.0, 0.0])\n",
    "P0 = np.diag([9.0, 1.0])\n",
    "Q_base = np.diag([0.04, 0.01])\n",
    "R_base = sensor_sd**2\n",
    "F = np.array([[1.0, dt], [0.0, 1.0]])\n",
    "H = np.array([1.0, 0.0])\n",
    "\n",
    "def rmse(estimate, actual):\n",
    "    return np.sqrt(np.mean((estimate - actual)**2))\n",
    "\n",
    "kf_means, kf_covariances = run_kf(z_position, F, H, Q_base, R_base, mu0, P0)\n",
    "print('KF position RMSE:', rmse(kf_means[1:, 0], truth[1:, 0]))"
   ]
  }
 ],
 "metadata": {
  "language_info": {"name": "python"}
 },
 "nbformat": 4,
 "nbformat_minor": 2
}

with open("kalman_filter_lab.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook_content, f, indent=2)

print("Fayl 'kalman_filter_lab.ipynb' adı ilə uğurla yaradıldı!")