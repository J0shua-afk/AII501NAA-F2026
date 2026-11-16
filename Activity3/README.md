# Activity 3 – Linear Regression

AII501NAA, Fall 2026. Google Machine Learning Crash Course linear regression exercise: predict the
fare of a Chicago taxi trip from its distance and duration.

## Contents

| File | What it is |
|---|---|
| `linear_regression_taxi.ipynb` | The completed notebook, saved with the outputs of a full run. Parts 1–4 are Google's exercise; Part 5 was added for the Activity 3 questions. |
| `answers.md` | Written answers to the eight questions. |
| `requirements.txt` | Library versions for running the notebook outside Colab. |
| `README.md` | This file. |

## Setup

### Option A – Google Colab (recommended)

1. Go to <https://colab.research.google.com>, choose **File → Upload notebook** and pick
   `linear_regression_taxi.ipynb`.
2. That's it. Colab already has TensorFlow, Keras, NumPy, pandas, matplotlib and Plotly. The first code
   cell installs the one library it is missing (`google-ml-edu`), and the notebook downloads the dataset.

### Option B – Run locally

Tested with Python 3.13.

```bash
cd Activity3
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter notebook linear_regression_taxi.ipynb
```

### Dataset

The notebook downloads the dataset from
`https://download.mlcc.google.com/mledu-datasets/chicago_taxi_train.csv`. To run offline, save that file
as `chicago_taxi_train.csv` in this folder and the notebook will use the local copy instead. The dataset
cell prints which of the two it used.

## Execution

Run every cell from top to bottom (**Runtime → Run all** in Colab, **Run → Run All Cells** in Jupyter).
A full run trains nine small models and takes a few minutes on a CPU.

| Part | What it does |
|---|---|
| 1 – Setup | Installs libraries, loads the dataset. |
| 2 – Dataset exploration | Summary statistics, correlation matrix, pair plot. |
| 3 – Train model | Experiment 1 (one feature), Experiments 2a/2b/2c (hyperparameters – the notebook's TODO), Experiment 3 (two features). |
| 4 – Validate model | Google's sample of 50 predictions. |
| 5 – Activity 3 extension | Train/test split, MAE/MSE on the test set, predicted vs. actual plot, one changed setting, feature importance, summary. |

## Testing

There are no unit tests; the notebook is checked by its own output. After a full run:

1. **Libraries installed** – the install cell lists the version of each library and ends with
   `All requirements successfully installed.` If a library is missing, that cell stops with an error.
2. **No cell shows an error.**
3. **Dataset loaded correctly** – the "View answers about dataset statistics" cell in Part 2 prints a
   maximum fare of $159.25, a mean distance of 8.2895 miles and 31 cab companies.
4. **The split is clean** – cell 5.1 prints 25,355 training rows, 6,339 test rows and `Rows in both sets: 0`.
5. **The model learned something sensible** – cell 5.2 prints the learned equation next to Chicago's
   real fare formula (`FARE = 2.25 * TRIP_MILES + 0.12 * TRIP_MINUTES + 3.25`); the weights should be
   in the same neighbourhood.
6. **The model beats the baseline** – in cell 5.2 the model's test MAE is far below the MAE of always
   guessing the average fare.
7. **Numbers match the write-up** – cell 5.6 prints the headline numbers quoted in `answers.md`; the
   tables in cells 5.3 to 5.5 have the rest.

Tested with Python 3.13 and the library versions Google Colab provides (November 2026): TensorFlow 2.21.0,
Keras 3.13.2, NumPy 2.4.6, pandas 2.2.3, matplotlib 3.10.0, Plotly 5.24.1 and google-ml-edu 0.1.3.

## Assumptions

- **Target and features.** The target is `FARE`. The final model uses `TRIP_MILES` and `TRIP_MINUTES`
  (`TRIP_SECONDS / 60`), the same two features as Google's Experiment 3.
- **Install cell changed.** Google's install cell pins exact versions, including `tensorflow~=2.18.0`.
  Colab now runs Python 3.13, and TensorFlow 2.18 is not available for Python 3.13, so that cell installs
  nothing and the notebook stops at `import ml_edu`. The cell now installs only `google-ml-edu` (and Plotly
  if it is missing) and uses the TensorFlow, Keras, NumPy, pandas and matplotlib that are already there.
  It also checks that every library is present instead of printing a success message regardless.
- **Train/test split.** Google's notebook trains and predicts on the same rows. Part 5 adds an 80/20
  random split with a fixed seed (42) because the questions ask about training vs. test data.
- **Metric.** MAE is the headline metric because it reads directly in dollars; MSE and RMSE are reported too.
- **One changed setting.** The learning rate (0.001 → 0.0001); everything else is held fixed.
- **Reproducibility.** Part 5 sets a random seed before each training run, so the numbers quoted in
  `answers.md` come out the same on every run in the same environment. Parts 1–4 are left as Google wrote
  them and are not seeded, so their numbers change from run to run. The change is large for Experiments 2b
  and 2c, which stop before the model has settled, so where they stop depends on the random starting weights.
- **No data cleaning.** The dataset is used as provided; no rows are removed.
- **Plots on GitHub.** Google's cells draw interactive Plotly charts, which GitHub's notebook viewer
  does not display. The Part 5 plots use matplotlib and do display. Open the notebook in Colab or
  Jupyter to see everything.

## Credits

Parts 1–4 are from Google's Machine Learning Crash Course (`linear_regression_taxi.ipynb`,
Copyright 2023 Google LLC, Apache License 2.0). The original licence cell is kept at the top of the notebook.
