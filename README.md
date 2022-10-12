# BSVP Crawlers

Crawlers for refrigeration equipment.

- Install requirements with `pip install -r requirements.txt`
- If you want to run a crawler that requires authentication, add your credentials to `config.yaml` (see below for details)
- Run `python crawler.py [OPTIONS]` (list options with `-h` or `--help`); no options will run all crawlers

## Further configurations

You can configure some behavior of the crawlers in the `config.yaml` file.
If it does not exist, the file is automatically created on script start.
If you want add configuration details before first script execution, manually copy or rename the `example.config.yaml` to `config.yaml`.

### Crawlers with authentication

If a crawler needs authentication, please add your regarding `auth_user` and `auth_password` to the `config.yaml`.

### Input CSV

Crawlers can use input CSV files.
They will copy the file and change the regarding properties per line, based on the parsing results.
The `input_csv_path` to the regarding input CSV file and its `input_csv_encoding` and `input_csv_separator` need to be specified in the `config.yaml`.

### Output paths

You can adapt the paths where resulting CSV files are written to in the `config.yaml`.
Please make sure the directories exist.
