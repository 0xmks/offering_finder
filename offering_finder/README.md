# offering_finder

## Overview
`offering_finder` is a tool to search for AWS RDS reserved instance offerings and retrieve offering IDs based on specified parameters.

## Features
- Search for RDS reserved instance offerings based on specified parameters
- Output search results in JSON format
- Generate AWS CLI commands to purchase reserved DB instance offerings

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/offering_finder.git
    cd offering_finder
    ```

2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## AWS Profile Setup

Before using the commands, ensure that you have set an accessible AWS account profile with read permissions. This is necessary for the commands to function correctly. You can set the AWS profile by using the following command.

```sh
export AWS_PROFILE=youre_readonly_permission_profile
```

## Usage

1. Run `cli.py` to retrieve offering IDs based on the specified parameters:
    ```bash
    python src/offering_finder/cli.py --product_description MySQL --db_instance_class db.m5.large --duration 31536000 --quantity 2 --region_name ap-northeast-1 --multi_az --offering_type "All Upfront" --reserved_instance_id "test-reserved-instance-id" | jq .
    ```

2. You can modify the parameters in the command to search for different offerings:
    ```bash
    python src/offering_finder/cli.py --product_description PostgreSQL --db_instance_class db.r5.large --duration 94608000 --quantity 1 --region_name us-west-2 --offering_type "Partial Upfront" | jq .
    ```

## Testing
1. Run the tests to ensure the code works correctly:
    ```bash
    python -m unittest discover tests
    ```

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.