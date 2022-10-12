# BSVP Crawlers

Crawlers for refrigeration equipment.

- Install requirements with `pip install -r requirements.txt`
- If you want to run a crawler that requires authentication, add your credentials to `config.yaml` (see below for details)
- Run `python crawler.py [OPTIONS]`; no options will run all crawlers

## Further configurations

You can configure some behavior of the crawlers in the `config.yaml` file.
If it does not exist, the file is automatically created on script start.
If you want add configuration details before first script execution, manually copy or rename the `example.config.yaml` to `config.yaml`.

### Crawlers with authentication

If a crawler needs authentication, please add your regarding `auth_user` and `auth_password` to the `config.yaml`.

### Output paths

You can adapt the paths where resulting CSV files are written to in the `config.yaml`.
