# Plugin Marketplaces

Create and manage plugin marketplaces for easy plugin discovery and distribution.

## What is a marketplace?

A marketplace is a GitHub repository that contains multiple plugins. It makes it easy for users to discover and install your plugins.

## Creating a marketplace

### Repository structure

```
my-marketplace/
├── plugin1/
│   ├── .claude-plugin/
│   │   └── plugin.json
│   ├── commands/
│   └── agents/
├── plugin2/
│   ├── .claude-plugin/
│   │   └── plugin.json
│   ├── commands/
│   └── agents/
└── README.md
```

### Best practices

1. **Clear organization**: Each plugin in its own directory
2. **Good README**: Document all available plugins
3. **Consistent naming**: Use clear, descriptive plugin names
4. **Version tags**: Tag releases for stability
5. **Categories**: Organize plugins by category

## Adding a marketplace

Users can add your marketplace with:

```bash
/plugin marketplace add owner/repo
```

For example:

```bash
/plugin marketplace add myusername/my-claude-plugins
```

## Installing from a marketplace

Once a marketplace is added, users can install plugins:

```bash
/plugin install plugin-name@marketplace-name
```

The marketplace name is the repository name. For example:

```bash
/plugin marketplace add myusername/my-claude-plugins
/plugin install helpful-plugin@my-claude-plugins
```

## Managing marketplaces

### List marketplaces

```bash
/plugin marketplace list
```

### Remove a marketplace

```bash
/plugin marketplace remove marketplace-name
```

### Update marketplace

Marketplaces are automatically updated when users install or update plugins.

## Example marketplace

Here's a simple example:

**Repository: myusername/dev-tools**

```
dev-tools/
├── code-formatter/
│   ├── .claude-plugin/
│   │   └── plugin.json
│   └── commands/
│       └── format.md
├── test-runner/
│   ├── .claude-plugin/
│   │   └── plugin.json
│   └── commands/
│       └── test.md
└── README.md
```

**README.md:**

```markdown
# Dev Tools Marketplace

A collection of development productivity plugins.

## Available Plugins

### code-formatter
Automatically format code in multiple languages.

Install: `/plugin install code-formatter@dev-tools`

### test-runner
Run tests with smart defaults.

Install: `/plugin install test-runner@dev-tools`

## Installation

1. Add marketplace: `/plugin marketplace add myusername/dev-tools`
2. Install a plugin: `/plugin install plugin-name@dev-tools`
```

## Publishing your marketplace

1. Create a public GitHub repository
2. Add your plugins
3. Write a clear README
4. Tag a release (optional but recommended)
5. Share the repository URL

Users can then add your marketplace and install plugins.

## Marketplace discovery

To help users find your marketplace:

- Use clear, descriptive repository name
- Add relevant topics/tags on GitHub
- Include "claude-code-plugins" or "claude-code-marketplace" topic
- Write comprehensive README
- Share on relevant forums/communities
- Keep plugins updated

## Private marketplaces

Marketplaces can be private repositories. Users will need:

1. GitHub access to the repository
2. Authenticated git access configured
3. Use same commands: `/plugin marketplace add owner/private-repo`

## Best practices

### For marketplace maintainers

- **Test all plugins** before publishing
- **Document clearly** what each plugin does
- **Version carefully** using semantic versioning
- **Respond to issues** from users
- **Keep updated** with Claude Code changes

### For plugin organization

- **One plugin per directory** with clear name
- **Consistent structure** across all plugins
- **Good metadata** in each plugin.json
- **Working examples** in README
- **License information** for each plugin

## Multiple marketplaces

Users can add multiple marketplaces:

```bash
/plugin marketplace add user1/marketplace1
/plugin marketplace add user2/marketplace2

/plugin install tool1@marketplace1
/plugin install tool2@marketplace2
```

Plugin names must be unique within a marketplace but can be the same across different marketplaces.
