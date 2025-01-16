# offering_finder

## Overview
`offering_finder` is a tool to search for AWS Reserved Instance offerings and retrieve offering IDs based on specified parameters. Supported AWS services include RDS, ElastiCache, Savings Plans, and OpenSearch.

## Features
- Search for AWS Reserved Instance offerings based on specified parameters
- Output search results in JSON format
- Generate AWS CLI commands to purchase Reserved Instance offerings

## Installation

```bash
git clone https://github.com/0xmks/offering_finder
```

Since this project is managed using `uv`, please refer to [uv's GitHub repository](https://github.com/astral-sh/uv) for instructions on how to install `uv`.

Activate the virtual environment and install the necessary packages using `uv` in the project root:
```bash
uv sync
```

## AWS Profile Setup

Before using the commands, set up an AWS account profile with read permissions. If using a named profile, you can set the AWS profile with the following command:

```sh
export AWS_PROFILE=your_readonly_permission_profile
```

## Usage example

### RDS
Retrieve the offering ID for RDS based on specified parameters:
```bash
uv run cli.py\
 rds \
 --region_name 'ap-northeast-1'\
 --product_description 'MySQL'\
 --db_instance_class 'db.m5.large'\
 --duration 31536000\
 --quantity 2\
 --offering_type 'All Upfront'\
```

### ElastiCache
Retrieve the offering ID for ElastiCache based on specified parameters:
```bash
uv run cli.py\
 elasticache\
 --region_name 'ap-northeast-1'\
 --cache_node_type 'cache.t3.micro'\
 --quantity 2\
 --duration 31536000\
 --product_description 'redis'\
 --offering_type 'All Upfront'\
```

### Savings Plans
Retrieve the offering ID for SavingsPlans based on specified parameters:
```bash
uv run cli.py\
 savingsplans \
 --region_name 'ap-northeast-1'\
 --commitment 0.01\
 --durations 31536000\
 --plan_types 'Compute'\
 --payment_options 'All Upfront'
```

### OpenSearch
Retrieve the offering ID for OpenSearch based on specified parameters:
```bash
uv run cli.py\
 opensearch\
 --region_name 'ap-northeast-1'\
 --payment_option 'ALL_UPFRONT'\
 --instance_type 'c6g.12xlarge.search'\
 --quantity 2\
 --duration 31536000\
```

## Contributing
If you would like to contribute to this project, please fork the repository and submit a pull request.

## License
This project is licensed under the Unlicense.
