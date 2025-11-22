#!/usr/bin/env node

/**
 * Workflow Index Generator
 * Aggregates all metadata files into a single searchable index for front-end
 */

const fs = require('fs');
const path = require('path');
const glob = require('glob');

console.log('🔨 Generating workflow index...\n');

// Find all metadata files
const metadataFiles = glob.sync('workflows/**/*-metadata.json', { cwd: process.cwd() });
console.log(`Found ${metadataFiles.length} metadata files\n`);

const workflows = [];
const categories = {};
const tags = {};
const integrations = {};
const difficulties = { beginner: 0, intermediate: 0, advanced: 0 };

// Process each metadata file
metadataFiles.forEach((file, index) => {
  console.log(`[${index + 1}/${metadataFiles.length}] Processing ${file}...`);

  try {
    const data = JSON.parse(fs.readFileSync(file, 'utf8'));

    // Generate workflow ID from filename
    const workflowId = path.basename(file, '-metadata.json');
    const workflowJsonFile = file.replace('-metadata.json', '.json');

    // Extract category info
    const categoryName = data.category || 'Uncategorized';
    const subcategoryName = data.subcategory || 'General';

    // Build workflow entry for index
    const workflowEntry = {
      id: workflowId,
      name: data.name,
      description: data.description,
      category: categoryName,
      subcategory: subcategoryName,
      difficulty: data.difficulty ? data.difficulty.toLowerCase() : 'intermediate',
      tags: data.tags || [],
      integrations: data.integrations || [],
      triggerType: data.triggerType || 'Manual',
      setupTime: data.estimatedSetupTime || 'Unknown',
      cost: data.pricing?.estimatedMonthlyCost || 'Unknown',
      version: data.version || '1.0.0',
      author: data.author || 'Unknown',
      lastUpdated: data.lastUpdated || new Date().toISOString().split('T')[0],
      fileUrl: `/${workflowJsonFile}`,
      metadataUrl: `/${file}`,
      useCase: data.useCase || data.description || '',
      features: Array.isArray(data.features) ? data.features : Object.values(data.features || {}),
      requirements: data.requirements || []
    };

    workflows.push(workflowEntry);

    // Update categories stats
    if (!categories[categoryName]) {
      categories[categoryName] = {
        name: categoryName,
        count: 0,
        subcategories: {}
      };
    }
    categories[categoryName].count++;

    if (!categories[categoryName].subcategories[subcategoryName]) {
      categories[categoryName].subcategories[subcategoryName] = {
        name: subcategoryName,
        count: 0
      };
    }
    categories[categoryName].subcategories[subcategoryName].count++;

    // Update tags stats
    if (data.tags) {
      data.tags.forEach(tag => {
        tags[tag] = (tags[tag] || 0) + 1;
      });
    }

    // Update integrations stats
    if (data.integrations) {
      data.integrations.forEach(integration => {
        integrations[integration] = (integrations[integration] || 0) + 1;
      });
    }

    // Update difficulty stats
    if (data.difficulty) {
      const diff = data.difficulty.toLowerCase();
      if (difficulties.hasOwnProperty(diff)) {
        difficulties[diff]++;
      }
    }

  } catch (err) {
    console.error(`  ❌ Error processing ${file}: ${err.message}`);
  }
});

// Sort and format categories
const categoriesArray = Object.values(categories).map(cat => ({
  name: cat.name,
  count: cat.count,
  subcategories: Object.values(cat.subcategories).sort((a, b) => b.count - a.count)
})).sort((a, b) => b.count - a.count);

// Sort and format tags (top 50)
const popularTags = Object.entries(tags)
  .map(([tag, count]) => ({ tag, count }))
  .sort((a, b) => b.count - a.count)
  .slice(0, 50);

// Sort and format integrations
const integrationsArray = Object.entries(integrations)
  .map(([name, count]) => ({ name, count }))
  .sort((a, b) => b.count - a.count);

// Build final index
const workflowIndex = {
  version: '1.0.0',
  generatedAt: new Date().toISOString(),
  totalWorkflows: workflows.length,
  categories: categoriesArray,
  popularTags,
  integrations: integrationsArray,
  difficulties: {
    beginner: difficulties.beginner,
    intermediate: difficulties.intermediate,
    advanced: difficulties.advanced
  },
  workflows: workflows.sort((a, b) => a.name.localeCompare(b.name))
};

// Save to file
const outputFile = 'workflow-index.json';
fs.writeFileSync(outputFile, JSON.stringify(workflowIndex, null, 2));

// Print summary
console.log('\n' + '='.repeat(60));
console.log('✅ WORKFLOW INDEX GENERATED');
console.log('='.repeat(60));
console.log(`\n📊 Total Workflows: ${workflowIndex.totalWorkflows}`);
console.log(`📁 Categories: ${categoriesArray.length}`);
console.log(`🏷️  Unique Tags: ${Object.keys(tags).length}`);
console.log(`🔌 Integrations: ${integrationsArray.length}`);

console.log('\n📁 Workflows by Category:');
categoriesArray.forEach(cat => {
  console.log(`  - ${cat.name}: ${cat.count} workflows`);
  cat.subcategories.forEach(sub => {
    console.log(`    └─ ${sub.name}: ${sub.count}`);
  });
});

console.log('\n⚡ Workflows by Difficulty:');
console.log(`  🟢 Beginner: ${difficulties.beginner} (${(difficulties.beginner / workflows.length * 100).toFixed(1)}%)`);
console.log(`  🟡 Intermediate: ${difficulties.intermediate} (${(difficulties.intermediate / workflows.length * 100).toFixed(1)}%)`);
console.log(`  🔴 Advanced: ${difficulties.advanced} (${(difficulties.advanced / workflows.length * 100).toFixed(1)}%)`);

console.log('\n🔥 Top 10 Tags:');
popularTags.slice(0, 10).forEach((tag, index) => {
  console.log(`  ${index + 1}. ${tag.tag} (${tag.count})`);
});

console.log('\n🔌 Top 10 Integrations:');
integrationsArray.slice(0, 10).forEach((integration, index) => {
  console.log(`  ${index + 1}. ${integration.name} (${integration.count})`);
});

console.log('\n' + '='.repeat(60));
console.log(`💾 Index saved to: ${outputFile}`);
console.log('🚀 Ready for front-end integration!');
console.log('='.repeat(60) + '\n');

// Also generate a minified version for production
const minifiedFile = 'workflow-index.min.json';
fs.writeFileSync(minifiedFile, JSON.stringify(workflowIndex));
console.log(`📦 Minified version saved to: ${minifiedFile}\n`);
