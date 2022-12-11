# :roffle:
---
A linear model that predicts the likelihood of a message on my Discord channels getting a 😂 or 🤣 reaction.  

The model was trained on data from July of 2021 until now, and spans over 24 thousand messages.  

Repo contents:
- `db`, `models`, `pyscripts`, and `utils` are for programmatic data munging and transferring.
- `eda` contains jupyter notebooks and csv's used during the analyses.
- `.env_template` will have to be filled out for access to programmatic tools, such as fetching data from Discord or saving to an RDS instance.  
- `bds_data` files are there to prevent having to repeatedly ping AWS resources.
- `static` is for a UI that may eventually be created for interacting with the model.