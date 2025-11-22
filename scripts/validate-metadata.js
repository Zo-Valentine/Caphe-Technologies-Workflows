#!/usr/bin/env node

/**
 * Workflow Metadata Validator
 * Validates all metadata files against the schema and generates reports
 */

const fs = require('fs');
const path = require('path');
const glob = require('glob');

// Required fields for all metadata files
const REQUIRED_FIELDS = [
  'name',
  'description',
  'category',
  'difficulty',
  'tags',
  'integrations',
  'useCase',
  'requirements',
  'estimatedSetupTime',
  'version',
  'author',
  'lastUpdated'
];

// Valid enum values
const VALID_DIFFICULTIES = ['beginner', 'intermediate', 'advanced'];
const VALID_CATEGORIES = [
  'Healthcare',
  'Customer Service',
  'Data Analytics',
  'General Utilities',
  'IT Development',
  'Content Media',
  'Marketing & Sales',
  'Finance & Accounting',
  'Human Resources',
  'Operations & Logistics',
  'E-commerce',
  'Education'
];

// Find all metadata files
console.log('🔍 Searching for metadata files...\n');
const metadataFiles = glob.sync('workflows/**/*-metadata.json', { cwd: process.cwd() });
console.log(`Found ${metadataFiles.length} metadata files\n`);

const errors = [];
const warnings = [];
const stats = {
  total: metadataFiles.length,
  valid: 0,
  invalid: 0,
  byCategory: {},
  byDifficulty: {},
  totalTags: 0,
  totalIntegrations: new Set()
};

// Validate each metadata file
metadataFiles.forEach((file, index) => {
  console.log(`[${index + 1}/${metadataFiles.length}] Validating ${file}...`);

  try {
    const data = JSON.parse(fs.readFileSync(file, 'utf8'));
    let fileErrors = 0;

    // Check required fields
    REQUIRED_FIELDS.forEach(field => {
      if (!data[field]) {
        errors.push(`${file}: Missing required field "${field}"`);
        fileErrors++;
      }
    });

    // Validate difficulty
    if (data.difficulty && !VALID_DIFFICULTIES.includes(data.difficulty.toLowerCase())) {
      errors.push(`${file}: Invalid difficulty "${data.difficulty}" (must be beginner, intermediate, or advanced)`);
      fileErrors++;
    }

    // Validate category
    if (data.category && !VALID_CATEGORIES.includes(data.category)) {
      warnings.push(`${file}: Category "${data.category}" not in standard list`);
    }

    // Validate tags
    if (data.tags) {
      if (data.tags.length < 3) {
        warnings.push(`${file}: Should have at least 3 tags (currently ${data.tags.length})`);
      }

      // Check tag format (lowercase-with-hyphens)
      data.tags.forEach(tag => {
        if (!/^[a-z0-9]+(-[a-z0-9]+)*$/.test(tag)) {
          warnings.push(`${file}: Tag "${tag}" should be lowercase-with-hyphens format`);
        }
      });

      stats.totalTags += data.tags.length;
    }

    // Validate integrations
    if (data.integrations) {
      data.integrations.forEach(integration => {
        stats.totalIntegrations.add(integration);
      });
    }

    // Validate version format (semantic versioning)
    if (data.version && !/^\d+\.\d+\.\d+$/.test(data.version)) {
      errors.push(`${file}: Invalid version format "${data.version}" (should be X.Y.Z)`);
      fileErrors++;
    }

    // Validate date format
    if (data.lastUpdated && !/^\d{4}-\d{2}-\d{2}$/.test(data.lastUpdated)) {
      warnings.push(`${file}: lastUpdated should be in YYYY-MM-DD format`);
    }

    // Check description length
    if (data.description && data.description.length < 100) {
      warnings.push(`${file}: Description is too short (${data.description.length} chars, recommend 150-300)`);
    }

    // Check for recommended fields
    if (!data.pricing) {
      warnings.push(`${file}: Missing recommended field "pricing"`);
    }

    if (!data.support) {
      warnings.push(`${file}: Missing recommended field "support"`);
    }

    // Update stats
    if (fileErrors === 0) {
      stats.valid++;
    } else {
      stats.invalid++;
    }

    // Category stats
    if (data.category) {
      stats.byCategory[data.category] = (stats.byCategory[data.category] || 0) + 1;
    }

    // Difficulty stats
    if (data.difficulty) {
      const diff = data.difficulty.toLowerCase();
      stats.byDifficulty[diff] = (stats.byDifficulty[diff] || 0) + 1;
    }

  } catch (err) {
    errors.push(`${file}: Failed to parse JSON - ${err.message}`);
    stats.invalid++;
  }
});

// Print results
console.log('\n' + '='.repeat(60));
console.log('📊 VALIDATION RESULTS');
console.log('='.repeat(60));

console.log(`\n✅ Valid Files: ${stats.valid}/${stats.total}`);
console.log(`❌ Invalid Files: ${stats.invalid}/${stats.total}`);
console.log(`⚠️  Warnings: ${warnings.length}`);
console.log(`🚨 Errors: ${errors.length}`);

// Category breakdown
console.log('\n📁 By Category:');
Object.entries(stats.byCategory)
  .sort((a, b) => b[1] - a[1])
  .forEach(([category, count]) => {
    console.log(`  - ${category}: ${count} workflows`);
  });

// Difficulty breakdown
console.log('\n⚡ By Difficulty:');
Object.entries(stats.byDifficulty)
  .forEach(([difficulty, count]) => {
    const emoji = difficulty === 'beginner' ? '🟢' : difficulty === 'intermediate' ? '🟡' : '🔴';
    console.log(`  ${emoji} ${difficulty}: ${count} workflows`);
  });

// Integration stats
console.log(`\n🔌 Total Integrations: ${stats.totalIntegrations.size} unique services`);
console.log(`🏷️  Average Tags per Workflow: ${(stats.totalTags / stats.total).toFixed(1)}`);

// Print errors
if (errors.length > 0) {
  console.log('\n' + '='.repeat(60));
  console.log('🚨 ERRORS (MUST FIX):');
  console.log('='.repeat(60));
  errors.forEach(err => console.log(`  ❌ ${err}`));
}

// Print warnings
if (warnings.length > 0) {
  console.log('\n' + '='.repeat(60));
  console.log('⚠️  WARNINGS (SHOULD FIX):');
  console.log('='.repeat(60));
  warnings.forEach(warn => console.log(`  ⚠️  ${warn}`));
}

// Summary
console.log('\n' + '='.repeat(60));
if (errors.length === 0) {
  console.log('🎉 All metadata files passed validation!');
  console.log('✅ Ready for front-end integration');
} else {
  console.log(`⚠️  Found ${errors.length} errors that must be fixed`);
  console.log('❌ Not ready for front-end integration');
}
console.log('='.repeat(60) + '\n');

// Generate validation report file
const report = {
  timestamp: new Date().toISOString(),
  summary: {
    totalFiles: stats.total,
    validFiles: stats.valid,
    invalidFiles: stats.invalid,
    errorCount: errors.length,
    warningCount: warnings.length
  },
  stats,
  errors,
  warnings
};

fs.writeFileSync('metadata-validation-report.json', JSON.stringify(report, null, 2));
console.log('📄 Report saved to: metadata-validation-report.json\n');

// Exit with error code if validation failed
process.exit(errors.length > 0 ? 1 : 0);
