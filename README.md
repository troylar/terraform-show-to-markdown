# terraform-report

> This is an alpha project. Excuse the brevity.

## Overview
The goal of this project is to generate an easy-to-read inventory of resources created from terraform.

## Quick Overview
1. From the root of the repo, create a virtualenv
   ```
   python3 -m venv ./venv
   ./venv/bin/activate
   pip install -r ./requirements.txt
   ```

2. Deploy your terraform
3. Run this command to show all of the items in the `tfstate`.
    ```
    terraform show > state.out
    ```
    > You can even combine multiple state output files into a single file if you want to aggregate multiple terraform deploys into a single report. `terraform-report` _should_ remove most of the noise.
    
4. Create the markdown using a `unique_id`, which will be the subfolder for the markdown.
   ```
   python ./main.py ./state.out my_unique_id
   ```

The report will be located in the `report_output/my_unique_id` folder.
