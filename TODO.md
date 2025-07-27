## What I was doing in this commit


## What is left
- Able to force new values from settings with "f-" key
- In adaptManager if setp< min try to check and if it fails is when `min_time_step_failed` should works instead of `do_last_time_failed`
- Rewrite Space for indexing and for looping returning Partile (make it type hinted)
- Privatize methods
- Add docummentation
- Remove useless features
  - log_history in Adpatability
- Make that store_value in adaptability manager works when is not adaptative
- Split the force_acceleration and force_translation and privatize the other
- Privatize threshold_absolute_value and only return it when do_last_failed is true, if not raise error
- Refactor `check_ok` for returning True or making changes, but not both
- Add to plotting simulation a configuration obtion
- 