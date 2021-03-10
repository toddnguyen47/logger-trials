# VS Code Settings

If using VS Code, go into `.vscode/settings.json` and manually add linters there. I personally used `flake8`, so my sample `settings.json` file looks something like this:

```json
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.flake8Enabled": true,
  "python.linting.flake8Path": "{PATH_TO_PYTHON_INSTALLATION_DIRECTORY}/bin/flake8",
```

I also use `black` as my preferred autoformatter, so I also have this added to my `settings.json`:

```json
"python.formatting.provider": "black"
```
