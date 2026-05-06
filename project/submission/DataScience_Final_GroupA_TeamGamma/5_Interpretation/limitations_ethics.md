# Limitations and Ethics

## Project Limitations
- The user-level sample size is limited, which reduces the ability to generalize results to a wider population.
- SMS parsing relies on pattern matching and may misclassify multilingual or poorly formatted messages.
- The current model is based on behavioral transaction features only; demographic and contextual attributes are not included.
- Class imbalance between activity segments may impact the stability of model performance on new data.

## Ethical Considerations
- Only anonymized identifiers are used; no personally identifiable information is stored in the cleaned dataset.
- The model is intended for user segmentation and engagement planning, not for making high-stakes credit, identity, or fraud decisions.
- Care should be taken to avoid using activity predictions in ways that penalize lower activity users unfairly.

## Responsible Use
- Treat the model output as a signal, not a final decision.
- Validate any operational intervention with additional user research and fairness checks.

## Future Work
- Increase the number of participants and expand data sources to improve model robustness.
- Incorporate demographic and socio-economic features for fairness and deeper segmentation.
- Explore temporal models and sequential analysis for better prediction of behavior changes over time.
