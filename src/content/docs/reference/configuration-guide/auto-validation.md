---
title: Config Auto-Validation
description: Automatically validate configuration on startup.
sidebar:
  order: 6

---


## Automatic Configuration Validation

go-zero now supports automatic configuration validation through a simple interface implementation. This feature is particularly useful when you need to ensure your configuration values meet certain criteria before your application starts.

## How It Works

The new feature introduces a validation mechanism that automatically checks your configuration after loading. Here's how you can use it:

1. Implement the `Validator` interface in your configuration struct:

```go
type YourConfig struct {
    Name     string
    MaxUsers int
}

// Implement the Validator interface
func (c YourConfig) Validate() error {
    if len(c.Name) == 0 {
        return errors.New("name cannot be empty")
    }
    if c.MaxUsers <= 0 {
        return errors.New("max users must be positive")
    }
    return nil
}
```

2. Use the configuration as usual - validation happens automatically:

```go
var config YourConfig
err := conf.Load("config.yaml", &config)
if err != nil {
    // This will catch both loading errors AND validation errors
    log.Fatal(err)
}
```

## Key Benefits

1. **Early Error Detection**: Configuration errors are caught immediately during application startup
2. **Custom Validation Rules**: Define your own validation logic specific to your application needs
3. **Clean Integration**: No additional function calls needed - validation happens automatically after loading
4. **Type Safety**: Validation is tied to your configuration structs

## Example Use Cases

Here's a practical example of how you might use this feature:

```go
type DatabaseConfig struct {
    Host     string
    Port     int
    MaxConns int
}

func (c DatabaseConfig) Validate() error {
    if len(c.Host) == 0 {
        return errors.New("database host cannot be empty")
    }
    if c.Port <= 0 || c.Port > 65535 {
        return errors.New("invalid port number")
    }
    if c.MaxConns <= 0 {
        return errors.New("max connections must be positive")
    }
    return nil
}
```

## Implementation Details

The feature works by checking if your configuration type implements the `Validator` interface after loading the configuration values. If the interface is implemented, the validation is automatically performed. This approach maintains backward compatibility while providing enhanced functionality for new code.

## Getting Started

To use this feature, simply update to the latest version of go-zero. No additional dependencies are required. The validation will work with all existing configuration loading methods including JSON, YAML, and TOML formats.

## Best Practices

1. Keep validation rules simple and focused on configuration validity
2. Use clear error messages that indicate exactly what's wrong
3. Consider adding validation for all critical configuration values
4. Remember that validation runs at startup - avoid expensive operations