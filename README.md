# workflowpro-qa-automation
QA automation case study for a multi-tenant B2B SaaS platform
# QA Automation Case Study: Project Creation Flow

## Overview
This repository contains an automated integration test validating the lifecycle of a project across API, Web UI, and Mobile interfaces. It creates data via API for speed, verifies it via UI for user accuracy, and checks security boundaries.

## Repository Contents
* `tests/`: Contains the automated Python scripts using Pytest and Playwright.
* `docs/`: Contains the Test Plan and Strategy documentation.
* `reports/`: Contains the HTML execution report of the test run.

## Setup Instructions

### 1. Prerequisites
* Python 3.8+
* Pip

### 2. Installation
```bash
pip install -r requirements.txt
playwright install
