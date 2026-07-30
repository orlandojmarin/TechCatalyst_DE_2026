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

1.7 seconds

## Metric details
|           |    score |   threshold |
|:----------|---------:|------------:|
| logloss   | 0.605927 |  nan        |
| auc       | 0.637409 |  nan        |
| f1        | 0.825959 |    0.184114 |
| accuracy  | 0.713568 |    0.481817 |
| precision | 0.807339 |    0.733216 |
| recall    | 1        |    0.184114 |
| mcc       | 0.289803 |    0.686437 |


## Metric details with threshold from accuracy metric
|           |    score |   threshold |
|:----------|---------:|------------:|
| logloss   | 0.605927 |  nan        |
| auc       | 0.637409 |  nan        |
| f1        | 0.81672  |    0.481817 |
| accuracy  | 0.713568 |    0.481817 |
| precision | 0.74269  |    0.481817 |
| recall    | 0.907143 |    0.481817 |
| mcc       | 0.211964 |    0.481817 |


## Confusion matrix (at threshold=0.481817)
|                 |   Predicted as bad |   Predicted as good |
|:----------------|-------------------:|--------------------:|
| Labeled as bad  |                 15 |                  44 |
| Labeled as good |                 13 |                 127 |

## Learning curves
![Learning curves](learning_curves.png)

## Coefficients
| feature                 |   Learner_1 |
|:------------------------|------------:|
| intercept               |   1.02069   |
| housing                 |   0.306999  |
| foreign_worker          |   0.244774  |
| present_residence       |   0.16124   |
| telephone               |   0.146839  |
| property                |   0.12577   |
| age                     |   0.0639152 |
| other_installment_plans |   0.0372893 |
| number_credits          |   0.0218478 |
| other_debtors           |  -0.0137684 |
| job                     |  -0.0325928 |
| people_liable           |  -0.0617195 |
| installment_rate        |  -0.0917057 |
| employment_duration     |  -0.221173  |
| credit_history          |  -0.23479   |
| amount                  |  -0.307868  |
| savings                 |  -0.314352  |
| purpose                 |  -0.317989  |
| duration                |  -0.32597   |
| status                  |  -0.379761  |


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
