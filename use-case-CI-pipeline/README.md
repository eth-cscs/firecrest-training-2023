# Creating a CI/CD pipeline with FirecREST

## Goal of the excercise

Create a CI/CD pipeline that will run in Piz daint.
In the repository you can find the code that is tested and the pipeline is mostly set up so you will only need to fill the parts that will submit the job in the supercomputer and the processing of the results.

## Prerequisites

- **Basic python and git knowledge**: The task involves very basic Python.
Even if you have experience with another programming language, you'll likely find the task manageable.
- **CSCS user account**: The pipeline is alredy configured for access to Piz Daint but it requires minimal changes to customize for a different machine.
- **Github account**: The CI will utilize resources from your GitHub account, so make sure you have one.
- **Basic CI/CD understanding**: Familiarity with basic concepts of Continuous Integration and Continuous Deployment processes is recommended.

## Getting Started

1. **Create an OIDC client, if you haven't already.**

1. **Fork and Clone the Repository:**
     - Fork the repository by clicking the "Fork" button at the top right of the GitHub repository page.
    - Clone the forked repository to your local machine:

        ```bash
        git clone https://github.com/your-username/your-repository.git
        cd your-repository
        ```
    - The workflows will be disabled by default in your repo so go ahead and enable them in the "Actions" tab of your repository.

    Replace `your-username` and `your-repository` with your GitHub username and the name of the repository you forked.

1. **Inspect the code that will be tested:**
    Take a moment to review the code in the `dist` folder. This is the code that will be tested in the CI/CD pipeline.

    <!-- TODO! This can change until the course, depending on what we will end up testing. -->

1. **Configure CI/CD Pipeline:**
    - Open the CI configuration file (`.github/workflows/ci.yml`) and, with the help of the comments, try to understand the different steps that are already configured.
    - Find out the secrets that are used in the pipeline and try to figure out how to set them up in your account.
    - You will need to make changes in the file `.ci/ci_script.py`.
    Follow the instructions of the commented sections.

1. **Review Results:**
    Once you've configured the pipeline, commit your changes and push them to your GitHub repository.
    You can follow the progress of the workflow in the "Actions" tab and ensure that the tests ran successfully, and the job was submitted to Piz Daint without issues.

1. **[Optional] Apply this to your own codes:**
    If you are familiar with another CI platform and you have code that you would like to test on Piz Daint we can help you set up the CI.

## Additional Resources

- [OIDC Dashboard](https://oidc-dashboard-prod.cscs.ch/)
- [pyFirecrest documentation](https://pyfirecrest.readthedocs.io)
- [How to set up secrets in Github Actions](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions)
- [FirecREST documentation](https://firecrest.readthedocs.io)
