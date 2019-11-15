# AWS CIS Compliance Test Automation

## Introduction
Neova QA Team requires a set of scripts which can be used to simulate CIS benchmark recommendations for AWS Cloud as compliant and non-compliant. These would be used for generating test cases for Lacework SaaS platform.

There are total 64 such scenarios which needs to be automated.

**CIS Recommendations for AWS Cloud -**
[https://d1.awsstatic.com/whitepapers/compliance/AWS_CIS_Foundations_Benchmark.pdf](https://d1.awsstatic.com/whitepapers/compliance/AWS_CIS_Foundations_Benchmark.pdf)

## Client
Lacework Inc.

## Technology Stack
- Ubuntu 18 
- Python 3.5
- Boto 3

## High Level Design

- There will be a master script which would be running "n" number of these scripts as required.
- We will create 64 scripts, one for each recommendation.
- Every script will run in two modes. To simulate compliance and non-compliance.
- Logs will be printed on screen. If required we can store these logs for auditing purposes.

## Low Level Design
- The 64 individual scripts for each recommendation would be placed in one directory.
- All the scripts would have one config file which would have common functions such as for logging, authentication etc.
- One file would hold the configurable parameters for all the scripts.
- The individual scripts would be called with the command as described below -
For example -
if the recommendation is for "IAM - Avoid the use of the "root" account" then the script would be called by the command -
./iam-avoid-root-account.py <compliant|non-compliant>

## Workflow
- All the tasks related to the project would be created as Issues in gitlab.
- Developers would pick up the issues from the issue board.
- They would work on one issue at a time.
- Once the code is ready for any issue they would commit the changes to their respective repo and submit a merge request.
- Merge request to the master would be reviewed by QA team and would be merged to the master.
- QA team can suggest enhancements in the merge request which developers would fulfil.
- Once the code is approved, developers would pickup another issue and start working on it.
- After all the scripts are completed. The project would be closed and handed over to the QA team to manage.

## Contributors

- DevOps Team (Development)
- Infrastructure Team (Development)
- QA Team (Review)

**Individual Contribution**
- Arpit Airan - Design & Supervision
- Mayur Rathod - Approver for Code Submission