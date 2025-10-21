# Plugin Reference

Learn how to create custom slash commands and agents for Claude Code plugins.

## Slash Commands

Slash commands allow you to create custom prompts that can be invoked with a `/` prefix.

### Creating a command

Create a markdown file in the `commands/` directory:

```markdown
---
description: A short description of what this command does
tools: [Bash, Read, Write]  # Optional: limit available tools
---

# Command Instructions

Detailed instructions for what Claude should do when this command is invoked.

You can use markdown formatting, code blocks, and examples.

## Parameters

Commands can accept parameters:

```bash
/my-command param1 param2
```

The parameters will be appended to your prompt.
```

### Command metadata

- `description`: Brief description shown in command lists
- `tools`: Optional array of tool names to restrict Claude's tool usage

### Best practices

- Keep commands focused on a single task
- Provide clear, detailed instructions
- Include examples when helpful
- Use parameters for flexibility

## Agents

Agents are specialized assistants with specific roles and capabilities.

### Creating an agent

Create a markdown file in the `agents/` directory:

```markdown
---
description: A brief description of the agent's role
tools: [Read, Grep, Bash]  # Optional: restrict available tools
---

# Agent Instructions

You are a specialized agent for [specific task].

## Your Role

Detailed description of what this agent does and how it should behave.

## Capabilities

- List key capabilities
- Explain specialized knowledge
- Describe limitations

## Workflow

1. Step-by-step process
2. Decision points
3. Output format
```

### Agent metadata

- `description`: Brief description of agent's purpose
- `tools`: Optional array of tool names available to agent

### Invoking agents

Users can invoke your agent with:

```bash
@agent-name "task description"
```

### Best practices

- Define a clear, focused role
- Specify expertise domain
- Provide workflow guidance
- Set appropriate tool restrictions
- Include examples of good usage

## Tool restrictions

Both commands and agents can restrict which tools are available:

```yaml
---
tools: [Read, Write, Bash]
---
```

Common tools:
- `Read` - Read files
- `Write` - Write files
- `Edit` - Edit files
- `Bash` - Execute shell commands
- `Grep` - Search file contents
- `Glob` - Find files by pattern
- `WebFetch` - Fetch web content
- `WebSearch` - Search the web

## Parameters and arguments

Commands can accept parameters that are appended to the prompt:

```bash
/deploy staging --force
```

The agent receives: "staging --force"

Parse parameters in your instructions:

```markdown
Extract the environment from the first parameter.
If --force flag is present, skip confirmation.
```

## Examples

### Simple command

```markdown
---
description: Format code in the current directory
tools: [Bash, Read]
---

# Format Code

Run the appropriate formatter for all code files in the current directory.

1. Detect the project type
2. Run the standard formatter (prettier, black, rustfmt, etc.)
3. Report which files were formatted
```

### Specialized agent

```markdown
---
description: Expert in database schema design
tools: [Read, Write, Bash]
---

# Database Schema Agent

You are a database design expert specializing in relational database schemas.

## Your Expertise

- Schema normalization
- Index optimization
- Migration strategies
- SQL best practices

## Workflow

1. Analyze requirements
2. Design normalized schema
3. Generate migration SQL
4. Suggest indexes
5. Document relationships
```

## Plugin testing

Test your plugin locally before publishing:

1. Install from local directory: `/plugin install /path/to/plugin`
2. Try all commands and agents
3. Verify tool restrictions work
4. Check error handling
5. Test with different parameters

## Publishing

1. Create a clean repository
2. Add clear README
3. Include usage examples
4. Tag a version release
5. Share repository URL
