
# Contributing to Biophysics 4S03 Project

Thank you for your interest in contributing to this project! Please follow the guidelines below to ensure a smooth workflow for everyone involved.

## Getting Started

1. **Fork the repository**: Start by forking the main repository to your own GitHub account. This will create your own copy of the project.

2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR-USERNAME/REPO-NAME.git
   cd REPO-NAME
   ```

3. **Add the main repository as a remote**:
   ```bash
   git remote add upstream https://github.com/MAIN-REPO-OWNER/REPO-NAME.git
   ```

## Workflow

1. **Sync with the main repository**:
   Before starting your work, ensure your fork is up to date with the latest changes from the `release` branch.
   ```bash
   git fetch upstream
   git checkout release
   git merge upstream/release
   ```

2. **Create a new branch for your changes**:
   Always work on a new branch instead of the `release` branch.
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**: Work on your feature or bug fix.

4. **Commit your changes**:
   Once you're satisfied with your work, commit your changes with a meaningful message.
   ```bash
   git add .
   git commit -m "Add feature/fix: description of changes"
   ```

5. **Push your changes to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Submit a pull request (PR)**:
   Go to the main repository and submit a PR from your branch into the `release` branch. Make sure to provide a clear description of your changes.

## Reviewing Process

1. Your PR will be reviewed by one of the project maintainers.
2. If changes are requested, make the necessary updates and push them to your branch. The PR will automatically update.
3. Once approved, your changes will be merged into the `release` branch.

## General Guidelines

- **Code Style**: Follow any coding style guidelines established in the project.
- **Commit Messages**: Write clear and concise commit messages.
- **Testing**: Ensure that your changes pass any relevant tests.

Thank you for contributing to the project!
