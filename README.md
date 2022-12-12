# :roffle:
---
A linear model that predicts the likelihood of a message on my Discord channels getting a 😂 or 🤣 reaction.  

The model was trained on data from July of 2021 until now, and spans over 24 thousand messages.  

Repo contents (directories are denoted with a `/` at the end):
- `report/` contains the contents for the required capstone report.
- `eda/` contains jupyter notebooks and csv's used during the analyses.
- If you want to reproduce the programmatic steps I took, `.env_template` will have to be filled out. However, _none of the programmatic tools are optimized for reproduction_, they were designed merely as a means to an end. 
- `db/` contains classes for file I/O, S3 and Athena interaction, as well as a class for saving data to an AWS RDS instance (not likely to be used).
- `models/` contain Data Access Objects that convert some external data into a useable form. `S3_Image` was set up but has not been used.
- `pyscripts/` and `utils/` both contain ad-hoc functions, notable the Discord fetcher in `pyscripts/`
- `bds_data` files are there to prevent having to repeatedly ping AWS resources.
- `static/` is for a UI that may eventually be created for interacting with the model.