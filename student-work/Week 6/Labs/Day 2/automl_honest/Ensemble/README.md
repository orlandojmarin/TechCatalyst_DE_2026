# Summary of Ensemble

[<< Go back](../README.md)


## Ensemble structure
| Model                  |   Weight |
|:-----------------------|---------:|
| 2_DecisionTree         |        1 |
| 4_Default_Xgboost      |        4 |
| 6_Default_RandomForest |        1 |

## Metric details
|           |    score |   threshold |
|:----------|---------:|------------:|
| logloss   | 0.528352 |  nan        |
| auc       | 0.758354 |  nan        |
| f1        | 0.846154 |    0.486227 |
| accuracy  | 0.758794 |    0.486227 |
| precision | 0.87     |    0.797015 |
| recall    | 1        |    0.110738 |
| mcc       | 0.392477 |    0.689174 |


## Metric details with threshold from accuracy metric
|           |    score |   threshold |
|:----------|---------:|------------:|
| logloss   | 0.528352 |  nan        |
| auc       | 0.758354 |  nan        |
| f1        | 0.846154 |    0.486227 |
| accuracy  | 0.758794 |    0.486227 |
| precision | 0.767442 |    0.486227 |
| recall    | 0.942857 |    0.486227 |
| mcc       | 0.353274 |    0.486227 |


## Confusion matrix (at threshold=0.486227)
|                 |   Predicted as bad |   Predicted as good |
|:----------------|-------------------:|--------------------:|
| Labeled as bad  |                 19 |                  40 |
| Labeled as good |                  8 |                 132 |

## Learning curves
![Learning curves](learning_curves.png)
## Confusion Matrix

![Confusion Matrix](confusion_matrix.png)


## Normalized Confusion Matrix

![Normalized Confusion Matrix](confusion_matrix_normalized.png)


## ROC Curve

![ROC Curve](roc_curve.png)


## Kolmogorov-Smirnov Statistic

![Kolmogorov-Smirnov Statistic](ks_statistic.png)


## Precision-Recall Curve

![Precision-Recall Curve](precision_recall_curve.png)


## Calibration Curve

![Calibration Curve](calibration_curve_curve.png)


## Cumulative Gains Curve

![Cumulative Gains Curve](cumulative_gains_curve.png)


## Lift Curve

![Lift Curve](lift_curve.png)



[<< Go back](../README.md)
