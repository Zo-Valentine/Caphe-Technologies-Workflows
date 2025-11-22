#!/usr/bin/env python3
"""
Automated Metadata Fix Script
Fixes common metadata issues across all workflow files
"""

import json
from pathlib import Path
from typing import Dict, Any

# Default values for missing fields
DEFAULT_VALUES = {
    "estimatedTime": "15-30 minutes",
    "prerequisites": ["n8n account", "Basic workflow knowledge"],
    "featured": False
}

def fix_case_sensitivity(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Fix case sensitivity issues in metadata"""
    # Fix category case
    if "category" in metadata and isinstance(metadata["category"], str):
        # Remove any extra text and lowercase
        category = metadata["category"].split("/")[0].strip().lower()
        metadata["category"] = category

    # Fix difficulty case
    if "difficulty" in metadata and isinstance(metadata["difficulty"], str):
        metadata["difficulty"] = metadata["difficulty"].lower()

    return metadata

def add_missing_fields(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Add missing required fields with default values"""
    for field, default_value in DEFAULT_VALUES.items():
        if field not in metadata:
            metadata[field] = default_value

    return metadata

def fix_metadata_file(metadata_path: Path) -> bool:
    """Fix a single metadata file"""
    try:
        # Read existing metadata
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)

        # Apply fixes
        metadata = fix_case_sensitivity(metadata)
        metadata = add_missing_fields(metadata)

        # Write back with pretty formatting
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        return True
    except Exception as e:
        print(f"Error fixing {metadata_path}: {str(e)}")
        return False

def create_missing_metadata(workflow_path: Path) -> bool:
    """Create a metadata file for a workflow that's missing one"""
    try:
        # Extract info from workflow file
        with open(workflow_path, 'r', encoding='utf-8') as f:
            workflow = json.load(f)

        workflow_name = workflow_path.stem
        # Get category from path
        relative_path = workflow_path.relative_to(
            workflow_path.parents[2]  # Go up to workflows dir
        )
        category = str(relative_path.parent).split('/')[0]
        subcategory = str(relative_path.parent).split('/')[-1]

        # Create basic metadata structure
        metadata = {
            "name": workflow_name.replace('-', ' ').title(),
            "description": f"Automated workflow for {workflow_name.replace('-', ' ')}",
            "category": category,
            "subcategory": subcategory.replace('-', ' ').title(),
            "useCase": f"Automates {subcategory.replace('-', ' ')} processes",
            "difficulty": "intermediate",
            "estimatedTime": "15-30 minutes",
            "prerequisites": ["n8n account", "Basic workflow knowledge"],
            "tags": [category, subcategory, "automation"],
            "author": {
                "name": "n8n Team",
                "url": "https://n8n.io"
            },
            "version": "1.0.0",
            "featured": False
        }

        # Create metadata file
        metadata_path = workflow_path.with_name(
            f"{workflow_path.stem}-metadata.json"
        )
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        print(f"  ✅ Created metadata file: {metadata_path.name}")
        return True
    except Exception as e:
        print(f"  ❌ Error creating metadata for {workflow_path}: {str(e)}")
        return False

def find_workflows(base_dir: Path):
    """Find all workflow and metadata files"""
    workflows_with_metadata = []
    workflows_without_metadata = []

    for workflow_file in base_dir.rglob("*.json"):
        # Skip metadata files and templates
        if workflow_file.name.endswith("-metadata.json"):
            continue
        if workflow_file.name == "metadata-template.json":
            continue
        if workflow_file.parent == base_dir:
            continue

        # Check if metadata exists
        metadata_file = workflow_file.with_name(
            f"{workflow_file.stem}-metadata.json"
        )

        if metadata_file.exists():
            workflows_with_metadata.append(metadata_file)
        else:
            workflows_without_metadata.append(workflow_file)

    return workflows_with_metadata, workflows_without_metadata

def main():
    """Main fix function"""
    base_dir = Path(__file__).parent.parent / "workflows"

    print("🔧 Automated Metadata Fix Script")
    print("=" * 80)
    print()

    # Find all workflows
    with_metadata, without_metadata = find_workflows(base_dir)

    total = len(with_metadata) + len(without_metadata)
    print(f"Found {total} workflows:")
    print(f"  - {len(with_metadata)} with metadata files")
    print(f"  - {len(without_metadata)} missing metadata files")
    print()

    fixed_count = 0
    created_count = 0
    error_count = 0

    # Fix existing metadata files
    if with_metadata:
        print("📝 Fixing existing metadata files...")
        print("-" * 80)
        for metadata_path in with_metadata:
            relative_path = metadata_path.relative_to(base_dir)
            print(f"\n📄 {relative_path}")

            if fix_metadata_file(metadata_path):
                print("  ✅ Fixed")
                fixed_count += 1
            else:
                print("  ❌ Failed")
                error_count += 1

    # Create missing metadata files
    if without_metadata:
        print("\n\n📝 Creating missing metadata files...")
        print("-" * 80)
        for workflow_path in without_metadata:
            relative_path = workflow_path.relative_to(base_dir)
            print(f"\n📄 {relative_path}")

            if create_missing_metadata(workflow_path):
                created_count += 1
            else:
                error_count += 1

    # Print summary
    print("\n" + "=" * 80)
    print("\n✨ FIX SUMMARY")
    print("=" * 80)
    print(f"\n✅ Fixed existing metadata: {fixed_count}")
    print(f"✅ Created new metadata: {created_count}")
    if error_count > 0:
        print(f"❌ Errors: {error_count}")

    print(f"\n📊 Total processed: {fixed_count + created_count}/{total}")
    print("\n✅ Metadata fix complete!")
    print("\nRun 'python3 scripts/validate_metadata.py' to verify all fixes.")

if __name__ == "__main__":
    main()
