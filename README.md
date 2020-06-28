# Ares OpenData extractor / parser

Simple extractor downloading the CZ ARES registry [opendata dataset](http://wwwinfo.mfcr.cz/ares/ares_opendata.html.cz) . 
The dataset is usually updated once a month.

**CREDITS**: Parser function taken from [kokes/ares_opendata](https://github.com/kokes/ares_opendata) project.

# Functionality

The extractor downloads full ARES dataset from the registry along with list of ICOs that had changed since the last update. 
It fetches the version of dataset that hadn't been downloaded already - it maintains the last state. The list of ICOs may 
be used to understand what had changed since the last download and if that affects your data.
 


# Results

## ARES data

Actual data downloaded in full mode.

- `firmy`
- `fosoby`
- `posoby`

## ICO change set

List of changes created since the last time the dataset was updated. Downloaded in full mode.

- `ico_change_set` [`ICO`, `CHANGE_DT`, `DATASET_UPDATED`]

 
## Development
 
This example contains runnable container with simple unittest. For local testing it is useful to include `data` folder in the root
and use docker-compose commands to run the container or execute tests. 

If required, change local data folder (the `CUSTOM_FOLDER` placeholder) path to your custom path:
```yaml
    volumes:
      - ./:/code
      - ./CUSTOM_FOLDER:/data
```

Clone this repository, init the workspace and run the component with following command:

```
git clone https://bitbucket.org:kds_consulting_team/kbc-python-template.git my-new-component
cd my-new-component
docker-compose build
docker-compose run --rm dev
```

Run the test suite and lint check using this command:

```
docker-compose run --rm test
```

# Integration

For information about deployment and integration with KBC, please refer to the [deployment section of developers documentation](https://developers.keboola.com/extend/component/deployment/) 