#!/usr/bin/env python3
"""
Caphè Technologies Workflows Integration Script
Transforms business-focused workflows into advanced automation platform structure.
Integrates workflows into the Caphè Technologies framework.
"""

import json
import os
import shutil
import glob
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple
import re


class CapheTechnologiesIntegrator:
    """Integrates workflows into Caphè Technologies platform structure."""

    def __init__(self, source_dir: str, target_dir: str):
        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)
        self.integration_log = []
        self.category_mapping = self._create_category_mapping()

    def _create_category_mapping(self) -> Dict[str, str]:
        """Map our business categories to caphe-workflows integration categories."""
        return {
            # Our Category -> Primary Integration Category for caphe-workflows
            'content-media': 'Openai',  # AI-powered content workflows
            'customer-service': 'Slack', # Communication-focused workflows
            'data-analytics': 'Googlesheets', # Data processing workflows
            'ecommerce': 'Shopify', # E-commerce workflows
            'education': 'Notion', # Knowledge management workflows
            'finance-accounting': 'Quickbooks', # Financial workflows
            'general-utilities': 'Automation', # General automation workflows
            'healthcare': 'Automation', # Healthcare automation
            'human-resources': 'Gmail', # HR communication workflows
            'it-development': 'Github', # Development workflows
            'marketing-sales': 'Hubspot', # CRM and marketing workflows
            'operations-logistics': 'Airtable' # Operations management
        }

    def analyze_workflow_structure(self) -> Dict[str, Any]:
        """Analyze our current workflow structure for integration planning."""
        analysis = {
            'categories': {},
            'total_workflows': 0,
            'workflow_files': [],
            'metadata_files': []
        }

        for metadata_file in glob.glob(f"{self.source_dir}/**/*-metadata.json", recursive=True):
            metadata_path = Path(metadata_file)
            workflow_file = metadata_file.replace('-metadata.json', '.json')

            if os.path.exists(workflow_file):
                analysis['workflow_files'].append(workflow_file)
                analysis['metadata_files'].append(metadata_file)
                analysis['total_workflows'] += 1

                # Extract category structure
                rel_path = metadata_path.relative_to(self.source_dir)
                parts = rel_path.parts
                if len(parts) >= 2:
                    category = parts[0]
                    subcategory = parts[1]

                    if category not in analysis['categories']:
                        analysis['categories'][category] = {}
                    if subcategory not in analysis['categories'][category]:
                        analysis['categories'][category][subcategory] = []

                    analysis['categories'][category][subcategory].append({
                        'workflow_file': workflow_file,
                        'metadata_file': metadata_file,
                        'name': metadata_path.stem.replace('-metadata', '')
                    })

        return analysis

    def load_workflow_metadata(self, workflow_file: str, metadata_file: str) -> Tuple[Dict, Dict]:
        """Load both workflow JSON and metadata JSON files."""
        with open(workflow_file, 'r', encoding='utf-8') as f:
            workflow_data = json.load(f)

        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)

        return workflow_data, metadata

    def transform_to_caphe_format(self, workflow_data: Dict, metadata: Dict, category: str) -> Dict:
        """Transform our workflow format to caphe-workflows format."""

        # Generate caphe-style filename
        # Format: {number}_{primary_integration}_{secondary}_Create_{trigger_type}.json
        primary_integration = self.category_mapping.get(category, 'Automation')
        workflow_name = re.sub(r'[^a-zA-Z0-9]', '', metadata.get('name', 'Workflow'))

        # Determine trigger type from workflow
        trigger_type = self._analyze_trigger_type(workflow_data)

        # Create enhanced meta section with our rich metadata
        caphe_meta = {
            "instanceId": f"workflow-{hash(metadata.get('name', '')) % 100000:05d}",
            "versionId": metadata.get('version', '1.0.0'),
            "createdAt": datetime.now().isoformat(),
            "updatedAt": datetime.now().isoformat(),
            "owner": metadata.get('author', 'caphe-user'),
            "license": "MIT",
            "category": category,  # Our business category
            "subcategory": metadata.get('subcategory', ''),
            "status": "active",
            "priority": self._map_difficulty_to_priority(metadata.get('difficulty', 'medium')),
            "environment": "production",
            # Enhanced metadata fields
            "business_metadata": {
                "useCase": metadata.get('useCase', ''),
                "difficulty": metadata.get('difficulty', 'medium'),
                "estimatedSetupTime": metadata.get('estimatedSetupTime', '30 minutes'),
                "features": metadata.get('features', []),
                "limitations": metadata.get('limitations', []),
                "requirements": metadata.get('requirements', []),
                "tags": metadata.get('tags', []),
                "integrations": metadata.get('integrations', []),
                "pricing": metadata.get('pricing', {}),
                "lastUpdated": metadata.get('lastUpdated', datetime.now().strftime('%Y-%m-%d'))
            }
        }

        # Ensure workflow has nodes
        if 'nodes' not in workflow_data:
            workflow_data['nodes'] = []

        # Ensure workflow has connections
        if 'connections' not in workflow_data:
            workflow_data['connections'] = {}

        # Add error handling nodes if not present
        workflow_data = self._add_error_handling(workflow_data)

        # Create final caphe-workflows format
        caphe_workflow = {
            "meta": caphe_meta,
            "nodes": workflow_data.get('nodes', []),
            "connections": workflow_data.get('connections', {}),
            "name": metadata.get('name', 'Imported Workflow'),
            "settings": workflow_data.get('settings', {
                "executionOrder": "v1",
                "saveManualExecutions": True,
                "callerPolicy": "workflowsFromSameOwner"
            }),
            # Add our enhanced fields for better searchability
            "tags": metadata.get('tags', []),
            "active": True,
            "staticData": workflow_data.get('staticData', {}),
            "pinData": workflow_data.get('pinData', {}),
            "versionId": 1
        }

        return caphe_workflow

    def _analyze_trigger_type(self, workflow_data: Dict) -> str:
        """Analyze workflow to determine trigger type."""
        nodes = workflow_data.get('nodes', [])

        for node in nodes:
            node_type = node.get('type', '')
            if 'trigger' in node_type.lower():
                if 'webhook' in node_type.lower() or 'form' in node_type.lower():
                    return 'Webhook'
                elif 'schedule' in node_type.lower() or 'cron' in node_type.lower():
                    return 'Scheduled'
                elif 'manual' in node_type.lower():
                    return 'Manual'

        # Default to Complex for AI agents and multi-step workflows
        return 'Complex'

    def _map_difficulty_to_priority(self, difficulty: str) -> str:
        """Map our difficulty levels to caphe priority levels."""
        mapping = {
            'beginner': 'low',
            'intermediate': 'medium',
            'advanced': 'high',
            'expert': 'high'
        }
        return mapping.get(difficulty.lower(), 'medium')

    def _add_error_handling(self, workflow_data: Dict) -> Dict:
        """Add basic error handling to workflow if not present."""
        nodes = workflow_data.get('nodes', [])

        # Check if error handling already exists
        has_error_handling = any('error' in node.get('name', '').lower() or
                                'stopAndError' in node.get('type', '')
                                for node in nodes)

        if not has_error_handling and nodes:
            # Add a basic error handler
            error_node = {
                "id": f"error-{hash(str(nodes)) % 100000:08x}",
                "name": "Error Handler",
                "type": "n8n-nodes-base.stopAndError",
                "typeVersion": 1,
                "position": [1000, 400],
                "parameters": {
                    "message": "Workflow execution error",
                    "options": {}
                }
            }
            workflow_data['nodes'].append(error_node)

        return workflow_data

    def generate_caphe_filename(self, metadata: Dict, category: str, index: int) -> str:
        """Generate caphe-workflows style filename."""
        primary_integration = self.category_mapping.get(category, 'Automation')

        # Clean workflow name for filename
        name_part = re.sub(r'[^a-zA-Z0-9]', '', metadata.get('name', 'Workflow'))[:20]

        # Use our enhanced naming with business context
        filename = f"{index:04d}_{primary_integration}_{name_part}_{category}_Enhanced.json"

        return filename

    def integrate_workflow(self, workflow_file: str, metadata_file: str, category: str, index: int) -> Dict[str, Any]:
        """Integrate a single workflow into caphe-workflows structure."""
        try:
            # Load our workflow and metadata
            workflow_data, metadata = self.load_workflow_metadata(workflow_file, metadata_file)

            # Transform to caphe format
            caphe_workflow = self.transform_to_caphe_format(workflow_data, metadata, category)

            # Determine target integration directory
            target_integration = self.category_mapping.get(category, 'Automation')
            target_dir = self.target_dir / 'workflows' / target_integration
            target_dir.mkdir(parents=True, exist_ok=True)

            # Generate filename
            filename = self.generate_caphe_filename(metadata, category, index)
            target_file = target_dir / filename

            # Save transformed workflow
            with open(target_file, 'w', encoding='utf-8') as f:
                json.dump(caphe_workflow, f, indent=2, ensure_ascii=False)

            result = {
                'success': True,
                'source_workflow': workflow_file,
                'source_metadata': metadata_file,
                'target_file': str(target_file),
                'category': category,
                'integration_category': target_integration,
                'workflow_name': metadata.get('name', 'Unknown')
            }

            self.integration_log.append(result)
            return result

        except Exception as e:
            result = {
                'success': False,
                'error': str(e),
                'source_workflow': workflow_file,
                'source_metadata': metadata_file,
                'category': category
            }
            self.integration_log.append(result)
            return result

    def integrate_all_workflows(self) -> Dict[str, Any]:
        """Integrate all our workflows into caphe-workflows structure."""
        print("🚀 Starting Caphè Technologies Workflows Integration...")

        # Analyze current structure
        analysis = self.analyze_workflow_structure()
        print(f"📊 Found {analysis['total_workflows']} workflows across {len(analysis['categories'])} categories")

        integration_results = {
            'total_processed': 0,
            'successful': 0,
            'failed': 0,
            'results': [],
            'category_breakdown': {}
        }

        workflow_index = 5000  # Start from 5000 to avoid conflicts with existing workflows

        # Process each category
        for category, subcategories in analysis['categories'].items():
            print(f"\n📁 Processing category: {category}")
            category_results = []

            for subcategory, workflows in subcategories.items():
                print(f"  📂 Subcategory: {subcategory} ({len(workflows)} workflows)")

                for workflow_info in workflows:
                    workflow_index += 1
                    result = self.integrate_workflow(
                        workflow_info['workflow_file'],
                        workflow_info['metadata_file'],
                        category,
                        workflow_index
                    )

                    integration_results['total_processed'] += 1
                    category_results.append(result)

                    if result['success']:
                        integration_results['successful'] += 1
                        print(f"    ✅ {result['workflow_name']}")
                    else:
                        integration_results['failed'] += 1
                        print(f"    ❌ {result.get('workflow_name', 'Unknown')}: {result['error']}")

            integration_results['category_breakdown'][category] = category_results
            integration_results['results'].extend(category_results)

        # Save integration report
        self._save_integration_report(integration_results)

        return integration_results

    def _save_integration_report(self, results: Dict[str, Any]) -> None:
        """Save detailed integration report."""
        report_file = self.target_dir / 'integration_report.json'

        report = {
            'integration_date': datetime.now().isoformat(),
            'source_directory': str(self.source_dir),
            'target_directory': str(self.target_dir),
            'category_mapping': self.category_mapping,
            'results': results,
            'summary': {
                'total_workflows': results['total_processed'],
                'successful_integrations': results['successful'],
                'failed_integrations': results['failed'],
                'success_rate': f"{(results['successful'] / results['total_processed'] * 100):.1f}%" if results['total_processed'] > 0 else "0%"
            }
        }

        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"\n📋 Integration report saved to: {report_file}")

    def update_caphe_database(self) -> None:
        """Update caphe-workflows database with our integrated workflows."""
        print("\n🔄 Updating caphe-workflows database...")

        # Import caphe's database module
        import sys
        sys.path.append(str(self.target_dir))

        try:
            from workflow_db import WorkflowDatabase

            # Initialize database
            db_path = self.target_dir / 'workflows.db'
            db = WorkflowDatabase(str(db_path))

            # Rebuild index to include our workflows
            db.rebuild_index()

            print("✅ Database updated successfully")

        except Exception as e:
            print(f"❌ Database update failed: {e}")

    def generate_enhanced_search_index(self) -> None:
        """Generate enhanced search index including our business categories."""
        print("\n🔍 Generating enhanced search index...")

        try:
            # Run caphe's search index generator
            os.chdir(self.target_dir)
            os.system("python scripts/generate_search_index.py")

            print("✅ Search index generated successfully")

        except Exception as e:
            print(f"❌ Search index generation failed: {e}")


def main():
    """Main integration function."""
    print("🎯 Caphè Technologies Workflows Integration Tool")
    print("=" * 50)

    # Define paths
    source_workflows = "/Users/Apple/Caphe Workflows/workflows"
    target_caphe = "/Users/Apple/Caphe Workflows/frameworks/caphe-workflows"

    # Verify paths exist
    if not os.path.exists(source_workflows):
        print(f"❌ Source directory not found: {source_workflows}")
        return

    if not os.path.exists(target_caphe):
        print(f"❌ Target directory not found: {target_caphe}")
        return

    # Initialize integrator
    integrator = CapheTechnologiesIntegrator(source_workflows, target_caphe)

    # Perform integration
    results = integrator.integrate_all_workflows()

    # Update database and search index
    integrator.update_caphe_database()
    integrator.generate_enhanced_search_index()

    # Print final summary
    print("\n" + "=" * 50)
    print("🎉 INTEGRATION COMPLETE")
    print("=" * 50)
    print(f"✅ Successfully integrated: {results['successful']} workflows")
    print(f"❌ Failed integrations: {results['failed']} workflows")
    print(f"📈 Success rate: {(results['successful'] / results['total_processed'] * 100):.1f}%")
    print(f"📂 Workflows distributed across {len(set(r.get('integration_category') for r in results['results'] if r['success']))} integration categories")

    print(f"\n🌐 Next steps:")
    print(f"1. Review integration report: {target_caphe}/integration_report.json")
    print(f"2. Start caphe server: cd {target_caphe} && python run.py")
    print(f"3. Access web interface: http://localhost:8000")


if __name__ == "__main__":
    main()
