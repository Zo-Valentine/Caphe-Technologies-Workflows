# Contributing to Caphè Technologies Workflows

☕ **Welcome!** We're excited that you're interested in contributing to Caphè Technologies Workflows. This platform powers workflow automation for healthcare organizations, and your contributions help improve efficiency, compliance, and patient care delivery.

## Contents

- [Contributing to Caphè Technologies Workflows](#contributing-to-caphè-technologies-workflows)
	- [Contents](#contents)
	- [Code of Conduct](#code-of-conduct)
	- [Our Values](#our-values)
	- [Healthcare Considerations](#healthcare-considerations)
	- [Ways to Contribute](#ways-to-contribute)
	- [Workflow Contributions](#workflow-contributions)
	- [Code Contributions](#code-contributions)
	- [Directory Structure](#directory-structure)
	- [Development Setup](#development-setup)
		- [Dev Container](#dev-container)
		- [Requirements](#requirements)
			- [Node.js](#nodejs)
			- [pnpm](#pnpm)
				- [pnpm workspaces](#pnpm-workspaces)
			- [corepack](#corepack)
			- [Build tools](#build-tools)
		- [Actual Setup](#actual-setup)
		- [Start](#start)
	- [Development Cycle](#development-cycle)
		- [Community PR Guidelines](#community-pr-guidelines)
			- [**1. Change Request/Comment**](#1-change-requestcomment)
			- [**2. General Requirements**](#2-general-requirements)
			- [**3. PR Specific Requirements**](#3-pr-specific-requirements)
			- [**4. Workflow Summary for Non-Compliant PRs**](#4-workflow-summary-for-non-compliant-prs)
		- [Test Suite](#test-suite)
			- [Unit Tests](#unit-tests)
			- [Code Coverage](#code-coverage)
			- [E2E Tests](#e2e-tests)
	- [Create Custom Nodes](#create-custom-nodes)
	- [Documentation](#documentation)
	- [Contributor License Agreement](#contributor-license-agreement)
	- [Recognition](#recognition)

## Code of Conduct

This project and everyone participating in it are governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to conduct@caphetechnologies.com.

We are committed to creating a welcoming, inclusive, and professional environment for all contributors.

## Our Values

At Caphè Technologies, we operate with these core values:

- ☕ **Excellence**: We deliver high-quality solutions with attention to detail
- 🤝 **Collaboration**: We work together to solve complex problems
- ❤️ **Empathy**: We care about the people our technology serves
- 🎯 **Professionalism**: We maintain the highest standards in all our work
- ⭐ **Innovation**: We embrace new ideas and continuous improvement

## Healthcare Considerations

When contributing to Caphè Technologies Workflows, please keep in mind:

- **HIPAA Awareness**: Be mindful of Protected Health Information (PHI) in examples and test data
- **Security First**: Prioritize secure coding practices, especially for authentication and data handling
- **Compliance Mindset**: Consider regulatory requirements in healthcare workflows
- **Patient Safety**: Workflows should never compromise patient safety or care quality
- **Data Privacy**: Respect privacy regulations and data protection principles

> ⚕️ **Important**: Never include real patient data, PHI, or sensitive healthcare information in contributions, issues, or pull requests.

## Ways to Contribute

There are many ways to contribute to Caphè Technologies Workflows:

1. **Workflow Templates**: Share workflow automation solutions for common healthcare scenarios
2. **Code Improvements**: Enhance existing features, fix bugs, or optimize performance
3. **Documentation**: Improve guides, tutorials, or API documentation
4. **Testing**: Add test coverage or identify bugs
5. **Community Support**: Help others in discussions or troubleshooting
6. **Feature Suggestions**: Propose new features or enhancements

## Workflow Contributions

### Metadata Requirements

All workflow contributions **must** include complete metadata:

```json
{
  "workflowName": "Descriptive Workflow Name",
  "description": "Clear description of what the workflow does",
  "category": "healthcare-staffing | patient-care | compliance | etc.",
  "subcategory": "specific-use-case",
  "complexity": "beginner | intermediate | advanced",
  "estimatedSetupTime": "5-10 minutes",
  "prerequisites": ["Required services", "API keys", "etc."],
  "tags": ["relevant", "searchable", "tags"],
  "author": "Your Name",
  "dateAdded": "YYYY-MM-DD",
  "lastUpdated": "YYYY-MM-DD"
}
```

See [workflows/METADATA_GUIDE.md](workflows/METADATA_GUIDE.md) for detailed guidelines.

### Workflow Quality Standards

- **Clear Naming**: Use descriptive names for nodes and connections
- **Documentation**: Include inline comments explaining logic
- **Error Handling**: Implement proper error handling and fallbacks
- **Testing**: Test workflows thoroughly with sample data
- **Privacy**: Remove any sensitive or identifying information
- **Compliance**: Ensure workflows meet healthcare compliance requirements

### Submitting Workflows

1. Create your workflow with complete metadata
2. Test thoroughly with representative data (no PHI!)
3. Export the workflow JSON
4. Place in appropriate category folder under `/workflows/`
5. Update the category README with your workflow
6. Submit a pull request with clear description

## Code Contributions

### Code Quality Standards

- **TypeScript**: Use TypeScript for type safety (no `ts-ignore`)
- **Linting**: Follow ESLint rules and Biome formatting
- **Testing**: Include unit tests, integration tests, and E2E tests where applicable
- **Documentation**: Add JSDoc comments for functions and complex logic
- **Security**: Follow secure coding practices, especially for authentication and data handling

### Before You Start

1. Check existing issues and pull requests to avoid duplication
2. For major changes, open an issue first to discuss your approach
3. Ensure your development environment is properly set up
4. Review our [Code of Conduct](CODE_OF_CONDUCT.md)

### Development Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes following our coding standards
4. Write or update tests
5. Run the full test suite: `pnpm test`
6. Commit with clear, descriptive messages
7. Push to your fork
8. Open a pull request with a comprehensive description

### Pull Request Guidelines

- **One Feature Per PR**: Keep pull requests focused on a single feature or fix
- **Descriptive Titles**: Use clear, descriptive PR titles
- **Comprehensive Description**: Explain what changes were made and why
- **Tests Required**: Include appropriate test coverage
- **Documentation**: Update documentation for any user-facing changes
- **Review Feedback**: Respond to review comments within 14 days

## Code of conduct

## Directory Structure

Caphè Technologies Workflows is organized as a monorepo with multiple packages:

**Key Directories:**

- [/workflows](/workflows) - 2,080+ workflow templates organized by category
- [/frameworks/caphe-workflows](/frameworks/caphe-workflows) - Python Flask API server
- [/caphe-workflows-ui](/caphe-workflows-ui) - React + Vite frontend for workflow browsing
- [/caphe-workflows-frontend](/caphe-workflows-frontend) - Additional frontend components
- [/packages](/packages) - Core n8n modules (underlying platform)
- [/packages/cli](/packages/cli) - CLI code for front- & backend
- [/packages/core](/packages/core) - Core workflow execution engine
- [/packages/nodes-base](/packages/nodes-base) - Base nodes and integrations
- [/packages/workflow](/packages/workflow) - Workflow interfaces
- [/docker/images](/docker/images) - Docker container configurations

## Development setup

If you want to change or extend n8n you have to make sure that all the needed
dependencies are installed and the packages get linked correctly. Here's a short guide on how that can be done:

### Dev Container

If you already have VS Code and Docker installed, you can click [here](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/n8n-io/n8n) to get started. Clicking these links will cause VS Code to automatically install the Dev Containers extension if needed, clone the source code into a container volume, and spin up a dev container for use.

### Requirements

#### Node.js

[Node.js](https://nodejs.org/en/) version 22.16 or newer is required for development purposes.

#### pnpm

[pnpm](https://pnpm.io/) version 10.2 or newer is required for development purposes. We recommend installing it with [corepack](#corepack).

##### pnpm workspaces

n8n is split up into different modules which are all in a single mono repository.
To facilitate the module management, [pnpm workspaces](https://pnpm.io/workspaces) are used.
This automatically sets up file-links between modules which depend on each other.

#### corepack

We recommend enabling [Node.js corepack](https://nodejs.org/docs/latest-v16.x/api/corepack.html) with `corepack enable`.

You can install the correct version of pnpm using `corepack prepare --activate`.

**IMPORTANT**: If you have installed Node.js via homebrew, you'll need to run `brew install corepack`, since homebrew explicitly removes `npm` and `corepack` from [the `node` formula](https://github.com/Homebrew/homebrew-core/blob/master/Formula/node.rb#L66).

**IMPORTANT**: If you are on windows, you'd need to run `corepack enable` and `corepack prepare --activate` in a terminal as an administrator.

#### Build tools

The packages which n8n uses depend on a few build tools:

Debian/Ubuntu:

```
apt-get install -y build-essential python
```

CentOS:

```
yum install gcc gcc-c++ make
```

Windows:

```
npm add -g windows-build-tools
```

MacOS:

No additional packages required.

#### actionlint (for GitHub Actions workflow development)

If you plan to modify GitHub Actions workflow files (`.github/workflows/*.yml`), you'll need [actionlint](https://github.com/rhysd/actionlint) for workflow validation:

**macOS (Homebrew):**
```
brew install actionlint
```
> **Note:** actionlint is only required if you're modifying workflow files. It runs automatically via git hooks when workflow files are changed.

### Actual Setup

> **IMPORTANT**: All the steps below must be executed at least once to get the development setup running!

Now that all prerequisites are installed, set up the Caphè Technologies Workflows codebase:

1. [Fork](https://guides.github.com/activities/forking/#fork) the Caphè Technologies Workflows repository.

2. Clone your forked repository:

   ```bash
   git clone https://github.com/<your_github_username>/Caphe-Technologies-Workflows.git
   ```

3. Go into repository folder:

   ```bash
   cd Caphe-Technologies-Workflows
   ```

4. Add the original repository as `upstream`:

   ```bash
   git remote add upstream https://github.com/Zo-Valentine/Caphe-Technologies-Workflows.git
   ```

5. Install all dependencies and link modules:

   ```bash
   pnpm install
   ```

6. Build all the code:
   ```bash
   pnpm build
   ```

### Start

To start the application:

```bash
pnpm start
```

To start with tunnel (for webhook testing):

```bash
./packages/cli/bin/n8n start --tunnel
```

To start the Python API server (for workflow management):

```bash
cd frameworks/caphe-workflows
python run.py
```

## Development Cycle

While iterating on code, you can run `pnpm dev`. It will automatically build your code, restart the backend, and refresh the frontend on every change you make.

### Basic Development Workflow

1. Start n8n in development mode:
   ```
   pnpm dev
   ```
2. Hack, hack, hack
3. Check if everything still runs in production mode:
   ```
   pnpm build
   pnpm start
   ```
4. Create tests
5. Run all [tests](#test-suite):
   ```
   pnpm test
   ```
6. Commit code and [create a pull request](https://docs.github.com/en/github/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork)

### Hot Reload for Nodes (N8N_DEV_RELOAD)

When developing custom nodes or credentials, you can enable hot reload to automatically detect changes without restarting the server:

```bash
N8N_DEV_RELOAD=true pnpm dev
```

**Performance considerations:**
- File watching adds overhead to your system, especially on slower machines
- The watcher monitors potentially thousands of files, which can impact CPU and memory usage
- On resource-constrained systems, consider developing without hot reload and manually restarting when needed

### Selective Package Development

Running all packages in development mode can be resource-intensive. For better performance, run only the packages relevant to your work:

#### Available Filtered Commands

- **Backend-only development:**
  ```bash
  pnpm dev:be
  ```
  Excludes frontend packages like editor-ui and design-system

- **Frontend-only development:**
  ```bash
  pnpm dev:fe
  ```
  Runs the backend server and editor-ui development server

- **AI/LangChain nodes development:**
  ```bash
  pnpm dev:ai
  ```
  Runs only essential packages for AI node development

#### Custom Selective Development

For even more focused development, you can run packages individually:

**Example 1: Working on custom nodes**
```bash
# Terminal 1: Build and watch nodes package
cd packages/nodes-base
pnpm dev

# Terminal 2: Run the CLI with hot reload
cd packages/cli
N8N_DEV_RELOAD=true pnpm dev
```

**Example 2: Pure frontend development**
```bash
# Terminal 1: Start the backend server (no watching)
pnpm start

# Terminal 2: Run frontend dev server
cd packages/editor-ui
pnpm dev
```

**Example 3: Working on a specific node package**
```bash
# Terminal 1: Watch your node package
cd packages/nodes-base  # or your custom node package
pnpm watch

# Terminal 2: Run CLI with hot reload
cd packages/cli
N8N_DEV_RELOAD=true pnpm dev
```

### Performance Considerations

The full development mode (`pnpm dev`) runs multiple processes in parallel:

1. **TypeScript compilation** for each package
2. **File watchers** monitoring source files
3. **Nodemon** restarting the backend on changes
4. **Vite dev server** for the frontend with HMR
5. **Multiple build processes** for various packages

**Performance impact:**
- Can consume significant CPU and memory resources
- File system watching creates overhead, especially on:
  - Networked file systems
  - Virtual machines with shared folders
  - Systems with slower I/O performance
- The more packages you run in dev mode, the more system resources are consumed

**Recommendations for resource-constrained environments:**
1. Use selective development commands based on your task
2. Close unnecessary applications to free up resources
3. Monitor system performance and adjust your development approach accordingly

---

### Community PR Guidelines

#### **1. Change Request/Comment**

Please address the requested changes or provide feedback within 14 days. If there is no response or updates to the pull request during this time, it will be automatically closed. The PR can be reopened once the requested changes are applied.

#### **2. General Requirements**

- **Follow the Style Guide:**
  - Ensure your code adheres to n8n's coding standards and conventions (e.g., formatting, naming, indentation). Use linting tools where applicable.
- **TypeScript Compliance:**
  - Do not use `ts-ignore` .
  - Ensure code adheres to TypeScript rules.
- **Avoid Repetitive Code:**
  - Reuse existing components, parameters, and logic wherever possible instead of redefining or duplicating them.
  - For nodes: Use the same parameter across multiple operations rather than defining a new parameter for each operation (if applicable).
- **Testing Requirements:**
  - PRs **must include tests**:
    - Unit tests
    - Workflow tests for nodes (example [here](https://github.com/n8n-io/n8n/tree/master/packages/nodes-base/nodes/Switch/V3/test))
    - UI tests (if applicable)
- **Typos:**
  - Use a spell-checking tool, such as [**Code Spell Checker**](https://marketplace.visualstudio.com/items?itemName=streetsidesoftware.code-spell-checker), to avoid typos.

#### **3. PR Specific Requirements**

- **Small PRs Only:**
  - Focus on a single feature or fix per PR.
- **Descriptive Titles:**
  - Use clear, descriptive titles that explain the change.
- **New Nodes:**
  - New node proposals should be discussed in an issue first. PRs for custom nodes should include comprehensive documentation, tests, and healthcare-appropriate error handling.
- **Workflow Contributions:**
  - All workflow contributions must include complete metadata (see [Workflow Contributions](#workflow-contributions)).
- **Healthcare Compliance:**
  - Code touching patient data, PHI, or healthcare workflows must include security review comments.
- **Typo-Only PRs:**
  - Minor typo fixes should be bundled with other changes when possible.

#### **4. Workflow Summary for Non-Compliant PRs**

- **No Tests:** If tests are not provided, the PR will be auto-closed after **14 days**.
- **Non-Small PRs:** Large or multifaceted PRs will be returned for segmentation.
- **New Nodes/Typo PRs:** Automatically rejected if not aligned with project scope or guidelines.

---

### Test suite

#### Unit tests

Unit tests can be started via:

```
pnpm test
```

If that gets executed in one of the package folders it will only run the tests
of this package. If it gets executed in the n8n-root folder it will run all
tests of all packages.

If you made a change which requires an update on a `.test.ts.snap` file, pass `-u` to the command to run tests or press `u` in watch mode.

#### Code Coverage
We track coverage for all our code on [Codecov](https://app.codecov.io/gh/n8n-io/n8n).
But when you are working on tests locally, we recommend running your tests with env variable `COVERAGE_ENABLED` set to `true`. You can then view the code coverage in the `coverage` folder, or you can use [this VSCode extension](https://marketplace.visualstudio.com/items?itemName=ryanluker.vscode-coverage-gutters) to visualize the coverage directly in VSCode.

#### E2E Tests

We use [Playwright](https://playwright.dev) for end-to-end testing.

E2E tests can be started via:

- `pnpm --filter=n8n-playwright test:local` - Run tests locally (starts local server on port 5680 and runs UI tests)
- `pnpm --filter=n8n-playwright test:local --ui` - Run tests in interactive UI mode (useful for debugging)
- `pnpm --filter=n8n-playwright test:local --grep="test-name"` - Run specific tests matching pattern

See `packages/testing/playwright/README.md` for more test commands and `packages/testing/playwright/CONTRIBUTING.md` for writing guidelines.

**Healthcare Testing Considerations:**
- Never use real PHI in test data
- Test with realistic but synthetic healthcare scenarios
- Verify proper error handling for HIPAA compliance scenarios
- Test authentication and authorization thoroughly

## Create Custom Nodes

Learn about [building nodes](https://docs.n8n.io/integrations/creating-nodes/overview/) to create custom nodes. You can create community nodes and make them available.

**Healthcare Node Development:**
- Include comprehensive error handling
- Document HIPAA considerations
- Implement proper authentication and authorization
- Add data validation for healthcare data formats
- Include audit logging where appropriate

## Documentation

Good documentation helps everyone. Contributions to documentation are highly valued:

- **Code Documentation**: JSDoc comments, inline explanations
- **Workflow Documentation**: Clear descriptions in metadata
- **User Guides**: Step-by-step tutorials
- **API Documentation**: Comprehensive endpoint documentation
- **Healthcare Examples**: Real-world (but sanitized) use cases

Documentation should be:
- Clear and concise
- Technically accurate
- Free of jargon where possible
- Inclusive and accessible

## Contributor License Agreement

To ensure clarity around intellectual property and licensing, contributors are required to sign a [Contributor License Agreement](CONTRIBUTOR_LICENSE_AGREEMENT.md). This is a straightforward process.

The CLA ensures:
- You retain copyright to your contributions
- Caphè Technologies can use your contributions under the project's licenses
- The project remains legally sound and maintainable
- All contributors are protected

**Key Points:**
- By contributing, you agree that your contributions will be dual-licensed under:
  - The n8n Sustainable Use License (for base platform components)
  - The Caphè Technologies Proprietary License (for proprietary enhancements)
- You certify that you have the right to submit your contribution
- You understand the healthcare and compliance implications of your code

For licensing questions, contact: licensing@caphetechnologies.com

## Recognition

We value and recognize our contributors:

- All contributors are listed in our CONTRIBUTORS.md file
- Significant contributions are highlighted in release notes
- Active community members may be invited to join our healthcare advisory board
- Workflow template authors are credited in the workflow metadata

**Ways We Recognize Contributions:**
- 🏆 Featured workflows and templates
- 📝 Blog posts highlighting community contributions
- 🎤 Speaking opportunities at Caphè Technologies events
- 🌟 Community spotlight in newsletters

---

## Getting Help

If you need help or have questions:

- **Technical Questions**: Open a discussion on GitHub
- **Code of Conduct Issues**: conduct@caphetechnologies.com
- **Licensing Questions**: licensing@caphetechnologies.com
- **General Inquiries**: Use GitHub discussions

## Thank You! ☕

Thank you for contributing to Caphè Technologies Workflows. Your work helps healthcare organizations deliver better care through automation and efficiency. Every contribution, no matter how small, makes a difference.

Together, we're building technology that serves healthcare professionals and improves patient outcomes.

---

**License Notice**: This project is dual-licensed. See [LICENSE.md](LICENSE.md) for the n8n Sustainable Use License and [LICENSE_CAPHE.md](LICENSE_CAPHE.md) for the Caphè Technologies Proprietary License. By contributing, you agree to license your contributions under both licenses.
