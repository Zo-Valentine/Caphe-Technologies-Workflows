#!/usr/bin/env python3
"""
Workflow Metadata Validation Script
Validates all workflow JSON files and their metadata files
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Tuple

# Required metadata fields
REQUIRED_FIELDS = [
    "name",
    "description",
    "category",
    "subcategory",
    "useCase",
    "difficulty",
    "estimatedTime",
    "prerequisites",
    "tags",
    "author",
    "version",
    "featured"
]

# Valid values for specific fields
VALID_DIFFICULTIES = ["beginner", "intermediate", "advanced"]
VALID_CATEGORIES = [
    "content-media",
    "customer-service",
    "data-analytics",
    "ecommerce",
    "education",
    "finance-accounting",
    "general-utilities",
    "healthcare",
    "human-resources",
    "it-development",
    "marketing-sales",
    "operations-logistics"
]

def validate_metadata_structure(metadata: dict, workflow_name: str) -> List[str]:
    """Validate the structure and required fields of metadata"""
    errors = []

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in metadata:
            errors.append(f"Missing required field: {field}")
        elif not metadata[field] and field != "featured":
            errors.append(f"Empty value for required field: {field}")

    # Validate difficulty
    if "difficulty" in metadata and metadata["difficulty"] not in VALID_DIFFICULTIES:
        errors.append(f"Invalid difficulty: {metadata['difficulty']}. Must be one of {VALID_DIFFICULTIES}")

    # Validate category
    if "category" in metadata and metadata["category"] not in VALID_CATEGORIES:
        errors.append(f"Invalid category: {metadata['category']}. Must be one of {VALID_CATEGORIES}")

    # Validate tags is a list
    if "tags" in metadata and not isinstance(metadata["tags"], list):
        errors.append("tags must be a list")

    # Validate prerequisites is a list
    if "prerequisites" in metadata and not isinstance(metadata["prerequisites"], list):
        errors.append("prerequisites must be a list")

    return errors

def validate_workflow_file(workflow_path: Path) -> Tuple[bool, List[str]]:
    """Validate a workflow JSON file"""
    errors = []

    try:
        with open(workflow_path, 'r', encoding='utf-8') as f:
            workflow_data = json.load(f)

        # Check basic structure
        if "nodes" not in workflow_data:
            errors.append("Missing 'nodes' array")

        if "connections" not in workflow_data:
            errors.append("Missing 'connections' object")

    except json.JSONDecodeError as e:
        errors.append(f"Invalid JSON: {str(e)}")
    except Exception as e:
        errors.append(f"Error reading file: {str(e)}")

    return len(errors) == 0, errors

def find_workflows(base_dir: Path) -> List[Tuple[Path, Path]]:
    """Find all workflow files and their metadata files"""
    workflows = []

    # Search recursively for all JSON files
    for workflow_file in base_dir.rglob("*.json"):
        # Skip metadata template and metadata files themselves
        if workflow_file.name == "metadata-template.json":
            continue
        if workflow_file.name.endswith("-metadata.json"):
            continue

        # Skip files in the root workflows directory
        if workflow_file.parent == base_dir:
            continue

        # Look for corresponding metadata file
        metadata_file = workflow_file.with_name(f"{workflow_file.stem}-metadata.json")
        workflows.append((workflow_file, metadata_file))

    return workflows

def main():
    """Main validation function"""
    base_dir = Path(__file__).parent.parent / "workflows"

    if not base_dir.exists():
        print(f"❌ Workflows directory not found: {base_dir}")
        return

    print("🔍 Validating workflow metadata...\n")
    print("=" * 80)

    workflows = find_workflows(base_dir)

    if not workflows:
        print("⚠️  No workflows found!")
        return

    total_workflows = len(workflows)
    valid_workflows = 0
    warnings = 0
    errors_count = 0

    results = {
        "valid": [],
        "missing_metadata": [],
        "invalid_metadata": [],
        "invalid_workflow": []
    }

    for workflow_file, metadata_file in workflows:
        workflow_name = workflow_file.stem
        # Get relative path from workflows directory
        relative_path = workflow_file.relative_to(base_dir)
        category = str(relative_path.parent)

        print(f"\n📄 {category}/{workflow_name}")
        print("-" * 80)

        # Validate workflow file
        workflow_valid, workflow_errors = validate_workflow_file(workflow_file)

        if not workflow_valid:
            print(f"  ❌ Workflow file errors:")
            for error in workflow_errors:
                print(f"     - {error}")
            results["invalid_workflow"].append((workflow_name, category))
            errors_count += len(workflow_errors)
            continue

        # Check if metadata file exists
        if not metadata_file.exists():
            print(f"  ⚠️  Metadata file not found: {metadata_file.name}")
            results["missing_metadata"].append((workflow_name, category))
            warnings += 1
            continue

        # Validate metadata file
        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)

            metadata_errors = validate_metadata_structure(metadata, workflow_name)

            if metadata_errors:
                print(f"  ❌ Metadata validation errors:")
                for error in metadata_errors:
                    print(f"     - {error}")
                results["invalid_metadata"].append((workflow_name, category))
                errors_count += len(metadata_errors)
            else:
                print(f"  ✅ Valid")
                results["valid"].append((workflow_name, category))
                valid_workflows += 1

        except json.JSONDecodeError as e:
            print(f"  ❌ Invalid JSON in metadata file: {str(e)}")
            results["invalid_metadata"].append((workflow_name, category))
            errors_count += 1
        except Exception as e:
            print(f"  ❌ Error reading metadata file: {str(e)}")
            results["invalid_metadata"].append((workflow_name, category))
            errors_count += 1

    # Print summary
    print("\n" + "=" * 80)
    print("\n📊 VALIDATION SUMMARY")
    print("=" * 80)
    print(f"\nTotal workflows found: {total_workflows}")
    print(f"✅ Valid workflows: {valid_workflows}")
    print(f"⚠️  Missing metadata: {len(results['missing_metadata'])}")
    print(f"❌ Invalid metadata: {len(results['invalid_metadata'])}")
    print(f"❌ Invalid workflow files: {len(results['invalid_workflow'])}")
    print(f"\nTotal errors: {errors_count}")
    print(f"Total warnings: {warnings}")

    # Show completion percentage
    completion_rate = (valid_workflows / total_workflows * 100) if total_workflows > 0 else 0
    print(f"\n📈 Completion rate: {completion_rate:.1f}%")

    # List valid workflows by category
    if results["valid"]:
        print("\n✅ COMPLETED WORKFLOWS BY CATEGORY:")
        print("-" * 80)
        category_counts = {}
        for workflow_name, category in results["valid"]:
            if category not in category_counts:
                category_counts[category] = []
            category_counts[category].append(workflow_name)

        for category in sorted(category_counts.keys()):
            print(f"\n{category} ({len(category_counts[category])} workflows):")
            for workflow in sorted(category_counts[category]):
                print(f"  ✓ {workflow}")

    # List workflows needing attention
    if results["missing_metadata"]:
        print("\n⚠️  WORKFLOWS MISSING METADATA:")
        print("-" * 80)
        for workflow_name, category in results["missing_metadata"]:
            print(f"  - {category}/{workflow_name}")

    if results["invalid_metadata"]:
        print("\n❌ WORKFLOWS WITH INVALID METADATA:")
        print("-" * 80)
        for workflow_name, category in results["invalid_metadata"]:
            print(f"  - {category}/{workflow_name}")

    if results["invalid_workflow"]:
        print("\n❌ INVALID WORKFLOW FILES:")
        print("-" * 80)
        for workflow_name, category in results["invalid_workflow"]:
            print(f"  - {category}/{workflow_name}")

    print("\n" + "=" * 80)

    # Exit code based on errors
    if errors_count > 0:
        print("\n⚠️  Validation completed with errors")
        exit(1)
    elif warnings > 0:
        print("\n⚠️  Validation completed with warnings")
        exit(0)
    else:
        print("\n✅ All workflows validated successfully!")
        exit(0)

if __name__ == "__main__":
    main()
