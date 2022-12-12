# :roffle:
---
A linear model that predicts the likelihood of a message on my Discord channels getting a 😂 or 🤣 reaction.  

The model was trained on data from July of 2021 until now, and spans over 24 thousand messages.  

Repo contents:
- `report` contains the contents for the required capstone report.
- `eda` contains jupyter notebooks and csv's used during the analyses.
- If you want to reproduce the programmatic steps I took, `.env_template` will have to be filled out. However, _none of the programmatic tools are optimized for reproduction_, they were designed merely as a means to an end. 
- `db`, `models`, `pyscripts`, and `utils` are for programmatic data munging and transferring.
- `bds_data` files are there to prevent having to repeatedly ping AWS resources.
- `static` is for a UI that may eventually be created for interacting with the model.