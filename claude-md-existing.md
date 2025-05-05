# CLAUDE.md

This file provides guidance to Claude Code when working with this existing codebase, helping to maintain architectural consistency and follow established patterns.

## Codebase Overview

[Brief description of the project, its purpose, and current architecture]

## Architectural Approach

The project follows [architecture style: microservices, monolith, etc.] with the following key components:

- **Frontend**: [Current frontend technologies]
- **Backend**: [Current backend technologies]
- **Database**: [Current database technologies]
- **Infrastructure**: [Current deployment, CI/CD approach]

## Core Principles

When working with this codebase:

1. **Preserve existing patterns** - Follow established conventions even if they differ from your preferences
2. **Incremental evolution** - Make small, targeted changes rather than large-scale refactoring
3. **Respect boundaries** - Maintain separation between components as currently defined
4. **Compatibility first** - Ensure changes don't break existing functionality
5. **Test coverage** - Maintain or improve test coverage with any changes

## Code Style Guide

### Formatting
- Indentation: [tabs/spaces and size]
- Line length: [maximum characters]
- Whitespace conventions: [details]
- End of line: [LF/CRLF]

### Naming Conventions
- Files: [conventions]
- Classes/Interfaces: [conventions]
- Functions/Methods: [conventions]
- Variables: [conventions]
- Constants: [conventions]

## Project Structure

```
# Current project structure - modify to match actual structure
src/
├── [directory]/     # [purpose]
├── [directory]/     # [purpose]
└── [directory]/     # [purpose]
```

## Existing Patterns to Follow

### Component Pattern

```typescript
// Example of existing component pattern
class ExampleComponent {
  constructor(private dependency: Dependency) {
    // Initialization
  }
  
  public method(): void {
    // Implementation
  }
}
```

### Error Handling Pattern

```typescript
// Example of existing error handling pattern
try {
  // Operation
} catch (error) {
  logger.error('Error message', { error });
  throw new CustomError('User-friendly message', error);
}
```

### API Pattern

```typescript
// Example of existing API pattern
@Controller('resource')
export class ResourceController {
  constructor(private service: ResourceService) {}
  
  @Get(':id')
  async getResource(@Param('id') id: string): Promise<Resource> {
    return this.service.findById(id);
  }
}
```

## Known Technical Debt Areas

This section highlights areas that require special care:

1. **[Component/Module Name]**
   - Issues: [description of issues]
   - Approach: [how to handle changes in this area]

2. **[Component/Module Name]**
   - Issues: [description of issues]
   - Approach: [how to handle changes in this area]

## Legacy Code Guidelines

Some parts of the codebase are considered legacy and should be treated carefully:

- **[Legacy Area]**: [special considerations]
- **[Legacy Area]**: [special considerations]

When working with legacy code:
1. Add tests before making changes whenever possible
2. Make minimal changes to achieve the goal
3. Document workarounds clearly with comments
4. Don't modernize surrounding code unless specifically requested

## Common Development Commands

```bash
# Install dependencies
[command]

# Start development server
[command]

# Run tests
[command]

# Build for production
[command]

# Other common commands
[command]
```

## Database Schema Guidelines

- Follow existing table naming conventions
- Use foreign key constraints consistently
- Document all schema changes
- Create database migrations for all changes
- Follow the existing indexing strategy

## API Documentation

The API is documented using [documentation approach]. When making changes:

- Update documentation to match implementation
- Follow the existing format for consistency
- Include examples for new endpoints
- Document error responses

## Testing Strategy

- **Unit Tests**: Focus on business logic components
- **Integration Tests**: Test API endpoints and service interactions
- **E2E Tests**: Verify critical user journeys
- **Test Coverage**: Maintain minimum coverage of [percentage]

## Refactoring Guidelines

When refactoring existing code:

1. Establish test coverage first
2. Make small, incremental changes
3. Run tests after each significant change
4. Maintain backward compatibility
5. Follow existing patterns even if not ideal
6. Document the reasoning behind changes
7. Separate refactoring commits from feature commits

## Instructions for Research and External Resources

Claude, when you need to access external resources or research information:

1. ALWAYS FIRST add the URL temporarily to this CLAUDE.md file under "Authorized URLs"
2. Use WebFetchTool ONLY after adding the URL
3. Remove the URL from the list after completing the research
4. Never access URLs not explicitly authorized through this process

### Authorized URLs
- https://api.duckduckgo.com

## Deployment Process

The deployment process involves:

1. [Description of CI/CD pipeline]
2. [Description of environments]
3. [Description of release process]

## Contact Information

For questions about this codebase, contact [team email or contact information].

---
Last updated: May 05, 2025