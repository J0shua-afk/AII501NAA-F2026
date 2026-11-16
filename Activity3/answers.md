# Activity 3 – Answers

All numbers come from the saved outputs of `linear_regression_taxi.ipynb` in this folder. Part 5 of the notebook was added for these questions and sets a random seed, so its numbers are repeatable; section 5.6
lists the main ones in one place.

---

## 1. What is the target variable, and what are the input features? Why is this a regression problem rather than a classification problem?

The **target** (label) is `FARE`, the cost of a taxi trip in dollars.

The **input features** of my final model are:

- `TRIP_MILES` – the distance of the trip.
- `TRIP_MINUTES` – the length of the trip in minutes. But this column is not in the dataset, \
 it is `TRIP_SECONDS / 60`, where minutes are used instead of seconds so the two features are on a similar scale.

The notebook's first experiment uses `TRIP_MILES` alone. The working dataframe also keeps `COMPANY`,
`PAYMENT_TYPE` and `TIP_RATE`, but they are only used for exploring the data and are not fed to the model.

It is a `regression` problem because the thing being predicted is a continuous number. A fare can be $7.25 or $31.60 or anything in between, and being off by $1 is better than being off by $10. \
In a classification problem the model picks one of a fixed set of categories (for example cash vs. credit card), and there is no **"close"**: the answer is either the right category or the wrong one.

You can see it in what the model learned (section 5.2), which is an equation that turns the two features
into a dollar amount:

`FARE = 2.03 × TRIP_MILES + 0.15 × TRIP_MINUTES + 3.79`

## 2. Why do we split the data into training and test sets? What would go wrong if we tested on the training data?

The point of the model is to predict fares for trips it has **never seen**. The only way to measure that
is to hold some data back. In section 5.1 I use 80% of the trips (25,355) to train and keep 20% (6,339)
as a test set that the model never sees while learning.

If I tested on the training data, I would be checking the model against the same examples it adjusted its
weights to fit. It shows how well the model fits those particular rows, not how
well it generalises (its being optimistic). A model that had simply memorised its training data would look perfect and then do
badly on real trips, and I would have no way of noticing. It is like marking a student using the exact
practice questions they already saw the answers to.

Google's notebook says the same thing in Part 4: its sample predictions come from the training data, and
it notes that in practice predictions should be made on examples not used in training.

For my model the two numbers are close: the training MAE is $1.13 and the test MAE is $1.18. The test
error is slightly higher, which is normal, and the small gap tells me the model learned the general
pattern instead of memorising rows. I only know that because there is a test set to compare against.

## 3. What does Mean Absolute Error (or MSE) measure? Report your model's value and explain it in plain words.

**Mean Absolute Error** takes every prediction, measures how far it is from the real fare ignoring
whether it was too high or too low, and averages those distances. It is in the same units as the label,
so here it is in dollars.

**Mean Squared Error** squares each error before averaging. Squaring makes large mistakes count much
more than small ones, and the result is in dollars squared, which is harder to read. MSE is the loss the
model actually minimises during training. Its square root, RMSE, brings it back to dollars.

**My model's values on the test set (section 5.2):**

| Metric | Value |
|---|---|
| MSE | $14.7723 |
| RMSE | $3.8435 |
| MAE | $1.1763 |

**In plain words: on average, my model's predicted fare is off by about $1.18.** The average fare in the
test set is $24.54, so that is roughly 5% of a typical fare.


## 4. Look at the predicted vs. actual plot. Where does the model do well, and where does it struggle?

The plot is in section 5.3, with a table of error by fare range and a table of the ten worst predictions
under it.

**Where it does well:** There is a dense band of points sitting right on the dashed "perfect prediction"
line from about $5 up to about $60. These are ordinary metered trips, where the fare really is close to
a rate per mile plus a rate per minute. The table agrees:

| Actual fare | Share of test trips | Mean absolute error |
|---|---|---|
| $0–10 | 32.2% | $0.64 |
| $10–20 | 17.3% | $0.65 |
| $20–40 | 25.8% | $0.99 |
| $40–60 | 22.6% | $1.83 |
| over $60 | 2.1% | $9.11 |

For fares under $40, which is about three quarters of the test set, the model is off by less than $1 on
average. Under $60 it is also not leaning one way: the average error in each range is between −$0.11 and
+$0.29.

**Where it struggles.**

1. **Expensive trips.** Above $60 the points spread out and most of them fall below the line. Those 132
   trips have an MAE of $9.11, and the average error is −$8.52, meaning the model guesses too low.
2. **Trips where the fare does not match the distance and time.** These are the points far below the
   line. Of the 80 test trips that are off by more than $10, 68 were predicted too low and only 12 too
   high. The ten worst predictions are all underestimates of between $52 and $74. One is a 0.90-mile,
   1-minute trip that was charged $59.75 (the model said $5.76). Three are different trips that were all
   charged exactly $83.00, which the model priced at about $18 to $21. These look like flat or
   negotiated fares, or recording mistakes; I cannot tell which from the data. Either way, miles and
   minutes do not explain the fare, so a model that only sees miles and minutes cannot predict it.

So the model is good at ordinary metered trips and poor at the unusual ones, and the unusual ones are
almost always more expensive than it expects.

## 5. Change one setting. What changed in the results, and why do you think it did?

**Setting changed:** the learning rate, from `0.001` to `0.0001` (section 5.4). The features, epochs (20),
batch size (50), training rows and random seed were all kept the same, so the learning rate is the only
difference between the two runs.

**What changed:**

| | Learning rate 0.001 | Learning rate 0.0001 |
|---|---|---|
| Test MAE | $1.18 | $2.35 |
| Test RMSE | $3.84 | $4.57 |
| Test MSE | 14.77 | 20.87 |
| Learned equation | `2.03 × miles + 0.15 × minutes + 3.79` | `1.65 × miles + 0.39 × minutes + 0.83` |

The average error doubled. The loss curves show what happened. With 0.001 the training error drops
quickly and is flat by about epoch 10, so the model has settled. With 0.0001 the curve is still sloping
downward at epoch 20, so training stopped before the model had finished learning.

**Why I think it happened.** The learning rate controls how big a step the model takes each time it
adjusts its weights. With a step ten times smaller and the same 20 epochs, the weights simply do not
travel far enough to reach their best values. The learned equations show it: the intercept only got to
0.83, when the settled model has 3.79, and the other two weights are still a long way from where the
settled model put them.

The smaller learning rate is not wrong, it is just slower. With more epochs I would expect it to end up
at about the same equation, because both runs are heading for the same best fit. Experiment 2a in Part 3
shows the opposite problem: with a learning rate of 1.0 the steps are too big and the loss bounces around
instead of settling.

## 6. Which feature seems most important for the prediction? How did you decide?

**`TRIP_MILES`.** I checked it three ways in section 5.5 so the answer would not depend on one method,
and all three agree.

1. **Correlation with the fare.** 0.98 for `TRIP_MILES` against 0.83 for `TRIP_MINUTES`.
2. **Training with one feature at a time (test MAE).**

   | Features given to the model | Test MAE |
   |---|---|
   | Both | $1.18 |
   | `TRIP_MILES` only | $1.55 |
   | `TRIP_MINUTES` only | $6.73 |
   | Neither (always guess the average) | $14.76 |

   Taking minutes away barely hurts: the error goes from $1.18 to $1.55. Taking miles away makes it go
   from $1.18 to $6.73.
3. **Weight × spread.** The weights on their own (2.03 for miles, 0.15 for minutes) cannot be compared
   directly because they are in different units: dollars per mile and dollars per minute. Multiplying each
   weight by how much that feature typically varies (its standard deviation) fixes that. A typical change
   in miles moves the predicted fare by about $14.70; a typical change in minutes moves it by about
   $2.31, roughly six times less.

Minutes is still worth keeping, since adding it brings the error down from $1.55 to $1.18. That fits how a
taxi meter works, it charges for distance and also for time.

## 7. What is the key difference between classification and regression? Give one real-world example of each from your own life.

**kind of output**. Classification predicts a **category** from a fixed set of
options. Regression predicts a **number** on a continuous scale. That also changes how they are scored:
classification is scored by how often the category is right (accuracy), regression by how far off the
number is (MAE, MSE).


- **Classification:** my email's spam filter, which is also what I built in Activity 1. Every email gets
  one of two labels, spam or not spam.
- **Regression:** at work in procurement, estimating how many pairs of a shoe style will sell next
  season so the right quantity gets ordered. The answer is a number, and being off by 10 pairs is much
  better than being off by 500.

## 8. If you deployed this model in the real world, what could go wrong? Think about bad data, bias, and new situations the model hasn't seen.

**Bad data**

- Assuming the dataset is used exactly as provided. Trips with a wrong distance or time (a meter
  left running, a GPS glitch, a typo) are learned from like any other trip, and MSE gives big outliers
  extra weight, so a few bad rows can pull the line.
- My own results have an example. One of the ten worst test predictions is a 0.90-mile, 1-minute trip
  that was charged $59.75. Either that record is wrong or the fare was not a metered one. The model
  cannot tell which, and it was trained on rows like that too.
- In use, the model trusts whatever miles and minutes it is given. A bad input gives a wrong fare.
- It will happily return a fare for a 0-minute trip or a 500-mile trip. It has no technical limits.

**Bias**

- The data covers only a two-day period in May 2022, in Chicago. It cannot know about winter, holidays,
  big events or anything else that did not happen in those two days.
- Whatever kind of trip is most common in the data dominates training, so a good overall MAE can hide a
  group of riders the model is consistently wrong about. My results show exactly this: trips over $60 are
  only 2.1% of the test set, but their MAE is $9.11 against $1.18 overall, and the model guesses too low
  on them by $8.52 on average.
- Only distance and time are used. Anything else that affects a fare (a flat or negotiated rate, extra
  passengers, how a particular company prices) is invisible to the model, so it will be systematically
  off for trips where those matter.

**New situations**

- **Rules change.** The model has learned something close to Chicago's meter rates as they were in May
  2022. If the city changes its rates, every prediction is wrong in the same direction and nothing in the
  model will flag it.
- **Different place.** Another city has a different base fare and per-mile rate. The weights do not transfer.
- **Outside the range it trained on.** The longest trip in the data is about 68 miles. For anything much
  longer the model just extends the same straight line, with no evidence that fares keep behaving that way.

**What I would do about it:** clean and validate inputs, check error separately for different kinds of
trips instead of trusting one average, keep monitoring error on new trips after deployment, and retrain
when it drifts.
