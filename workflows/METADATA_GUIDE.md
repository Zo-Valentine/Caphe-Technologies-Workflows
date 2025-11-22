# Workflow Metadata Template

This template should be used for **every workflow** in the repository to ensure consistency and searchability.

## File Naming Convention

For each workflow, create these files:
```
workflow-name/
├── workflow-name.json          # The n8n workflow JSON
├── metadata.json               # This metadata file
└── README.md                   # Human-readable documentation
```

## Metadata Fields Explained

### Required Fields

- **name**: Short, descriptive workflow name (50 chars max)
- **description**: What the workflow does (200 chars max)
- **category**: Main category (must match folder name)
- **subcategory**: Subcategory (must match subfolder name)
- **difficulty**: One of: `beginner`, `intermediate`, `advanced`
- **version**: Semantic versioning (e.g., "1.0.0")
- **author**: Creator or organization name
- **lastUpdated**: Date in YYYY-MM-DD format

### Recommended Fields

- **tags**: Array of searchable keywords
- **integrations**: List of external services used
- **useCase**: Real-world application example
- **requirements**: Prerequisites for using the workflow
- **estimatedSetupTime**: How long to set up (e.g., "15 minutes")
- **features**: Key capabilities of the workflow
- **limitations**: Known limitations or constraints

### Optional Fields

- **support**: Documentation, video tutorials, contact info
- **pricing**: n8n plan requirements and external service costs

## Difficulty Levels

### Beginner (🟢)
- Minimal configuration required
- Uses common, well-documented services
- Simple, linear workflow
- Few decision points
- Good for learning n8n basics

### Intermediate (🟡)
- Moderate configuration needed
- Multiple integrations
- Conditional logic or branching
- Error handling implemented
- Requires understanding of APIs

### Advanced (🔴)
- Complex configuration
- Many integrations or custom code
- Advanced logic and data transformation
- Robust error handling
- May require technical knowledge of services

## Example Metadata

```json
{
  "name": "Lead Capture to CRM",
  "description": "Automatically capture leads from web forms and add them to Salesforce with enrichment",
  "category": "marketing-sales",
  "subcategory": "lead-generation",
  "difficulty": "intermediate",
  "tags": ["crm", "lead-generation", "automation", "salesforce", "typeform"],
  "integrations": ["Typeform", "Salesforce", "Clearbit"],
  "useCase": "When a user submits a contact form on your website, automatically enrich the lead data and create a new contact in Salesforce",
  "requirements": [
    "Typeform account with API access",
    "Salesforce account with API credentials",
    "Clearbit API key for enrichment (optional)"
  ],
  "version": "1.0.0",
  "author": "Caphe Workflows",
  "lastUpdated": "2025-11-19",
  "estimatedSetupTime": "20 minutes",
  "features": [
    "Automatic lead capture from forms",
    "Data enrichment with Clearbit",
    "Duplicate detection",
    "Automatic lead assignment"
  ],
  "limitations": [
    "Clearbit API has rate limits",
    "Requires Salesforce Pro or higher"
  ]
}
```

## Using This Template

1. **Copy** the `metadata-template.json` file
2. **Rename** it to `metadata.json` in your workflow folder
3. **Fill in** all required fields
4. **Add** recommended fields for better discoverability
5. **Validate** JSON syntax before committing

## Validation Checklist

- [ ] All required fields are filled
- [ ] Category and subcategory match folder structure
- [ ] Difficulty level is accurate
- [ ] Tags are relevant and searchable
- [ ] Version follows semantic versioning
- [ ] Date is in YYYY-MM-DD format
- [ ] JSON syntax is valid
- [ ] Use case is clear and specific

---

*Consistent metadata makes workflows easier to discover, filter, and implement!*
