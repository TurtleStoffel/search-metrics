import os
import sys
import json

from googleapiclient import sample_tools

from most_impactful_pages_by_impressions import MostImpactfulPagesByImpressions
from metrics_per_date import MetricsPerDate
import config

def create_service():
    service, _ = sample_tools.init(
        sys.argv,
        "searchconsole",
        "v1",
        __doc__,
        __file__,
        scope="https://www.googleapis.com/auth/webmasters.readonly",
    )

    return service

def get_index_status(service, url):
    print(f'Getting index status for {url}')
    request = {
        'inspectionUrl': url,
        'siteUrl': 'sc-domain:turtlestoffel.com'
    }
    response = service.urlInspection().index().inspect(
        body=request
    ).execute()

    isIndexed = response['inspectionResult']['indexStatusResult']['verdict'] == 'PASS'

    print(f'Is indexed: {isIndexed}')

    return isIndexed

def write_data(data_file, data):
    with open(data_file, 'w+') as f:
        json.dump(data, f, indent=4, sort_keys=True)

if __name__ == "__main__":
    service = create_service()
    os.chdir(os.path.expanduser(config.ROOT))

    data_file = f'{config.DATA_FOLDER}/data.json'

    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            data = json.load(f)
    else:
        data = {}

    with open(config.SITEMAP_FILE, 'r') as f:
        sitemap = f.readlines()

    for url in sitemap:
        url = url.strip()

        if url not in data:
            data[url] = {
                'isIndexed': get_index_status(service, url)
            }

            write_data(data_file, data)
    
    # MostImpactfulPagesByImpressions(service).calculate()
    # MetricsPerDate(service).calculate()
