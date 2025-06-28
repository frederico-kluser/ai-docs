# Step-by-Step Guide: Implementing an XMind Generator npm Package

This guide walks through the complete process of implementing a Node.js package that creates XMind mind maps from structured data produced by LLMs. The implementation focuses on creating a clean, predictable API that LLMs can easily work with.

## 1. Project Setup

Start by creating a new npm package with the necessary structure:

```bash
# Create project directory
mkdir llm-xmind-generator
cd llm-xmind-generator

# Initialize npm package
npm init -y

# Create basic folder structure
mkdir -p src/lib src/utils test examples
```

Edit `package.json` to add essential information:

```json
{
  "name": "llm-xmind-generator",
  "version": "0.1.0",
  "description": "Generate XMind mind maps from LLM-structured data",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "scripts": {
    "build": "tsc",
    "test": "jest",
    "lint": "eslint src --ext .ts",
    "prepublishOnly": "npm run build"
  },
  "keywords": ["xmind", "mindmap", "llm", "ai", "generator"],
  "author": "Your Name",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/yourusername/llm-xmind-generator.git"
  }
}
```

## 2. Install Dependencies

Install the required packages for development and XMind file generation:

```bash
# Install xmind-generator (official XMind library)
npm install xmind-generator

# Install development dependencies
npm install --save-dev typescript jest ts-jest @types/node @types/jest eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin
```

## 3. Configure TypeScript

Create a `tsconfig.json` file:

```json
{
  "compilerOptions": {
    "target": "ES2018",
    "module": "CommonJS",
    "declaration": true,
    "outDir": "./dist",
    "strict": true,
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "**/*.test.ts"]
}
```

## 4. Define Core Data Structures

Create `src/types/index.ts` to define the interfaces for LLM-friendly data structures:

```typescript
/**
 * Represents a topic in a mind map
 */
export interface MindMapTopic {
  /** The title/content of the topic */
  title: string;
  /** Optional notes for this topic */
  note?: string;
  /** Optional URL for this topic */
  url?: string;
  /** Optional subtopics/children */
  children?: MindMapTopic[];
  /** Optional labels/markers */
  markers?: string[];
}

/**
 * Top-level structure expected from LLM output
 */
export interface MindMapData {
  /** The central/root topic of the mind map */
  centralTopic: string;
  /** The main topics branching from the central topic */
  mainTopics: MindMapTopic[];
  /** Optional title for the sheet */
  title?: string;
  /** Optional theme for the mind map */
  theme?: string;
}
```

## 5. Implement Core Conversion Logic

Create `src/lib/converter.ts` to transform LLM-structured data to XMind format:

```typescript
import { Topic, RootTopic, Workbook } from 'xmind-generator';
import { MindMapData, MindMapTopic } from '../types';

/**
 * Converts a MindMapTopic to an XMind-generator Topic
 */
function convertTopic(topic: MindMapTopic): any {
  // Create the basic topic with title
  const xmindTopic = Topic(topic.title);
  
  // Add note if provided
  if (topic.note) {
    xmindTopic.note(topic.note);
  }
  
  // Add hyperlink if URL is provided
  if (topic.url) {
    xmindTopic.hyperlink(topic.url);
  }
  
  // Add markers/labels if provided
  if (topic.markers && topic.markers.length > 0) {
    topic.markers.forEach(marker => {
      xmindTopic.marker(marker);
    });
  }
  
  // Recursively process children if they exist
  if (topic.children && topic.children.length > 0) {
    xmindTopic.children(
      topic.children.map(child => convertTopic(child))
    );
  }
  
  return xmindTopic;
}

/**
 * Converts LLM-friendly mind map data to XMind workbook format
 */
export function convertToXmind(data: MindMapData): any {
  // Create the root topic
  const rootTopic = RootTopic(data.centralTopic)
    .children(
      data.mainTopics.map(topic => convertTopic(topic))
    );
  
  // Create the workbook with the root topic
  const workbook = Workbook(rootTopic);
  
  // Apply theme if specified
  if (data.theme) {
    workbook.theme(data.theme);
  }
  
  return workbook;
}
```

## 6. Create Main Export File

Create `src/index.ts` to export the public API:

```typescript
import { writeLocalFile } from 'xmind-generator';
import { convertToXmind } from './lib/converter';
import { MindMapData, MindMapTopic } from './types';

/**
 * Generates an XMind file from LLM-structured data
 * 
 * @param data The mind map data structure
 * @param outputPath The path where the XMind file will be saved
 * @returns Promise that resolves when the file is written
 */
export async function generateXmindFile(data: MindMapData, outputPath: string): Promise<void> {
  const workbook = convertToXmind(data);
  return writeLocalFile(workbook, outputPath);
}

/**
 * Creates a mind map data structure from a central topic and main topics
 * (Helper function for easier creation)
 */
export function createMindMapData(
  centralTopic: string, 
  mainTopics: MindMapTopic[],
  options?: { title?: string, theme?: string }
): MindMapData {
  return {
    centralTopic,
    mainTopics,
    title: options?.title,
    theme: options?.theme
  };
}

// Re-export types for consumers
export { MindMapData, MindMapTopic };

// Default export for convenience
export default {
  generateXmindFile,
  createMindMapData
};
```

## 7. Add Utility Functions

Create `src/utils/validators.ts` for data validation:

```typescript
import { MindMapData, MindMapTopic } from '../types';

/**
 * Validates a mind map topic structure
 */
export function validateTopic(topic: MindMapTopic): boolean {
  // Title is required
  if (!topic.title || topic.title.trim() === '') {
    return false;
  }
  
  // Validate children recursively if they exist
  if (topic.children && topic.children.length > 0) {
    return topic.children.every(child => validateTopic(child));
  }
  
  return true;
}

/**
 * Validates the complete mind map data structure
 */
export function validateMindMapData(data: MindMapData): boolean {
  // Central topic is required
  if (!data.centralTopic || data.centralTopic.trim() === '') {
    return false;
  }
  
  // Main topics array is required and should not be empty
  if (!data.mainTopics || !Array.isArray(data.mainTopics) || data.mainTopics.length === 0) {
    return false;
  }
  
  // Validate each main topic
  return data.mainTopics.every(topic => validateTopic(topic));
}
```

Add these validations to the main generation function in `src/index.ts`:

```typescript
import { validateMindMapData } from './utils/validators';

export async function generateXmindFile(data: MindMapData, outputPath: string): Promise<void> {
  // Validate input data
  if (!validateMindMapData(data)) {
    throw new Error('Invalid mind map data structure');
  }
  
  const workbook = convertToXmind(data);
  return writeLocalFile(workbook, outputPath);
}
```

## 8. Create Example File

Create an example in `examples/simple.js`:

```javascript
const { generateXmindFile, createMindMapData } = require('../dist');

// Example data that could come from an LLM
const mindMapData = createMindMapData(
  'Prompt Engineering Principles',
  [
    {
      title: 'Context Details',
      children: [
        { title: 'Project specifications' },
        { title: 'Technical limitations' },
        { title: 'Use cases' }
      ]
    },
    {
      title: 'Problem Decomposition',
      children: [
        { title: 'Break into subtasks' },
        { title: 'Identify dependencies' }
      ]
    },
    {
      title: 'Structured Thinking',
      children: [
        { title: 'Step-by-step reasoning' },
        { title: 'Consider edge cases' }
      ]
    },
    {
      title: 'Verification',
      children: [
        { title: 'Test with examples' },
        { title: 'Validate outputs' }
      ]
    }
  ],
  { theme: 'classic' }
);

// Generate the XMind file
generateXmindFile(mindMapData, 'prompt-engineering.xmind')
  .then(() => console.log('Mind map generated successfully!'))
  .catch(err => console.error('Error generating mind map:', err));
```

## 9. Create Tests

Set up Jest for testing in `jest.config.js`:

```javascript
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  testMatch: ['**/*.test.ts'],
};
```

Create a basic test file in `test/converter.test.ts`:

```typescript
import { convertToXmind } from '../src/lib/converter';
import { MindMapData } from '../src/types';

describe('XMind Converter', () => {
  it('should convert simple mind map data to XMind format', () => {
    // Arrange
    const data: MindMapData = {
      centralTopic: 'Test Topic',
      mainTopics: [
        { title: 'Topic 1' },
        { 
          title: 'Topic 2',
          children: [
            { title: 'Subtopic 2.1' }
          ]
        }
      ]
    };
    
    // Act
    const result = convertToXmind(data);
    
    // Assert
    expect(result).toBeDefined();
    expect(result.root.title).toBe('Test Topic');
    expect(result.root.children.length).toBe(2);
    expect(result.root.children[1].children.length).toBe(1);
  });
});
```

## 10. Create Documentation

Create a comprehensive README.md file:

```markdown
# LLM XMind Generator

Generate XMind mind maps from structured data produced by Large Language Models (LLMs).

## Installation

```bash
npm install llm-xmind-generator
```

## Usage

```javascript
const { generateXmindFile, createMindMapData } = require('llm-xmind-generator');

// Create mind map data (this could come from an LLM)
const mindMapData = createMindMapData(
  'Central Topic',
  [
    {
      title: 'Main Topic 1',
      children: [
        { title: 'Subtopic 1.1' },
        { title: 'Subtopic 1.2' }
      ]
    },
    {
      title: 'Main Topic 2',
      note: 'This is an important topic',
      url: 'https://example.com',
      children: [
        { title: 'Subtopic 2.1' }
      ]
    }
  ],
  { theme: 'classic' }
);

// Generate the XMind file
generateXmindFile(mindMapData, 'output.xmind')
  .then(() => console.log('Mind map generated successfully!'))
  .catch(err => console.error('Error:', err));
```

## Data Structure

The library accepts a simple, predictable structure that LLMs can easily generate:

```typescript
interface MindMapData {
  centralTopic: string;
  mainTopics: MindMapTopic[];
  title?: string;
  theme?: string;
}

interface MindMapTopic {
  title: string;
  note?: string;
  url?: string;
  children?: MindMapTopic[];
  markers?: string[];
}
```

## LLM Integration

This library is designed to work seamlessly with LLM outputs. Here's an example prompt to generate compatible data:

```
Generate a mind map about [TOPIC] in the following JSON format:
{
  "centralTopic": "Main Topic",
  "mainTopics": [
    {
      "title": "Subtopic 1",
      "children": [
        {"title": "Detail 1.1"},
        {"title": "Detail 1.2"}
      ]
    },
    {
      "title": "Subtopic 2",
      "children": [
        {"title": "Detail 2.1"}
      ]
    }
  ]
}
```

## License

MIT
```

## 11. Build and Test the Package

Run the build and test processes:

```bash
# Build the TypeScript code
npm run build

# Run tests
npm test

# Try the example
node examples/simple.js
```

## 12. Publishing the Package

When ready to publish:

```bash
# First time setup
npm login

# Publish the package
npm publish
```

## Implementation Tips

1. **Predictable Input Format**: Keep the input format simple and predictable for LLMs to generate.

2. **Validation**: Always validate input data to prevent unexpected errors.

3. **Clear Documentation**: Document the expected input format thoroughly, with examples.

4. **Error Handling**: Implement proper error handling to make debugging easier.

5. **Progressive Enhancement**: Start with a minimal implementation that handles basic mind maps, then add support for advanced features.

6. **Testing**: Create tests with diverse data structures to ensure robustness.

This implementation provides a clean, predictable API that LLMs can easily work with, enabling seamless integration between language models and mind map generation.