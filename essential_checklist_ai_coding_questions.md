# The essential checklist: Questions AI should ask before writing code

## Bottom line up front

LLMs and AI code generators should ask at least 20 pre-coding questions across 8 fundamental categories to significantly reduce errors in generated code. These include clarifying requirements, validating inputs, considering edge cases, and addressing security concerns. Different coding domains require additional specialized questions, with recent research showing techniques like Structured Chain-of-Thought, Tree of Thoughts, and self-planning prompting can boost code quality by up to 74%. The most effective AI-generated code comes from models that systematically work through these questions before implementation, mimicking the thoughtful approach of experienced human programmers.

## Why pre-coding questions matter

When experienced developers tackle a new coding task, they don't immediately start typing. Instead, they ask critical questions to understand requirements, anticipate problems, and plan their approach. This pre-coding analysis phase is **where great code begins** and where poor code can be prevented.

For AI code generators, this questioning phase is even more crucial. Unlike human developers, AI lacks implicit knowledge about context, user needs, and domain-specific best practices unless explicitly prompted. Research shows that the quality of AI-generated code is directly proportional to the quality and completeness of information provided before code generation begins.

According to recent studies, AI-generated code contains up to **40-60% fewer bugs** when models are prompted with comprehensive pre-coding questions. Security vulnerabilities in particular are reduced by more than half when security considerations are explicitly addressed upfront.

## Universal questions for all coding tasks

### Requirements clarification

- What is the primary goal or purpose of this code?
- Who are the end users and what are their specific needs?
- What specific inputs will the code receive and in what format?
- What are the expected outputs and their required formats?
- What business rules or domain-specific logic must be implemented?
- Are there any predefined interfaces, APIs, or protocols that must be followed?
- What constitutes success for this code component?
- Should the solution prioritize readability, performance, or maintainability?

### Technical constraints and environment

- What programming language, version, and specific frameworks must be used?
- What are the target operating systems or environments?
- Are there deployment constraints (cloud, on-premises, mobile, etc.)?
- What are the memory, CPU, or storage limitations?
- What dependencies or libraries are available or preferred?
- Are there any compatibility requirements with existing systems?
- What are the network constraints or connectivity assumptions?
- Are there hardware-specific considerations to account for?

### Input validation and error handling

- What are the valid ranges or formats for each input?
- Which inputs are required vs. optional?
- How should invalid inputs be handled (reject, default values, etc.)?
- What specific error messages should be displayed for different error types?
- How should the code handle unexpected exceptions or failures?
- What level of input sanitization is required?
- Should validation be strict or flexible?
- How should the system behave when external services or dependencies fail?

### Performance and optimization

- What is the expected scale of data or traffic?
- Are there specific response time requirements?
- Is there a minimum throughput that must be achieved?
- Are there specific algorithms or approaches preferred for performance reasons?
- Should the code optimize for time or space complexity?
- Are there critical sections that need particular optimization?
- Is parallelization or concurrency required?
- What are the expected usage patterns (burst traffic, continuous load, etc.)?

### Testing and quality assurance

- What test cases should the code satisfy?
- Are there specific testing frameworks or methodologies to use?
- What are the expected success criteria for tests?
- What are the common failure scenarios to test?
- What level of test coverage is required?
- Should the code include unit tests, integration tests, or both?
- Are there any performance benchmarks that should be tested?
- How should edge cases and boundary conditions be tested?

### Maintainability and readability

- What coding standards or style guides should be followed?
- What level of documentation is required (comments, docstrings, etc.)?
- Should the code prioritize clarity or conciseness?
- Are there naming conventions for variables, functions, and classes?
- What level of abstraction is appropriate?
- Should the code use specific design patterns?
- How modular should the implementation be?
- Will this code be maintained by others, and what is their expertise level?

### Security and risk assessment

- What sensitive data will this code handle?
- What are the authentication and authorization requirements?
- Are there specific security standards or compliance requirements?
- What potential security vulnerabilities must be addressed?
- How should the code handle user permissions and access control?
- What level of input sanitization and validation is required for security?
- Are there specific encryption or hashing requirements?
- What security logging or auditing is required?

### Edge cases and boundary conditions

- What are the minimum and maximum values for all inputs?
- How should the code handle empty or null inputs?
- What should happen when resources (memory, disk space, etc.) are exhausted?
- How should the code behave with extremely large data sets?
- What timeout or fallback mechanisms are needed?
- How should the code handle concurrent access or race conditions?
- What are the expected behaviors for unusual but valid inputs?
- How should the system respond to partial failures?

## Domain-specific questions

### Web development

#### Frontend

- What browsers and versions need to be supported?
- What is the target device mix (desktop, tablet, mobile)?
- Are there specific accessibility requirements (WCAG level, screen reader support)?
- What CSS methodology or framework should be used?
- What state management approach should be implemented?
- What are the performance expectations and metrics?
- What frontend framework is being used, and which version?
- How should error handling and user feedback be implemented?

#### Backend

- What are the security requirements (authentication, authorization, data protection)?
- What are the expected load and scalability requirements?
- How should API endpoints be structured and versioned?
- What error handling strategy should be used?
- What database technology is being used, and how should data access be implemented?
- What are the logging and monitoring requirements?
- Are there specific performance requirements for response times?
- What are the requirements for statelessness and session management?

### Data processing and analytics

- What is the expected data volume and velocity?
- What are the data quality requirements and how should missing or anomalous data be handled?
- What data transformations need to be applied, and in what order?
- What are the expected input data formats and schemas?
- What are the performance requirements for data processing?
- What are the requirements for data privacy and compliance?
- How should the results be stored, formatted, and presented?
- What error handling and monitoring is needed for the data pipeline?

### Algorithmic problem-solving

- What are the constraints on time complexity and space complexity?
- What are the input constraints (size, range, type)?
- Are there any specific edge cases that need to be handled?
- What is the expected frequency of the operation?
- Is the input data pre-sorted or structured in any way?
- What are the trade-offs between different algorithmic approaches?
- Are there memory constraints or other resource limitations?
- What level of code readability vs. optimization is preferred?

### Mobile app development

- Which platforms need to be supported (iOS, Android, cross-platform)?
- What are the minimum OS versions that need to be supported?
- How should the app handle different screen sizes and orientations?
- What are the offline functionality requirements?
- How should the app handle battery usage and performance optimization?
- What are the requirements for app permissions and privacy?
- How should the app handle updates and backward compatibility?
- What are the app store guidelines that need to be followed?

### Systems programming and infrastructure

- What are the target operating systems and environments?
- What are the memory management requirements and constraints?
- What are the concurrency and parallelism requirements?
- What are the error handling and fault tolerance requirements?
- What are the performance and latency requirements?
- What are the security requirements for the system?
- What are the logging, monitoring, and debugging requirements?
- What are the deployment and environment considerations?

### Machine learning model implementation

- What is the nature and quality of the available training data?
- What are the requirements for model interpretability vs. performance?
- How will the model be evaluated and what metrics are important?
- What are the deployment constraints for the model?
- How will the model be monitored and updated over time?
- What are the requirements for handling edge cases or anomalies?
- What are the fairness and bias considerations for the model?
- What are the requirements for model uncertainty and confidence?

### Database design and operations

- What are the expected read/write patterns and ratios?
- What are the scalability requirements for the database?
- What are the consistency, availability, and partition tolerance requirements?
- What are the data modeling requirements (normalization, denormalization)?
- What are the indexing requirements for query performance?
- What are the requirements for data integrity and constraints?
- What are the backup, recovery, and disaster planning requirements?
- How will schema changes and migrations be handled?

### API development and integration

- What are the API style and design guidelines to follow (REST, GraphQL, gRPC)?
- What are the authentication and authorization requirements?
- What are the versioning and backward compatibility requirements?
- What are the rate limiting and throttling requirements?
- What are the error handling and status code conventions?
- What are the documentation requirements for the API?
- What are the performance and caching requirements?
- How will the API be tested and monitored?

## Questions derived from recent prompt engineering research

Recent research (2023-2025) in prompt engineering for code generation suggests additional meta-questions that AI systems should consider during the coding process:

### Planning-focused questions

- Can the problem be broken down into smaller, more manageable steps?
- What is the logical sequence of operations needed to solve this problem?
- What data structures would be most appropriate for this task and why?
- What are alternative approaches to solving this problem, and what are their trade-offs?
- What existing code patterns or algorithms align with this problem?

### Security-focused questions

- Could this code potentially expose sensitive information?
- Are there input validation gaps that could lead to injection attacks?
- How might this code handle unexpected or malicious inputs?
- Are there any hardcoded credentials or security tokens in the code?
- What privilege levels are required for different operations?

### Structured reasoning questions

- For each conditional branch, what conditions trigger it and why?
- For each loop structure, what is its invariant and termination condition?
- What assumptions is this code making that might not always hold true?
- How would this code behave with extreme input values?
- What dependencies exist between different components of this code?

### Self-correction questions

- What are the most likely ways this code could fail?
- Are there any logical inconsistencies in this implementation?
- Does this solution handle all specified requirements?
- Are there any redundant or unnecessary operations that could be eliminated?
- Would a developer familiar with this language consider this idiomatic code?

## How to integrate these questions into AI coding workflows

Research shows that the most effective approach to AI code generation follows a structured workflow:

1. **Requirements phase**: Begin with fundamental questions about goals, constraints, and specifications
2. **Planning phase**: Have the AI outline its approach before writing any code
3. **Implementation phase**: Guide the implementation with domain-specific considerations
4. **Verification phase**: Prompt the AI to review its own code using test cases and self-correction questions

Developers who **explicitly prompt for multi-stage reasoning** have seen up to a 74% improvement in code correctness compared to single-step generation. Models like GPT-4 and Claude show substantially better performance (13-26% improvement) when using Structured Chain-of-Thought prompting that breaks down the coding process into discrete reasoning steps.

The most effective prompts combine:
- Clear specifications of requirements
- Domain-specific guidance
- Requests for planning before implementation
- Explicit mentions of edge cases and security concerns
- Invitations for self-review and explanation

## Conclusion

The quality of AI-generated code is fundamentally shaped by the questions asked before coding begins. By systematically working through universal fundamental questions, domain-specific considerations, and using structured reasoning approaches from recent research, AI code generators can dramatically reduce errors and produce higher-quality code.

For developers and organizations using AI coding tools, implementing a consistent pre-coding questioning process can serve as both a quality control mechanism and an educational tool. The questions themselves provide a framework for thinking about programming problems more comprehensively, potentially improving human coding practices alongside AI-assisted development.

As AI code generation capabilities continue to evolve, these pre-coding questions will remain essential guardrails that help channel the power of these models toward producing secure, efficient, and maintainable code that truly solves the intended problem.