# Summary of 3_Linear

[<< Go back](../README.md)


## Logistic Regression (Linear)
- **n_jobs**: -1
- **explain_level**: 2

## Validation
 - **validation_type**: split
 - **train_ratio**: 0.75
 - **shuffle**: True
 - **stratify**: True

## Optimized metric
logloss

## Training time

1.9 seconds

## Metric details
|           |    score |   threshold |
|:----------|---------:|------------:|
| logloss   | 0.33325  |  nan        |
| auc       | 0.917918 |  nan        |
| f1        | 0.923077 |    0.391977 |
| accuracy  | 0.889447 |    0.391977 |
| precision | 0.95     |    0.894038 |
| recall    | 1        |    0.015088 |
| mcc       | 0.728979 |    0.391977 |


## Metric details with threshold from accuracy metric
|           |    score |   threshold |
|:----------|---------:|------------:|
| logloss   | 0.33325  |  nan        |
| auc       | 0.917918 |  nan        |
| f1        | 0.923077 |    0.391977 |
| accuracy  | 0.889447 |    0.391977 |
| precision | 0.90411  |    0.391977 |
| recall    | 0.942857 |    0.391977 |
| mcc       | 0.728979 |    0.391977 |


## Confusion matrix (at threshold=0.391977)
|                 |   Predicted as bad |   Predicted as good |
|:----------------|-------------------:|--------------------:|
| Labeled as bad  |                 45 |                  14 |
| Labeled as good |                  8 |                 132 |

## Learning curves
![Learning curves](learning_curves.png)

## Coefficients
| feature                 |    Learner_1 |
|:------------------------|-------------:|
| intercept               |  2.29603     |
| number_credits          |  0.193158    |
| foreign_worker          |  0.183154    |
| property                |  0.180387    |
| telephone               |  0.130535    |
| housing                 |  0.129591    |
| present_residence       |  0.125688    |
| job                     |  0.0888679   |
| other_installment_plans |  0.0449565   |
| age                     |  0.0227112   |
| employment_duration     | -0.000650118 |
| installment_rate        | -0.0160666   |
| amount                  | -0.0226699   |
| people_liable           | -0.0715514   |
| savings                 | -0.136682    |
| credit_history          | -0.180685    |
| other_debtors           | -0.196285    |
| duration                | -0.281214    |
| purpose                 | -0.313096    |
| status                  | -0.353742    |
| id                      | -3.16337     |


## Permutation-based Importance
![Permutation-based Importance](permutation_importance.png)
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



## SHAP Importance
![SHAP Importance](shap_importance.png)

## SHAP Dependence plots

### Dependence (Fold 1)
![SHAP Dependence from Fold 1](learner_fold_0_shap_dependence.png)

## SHAP Decision plots

### Top-10 Worst decisions for class 0 (Fold 1)
![SHAP worst decisions class 0 from Fold 1](learner_fold_0_shap_class_0_worst_decisions.png)
### Top-10 Best decisions for class 0 (Fold 1)
![SHAP best decisions class 0 from Fold 1](learner_fold_0_shap_class_0_best_decisions.png)
### Top-10 Worst decisions for class 1 (Fold 1)
![SHAP worst decisions class 1 from Fold 1](learner_fold_0_shap_class_1_worst_decisions.png)
### Top-10 Best decisions for class 1 (Fold 1)
![SHAP best decisions class 1 from Fold 1](learner_fold_0_shap_class_1_best_decisions.png)

[<< Go back](../README.md)
