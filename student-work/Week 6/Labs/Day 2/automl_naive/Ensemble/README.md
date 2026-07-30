# Summary of Ensemble

[<< Go back](../README.md)


## Ensemble structure
| Model                  |   Weight |
|:-----------------------|---------:|
| 2_DecisionTree         |        2 |
| 4_Default_Xgboost      |        3 |
| 6_Default_RandomForest |        1 |

## Metric details
|           |    score |   threshold |
|:----------|---------:|------------:|
| logloss   | 0.195346 | nan         |
| auc       | 0.953511 | nan         |
| f1        | 0.961672 |   0.669805  |
| accuracy  | 0.944724 |   0.669805  |
| precision | 0.964912 |   0.93611   |
| recall    | 1        |   0.0170839 |
| mcc       | 0.866093 |   0.669805  |


## Metric details with threshold from accuracy metric
|           |    score |   threshold |
|:----------|---------:|------------:|
| logloss   | 0.195346 |  nan        |
| auc       | 0.953511 |  nan        |
| f1        | 0.961672 |    0.669805 |
| accuracy  | 0.944724 |    0.669805 |
| precision | 0.938776 |    0.669805 |
| recall    | 0.985714 |    0.669805 |
| mcc       | 0.866093 |    0.669805 |


## Confusion matrix (at threshold=0.669805)
|                 |   Predicted as bad |   Predicted as good |
|:----------------|-------------------:|--------------------:|
| Labeled as bad  |                 50 |                   9 |
| Labeled as good |                  2 |                 138 |

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
