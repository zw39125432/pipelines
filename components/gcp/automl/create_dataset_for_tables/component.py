# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import NamedTuple


def automl_create_dataset_for_tables(
    gcp_project_id: str,
    gcp_region: str,
    display_name: str,
    description: str = None,
    tables_dataset_metadata: dict = {},
    retry=None, #=google.api_core.gapic_v1.method.DEFAULT,
    timeout: float = None, #=google.api_core.gapic_v1.method.DEFAULT,
    metadata: dict = None,
) -> NamedTuple('Outputs', [('dataset_path', str), ('create_time', str), ('dataset_id', str)]):
    '''automl_create_dataset_for_tables creates an empty Dataset for AutoML tables
    '''
    import sys
    import subprocess
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'google-cloud-automl==0.4.0', '--quiet', '--no-warn-script-location'], env={'PIP_DISABLE_PIP_VERSION_CHECK': '1'}, check=True)

    import google
    from google.cloud import automl
    client = automl.AutoMlClient()

    location_path = client.location_path(gcp_project_id, gcp_region)
    dataset_dict = {
        'display_name': display_name,
        'description': description,
        'tables_dataset_metadata': tables_dataset_metadata,
    }
    dataset = client.create_dataset(
        location_path,
        dataset_dict,
        retry or google.api_core.gapic_v1.method.DEFAULT,
        timeout or google.api_core.gapic_v1.method.DEFAULT,
        metadata,
    )
    print(dataset)
    dataset_id = dataset.name.rsplit('/', 1)[-1]
    return (dataset.name, dataset.create_time, dataset_id)


if __name__ == '__main__':
    import kfp
    kfp.components.func_to_container_op(automl_create_dataset_for_tables, output_component_file='component.yaml', base_image='python:3.7')
