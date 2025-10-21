# Plugins

Extend the functionality of Claude Code with plugins.

## What is a plugin?

A plugin allows you to create reusable functionality that can be shared and used across different projects. Plugins can add custom slash commands, agents, and other features to Claude Code.

## Plugin structure

A basic plugin has this structure:

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # Plugin metadata
├── commands/
│   └── my-command.md        # Slash command definitions
└── agents/
    └── my-agent.md          # Agent definitions
```

### Plugin metadata (plugin.json)

The `plugin.json` file contains metadata about your plugin:

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "A helpful plugin",
  "author": {
    "name": "Your Name",
    "email": "your.email@example.com"
  },
  "homepage": "https://github.com/yourusername/my-plugin",
  "repository": "https://github.com/yourusername/my-plugin",
  "license": "MIT",
  "keywords": ["productivity", "automation"],
  "category": "productivity"
}
```

## Installing plugins

### From a marketplace

First, add a marketplace:

```bash
/plugin marketplace add owner/repo
```

Then install a plugin from that marketplace:

```bash
/plugin install plugin-name@marketplace-name
```

### From a local directory

```bash
/plugin install /path/to/plugin
```

### From a git URL

```bash
/plugin install https://github.com/owner/repo
```

## Managing plugins

### List installed plugins

```bash
/plugin list
```

### Update a plugin

```bash
/plugin update plugin-name
```

### Uninstall a plugin

```bash
/plugin uninstall plugin-name
```

## Creating plugins

See the [Plugin Reference](/docs/claude-code/plugins-reference) for details on creating commands and agents.

## Publishing plugins

To share your plugin:

1. Create a GitHub repository
2. Add your plugin files
3. Tag a release
4. Share the repository URL

Users can then install your plugin directly or you can create a marketplace for easier discovery.
