---
title: MCP 서버
description: go-zero의 MCP 서버에 대해 설명합니다.
sidebar:
  order: 2
---


## 개요

이 패키지는 Go로 Model Context Protocol(MCP) 서버 사양을 구현합니다. Server-Sent Events(SSE)를 사용해 AI 모델과 client 사이의 실시간 통신을 제공하며, 양방향 통신이 필요한 AI 지원 애플리케이션을 표준 MCP 방식으로 만들 수 있게 합니다.

## 핵심 컴포넌트

### Server-Sent Events(SSE) 통신

- **실시간 통신**: client와 persistent connection을 유지하는 견고한 SSE 기반 통신 시스템
- **연결 관리**: client 등록, 메시지 broadcast, client 정리 메커니즘
- **이벤트 처리**: tools, prompts, resources 변경을 위한 이벤트 타입

### JSON-RPC 구현

- **요청 처리**: MCP protocol 메서드를 처리하는 완전한 JSON-RPC request processor
- **응답 포맷팅**: JSON-RPC 사양에 맞는 응답 포맷팅
- **오류 처리**: 적절한 오류 코드와 함께 제공되는 포괄적인 오류 처리

### 도구 관리

- **도구 등록**: handler와 함께 사용자 정의 도구를 등록하는 시스템
- **도구 실행**: timeout 처리를 포함해 도구 함수를 실행하는 메커니즘
- **결과 처리**: 문자열, JSON, 이미지 등 다양한 반환 타입을 지원하는 유연한 결과 처리

### Prompt 시스템

- **Prompt 등록**: 정적 prompt와 동적 prompt를 모두 등록하는 시스템
- **인자 검증**: 필수 인자와 선택 인자의 기본값 검증
- **메시지 생성**: 올바른 형식의 대화 메시지를 생성하는 handler

### 리소스 관리

- **리소스 등록**: 외부 리소스를 관리하고 접근하는 시스템
- **콘텐츠 전달**: client 요청 시 리소스 콘텐츠를 전달하는 handler
- **리소스 구독**: client가 리소스 업데이트를 구독하는 메커니즘

### Protocol 기능

- **초기화 순서**: capability negotiation을 포함한 올바른 handshaking
- **알림 처리**: 표준 알림과 client별 알림 모두 지원
- **메시지 라우팅**: 요청을 적절한 handler로 전달하는 지능형 라우팅

## 기술적 특징

### 설정 시스템

- **유연한 설정**: 합리적인 기본값과 커스터마이징 옵션을 제공하는 설정 시스템
- **CORS 지원**: 교차 출처 요청을 위한 CORS 설정
- **서버 정보**: 서버 식별과 버전 정보를 올바르게 제공

### client session 관리

- **세션 추적**: 고유 식별자 기반 client session 추적
- **연결 상태 확인**: 연결 상태를 유지하기 위한 ping/pong 메커니즘
- **초기화 상태**: client 초기화 상태 추적

### 콘텐츠 처리

- **다중 형식 콘텐츠**: text, code, binary content 지원
- **MIME 타입 지원**: 다양한 콘텐츠 타입에 맞는 MIME 타입 식별
- **대상 주석**: user/assistant target을 지정하기 위한 content audience annotation

## 사용법

### MCP 서버 설정

MCP 서버를 만들고 시작하려면 다음처럼 작성합니다.

```go
package main

import (
	"github.com/zeromicro/go-zero/core/conf"
	"github.com/zeromicro/go-zero/core/logx"
	"github.com/zeromicro/go-zero/mcp"
)

func main() {
	// YAML 파일에서 설정을 로드합니다
	var c mcp.McpConf
	conf.MustLoad("config.yaml", &c)

	// 선택 사항: 통계 로그를 비활성화합니다
	logx.DisableStat()

	// MCP 서버를 생성합니다
	server := mcp.NewMcpServer(c)

	// 도구, prompt, 리소스를 등록합니다(아래 예제 참고)

	// 서버를 시작하고 종료 시 중지되도록 보장합니다
	defer server.Stop()
	server.Start()
}
```

샘플 설정 파일(`config.yaml`):

```yaml
name: mcp-server
host: localhost
port: 8080
mcp:
  name: my-mcp-server
  messageTimeout: 30s # 도구 호출 timeout
  cors:
    - http://localhost:3000 # 선택 사항: CORS 설정
```

### 도구 등록

도구를 사용하면 AI 모델이 MCP protocol을 통해 사용자 정의 코드를 실행할 수 있습니다.

#### 기본 도구 예제:

```go
// 간단한 echo 도구를 등록합니다
echoTool := mcp.Tool{
	Name:        "echo",
	Description: "Echoes back the message provided by the user",
	InputSchema: mcp.InputSchema{
		Properties: map[string]any{
			"message": map[string]any{
				"type":        "string",
				"description": "The message to echo back",
			},
			"prefix": map[string]any{
				"type":        "string",
				"description": "Optional prefix to add to the echoed message",
				"default":     "Echo: ",
			},
		},
		Required: []string{"message"},
	},
	Handler: func(ctx context.Context, params map[string]any) (any, error) {
		var req struct {
			Message string `json:"message"`
			Prefix  string `json:"prefix,optional"`
		}

		if err := mcp.ParseArguments(params, &req); err != nil {
			return nil, fmt.Errorf("failed to parse params: %w", err)
		}

		prefix := "Echo: "
		if len(req.Prefix) > 0 {
			prefix = req.Prefix
		}

		return prefix + req.Message, nil
	},
}

server.RegisterTool(echoTool)
```

#### 여러 응답 타입을 반환하는 도구

```go
// JSON 데이터를 반환하는 도구입니다
dataTool := mcp.Tool{
	Name:        "data.generate",
	Description: "Generates sample data in various formats",
	InputSchema: mcp.InputSchema{
		Properties: map[string]any{
			"format": map[string]any{
				"type":        "string",
				"description": "Format of data (json, text)",
				"enum":        []string{"json", "text"},
			},
		},
	},
	Handler: func(ctx context.Context, params map[string]any) (any, error) {
		var req struct {
			Format string `json:"format"`
		}

		if err := mcp.ParseArguments(params, &req); err != nil {
			return nil, fmt.Errorf("failed to parse params: %w", err)
		}

		if req.Format == "json" {
			// 반환값을 설명합니다
			return map[string]any{
				"items": []map[string]any{
					{"id": 1, "name": "Item 1"},
					{"id": 2, "name": "Item 2"},
				},
				"count": 2,
			}, nil
		}

		// Default 예시입니다
		return "Sample text data", nil
	},
}

server.RegisterTool(dataTool)
```

#### 이미지 생성 도구 예제

```go
// 이미지 콘텐츠를 반환하는 도구입니다
imageTool := mcp.Tool{
	Name:        "image.generate",
	Description: "Generates a simple image",
	InputSchema: mcp.InputSchema{
		Properties: map[string]any{
			"type": map[string]any{
				"type":        "string",
				"description": "Type of image to generate",
				"default":     "placeholder",
			},
		},
	},
	Handler: func(ctx context.Context, params map[string]any) (any, error) {
		// 반환값을 설명합니다
		return mcp.ImageContent{
			Data:     "base64EncodedImageData...", // Base64 예시입니다
			MimeType: "image/png",
		}, nil
	},
}

server.RegisterTool(imageTool)
```

#### `ToolResult` 기반 사용자 정의 출력

```go
// Tool, ToolResult 예시입니다
customResultTool := mcp.Tool{
	Name:        "custom.result",
	Description: "Returns a custom formatted result",
	InputSchema: mcp.InputSchema{
		Properties: map[string]any{
			"resultType": map[string]any{
				"type": "string",
				"enum": []string{"text", "image"},
			},
		},
	},
	Handler: func(ctx context.Context, params map[string]any) (any, error) {
		var req struct {
			ResultType string `json:"resultType"`
		}

		if err := mcp.ParseArguments(params, &req); err != nil {
			return nil, fmt.Errorf("failed to parse params: %w", err)
		}

		if req.ResultType == "image" {
			return mcp.ToolResult{
				Type: mcp.ContentTypeImage,
				Content: map[string]any{
					"data":     "base64EncodedImageData...",
					"mimeType": "image/jpeg",
				},
			}, nil
		}

		// Default 예시입니다
		return mcp.ToolResult{
			Type:    mcp.ContentTypeText,
			Content: "This is a text result from ToolResult",
		}, nil
	},
}

server.RegisterTool(customResultTool)
```

### Prompt 등록

Prompts은 reusable conversation 템플릿 위한 AI models입니다.

#### Static Prompt 예제:

```go
// 등록합니다
server.RegisterPrompt(mcp.Prompt{
	Name:        "hello",
	Description: "A simple hello prompt",
	Arguments: []mcp.PromptArgument{
		{
			Name:        "name",
			Description: "The name to greet",
			Required:    false,
		},
	},
	Content: "Say hello to {{name}} and introduce yourself as an AI assistant.",
})
```

#### Dynamic Prompt 사용하여 핸들러 함수:

```go
// 등록합니다
server.RegisterPrompt(mcp.Prompt{
	Name:        "dynamic-prompt",
	Description: "A prompt that uses a handler to generate dynamic content",
	Arguments: []mcp.PromptArgument{
		{
			Name:        "username",
			Description: "User's name for personalized greeting",
			Required:    true,
		},
		{
			Name:        "topic",
			Description: "Topic of expertise",
			Required:    true,
		},
	},
	Handler: func(ctx context.Context, args map[string]string) ([]mcp.PromptMessage, error) {
		var req struct {
			Username string `json:"username"`
			Topic    string `json:"topic"`
		}

		if err := mcp.ParseArguments(args, &req); err != nil {
			return nil, fmt.Errorf("failed to parse args: %w", err)
		}

		// 생성합니다
		userMessage := mcp.PromptMessage{
			Role: mcp.RoleUser,
			Content: mcp.TextContent{
				Text: fmt.Sprintf("Hello, I'm %s and I'd like to learn about %s.", req.Username, req.Topic),
			},
		}

		// 생성합니다
		currentTime := time.Now().Format(time.RFC1123)
		assistantMessage := mcp.PromptMessage{
			Role: mcp.RoleAssistant,
			Content: mcp.TextContent{
				Text: fmt.Sprintf("Hello %s! I'm an AI assistant and I'll help you learn about %s. The current time is %s.",
					req.Username, req.Topic, currentTime),
			},
		}

		// 반환값을 설명합니다
		return []mcp.PromptMessage{userMessage, assistantMessage}, nil
	},
})
```

#### Multi-Message Prompt 사용하여 Code 예제:

```go
// 등록합니다
server.RegisterPrompt(mcp.Prompt{
	Name:        "code-example",
	Description: "Provides code examples in different programming languages",
	Arguments: []mcp.PromptArgument{
		{
			Name:        "language",
			Description: "Programming language for the example",
			Required:    true,
		},
		{
			Name:        "complexity",
			Description: "Complexity level (simple, medium, advanced)",
		},
	},
	Handler: func(ctx context.Context, args map[string]string) ([]mcp.PromptMessage, error) {
		var req struct {
			Language   string `json:"language"`
			Complexity string `json:"complexity,optional"`
		}

		if err := mcp.ParseArguments(args, &req); err != nil {
			return nil, fmt.Errorf("failed to parse args: %w", err)
		}

		// Validate 예시입니다
		supportedLanguages := map[string]bool{"go": true, "python": true, "javascript": true, "rust": true}
		if !supportedLanguages[req.Language] {
			return nil, fmt.Errorf("unsupported language: %s", req.Language)
		}

		// Generate 예시입니다
		var codeExample string

		switch req.Language {
		case "go":
			if req.Complexity == "simple" {
				codeExample = `
package main

import "fmt"

func main() {
	fmt.Println("Hello, World!")
}`
			} else {
				codeExample = `
package main

import (
	"fmt"
	"time"
)

func main() {
	now := time.Now()
	fmt.Printf("Hello, World! Current time is %s\n", now.Format(time.RFC3339))
}`
			}
		case "python":
			// Python example code
			if req.Complexity == "simple" {
				codeExample = `
def greet(name):
    return f"Hello, {name}!"

print(greet("World"))`
			} else {
				codeExample = `
import datetime

def greet(name, include_time=False):
    message = f"Hello, {name}!"
    if include_time:
        message += f" Current time is {datetime.datetime.now().isoformat()}"
    return message

print(greet("World", include_time=True))`
			}
		}

		// 생성합니다
		messages := []mcp.PromptMessage{
			{
				Role: mcp.RoleAssistant,
				Content: mcp.TextContent{
					Text: fmt.Sprintf("You are a helpful coding assistant specialized in %s programming.", req.Language),
				},
			},
			{
				Role: mcp.RoleUser,
				Content: mcp.TextContent{
					Text: fmt.Sprintf("Show me a %s example of a Hello World program in %s.", req.Complexity, req.Language),
				},
			},
			{
				Role: mcp.RoleAssistant,
				Content: mcp.TextContent{
					Text: fmt.Sprintf("Here's a %s example in %s:\n\n```%s%s\n```\n\nHow can I help you implement this?",
						req.Complexity, req.Language, req.Language, codeExample),
				},
			},
		}

		return messages, nil
	},
})
```

### 리소스 등록

리소스는 파일이나 생성된 데이터 같은 외부 콘텐츠에 접근할 수 있게 합니다.

#### 기본 Resource 예제:

```go
// 등록합니다
server.RegisterResource(mcp.Resource{
	Name:        "example-document",
	URI:         "file:///example/document.txt",
	Description: "An example document",
	MimeType:    "text/plain",
	Handler: func(ctx context.Context) (mcp.ResourceContent, error) {
		return mcp.ResourceContent{
			URI:      "file:///example/document.txt",
			MimeType: "text/plain",
			Text:     "This is an example document content.",
		}, nil
	},
})
```

#### Dynamic Resource 사용하여 Code 예제:

```go
// 등록합니다
server.RegisterResource(mcp.Resource{
	Name:        "go-example",
	URI:         "file:///project/src/main.go",
	Description: "A simple Go example with multiple files",
	MimeType:    "text/x-go",
	Handler: func(ctx context.Context) (mcp.ResourceContent, error) {
		// 반환값을 설명합니다
		return mcp.ResourceContent{
			URI:      "file:///project/src/main.go",
			MimeType: "text/x-go",
			Text:     "package main\n\nimport (\n\t\"fmt\"\n\t\"./greeting\"\n)\n\nfunc main() {\n\tfmt.Println(greeting.Hello(\"world\"))\n}",
		}, nil
	},
})

// 등록합니다
server.RegisterResource(mcp.Resource{
	Name:        "go-greeting",
	URI:         "file:///project/src/greeting/greeting.go",
	Description: "A greeting package for the Go example",
	MimeType:    "text/x-go",
	Handler: func(ctx context.Context) (mcp.ResourceContent, error) {
		return mcp.ResourceContent{
			URI:      "file:///project/src/greeting/greeting.go",
			MimeType: "text/x-go",
			Text:     "package greeting\n\nfunc Hello(name string) string {\n\treturn \"Hello, \" + name + \"!\"\n}",
		}, nil
	},
})
```

#### 바이너리 Resource 예제:

```go
// 등록합니다
server.RegisterResource(mcp.Resource{
	Name:        "example-image",
	URI:         "file:///example/image.png",
	Description: "An example image",
	MimeType:    "image/png",
	Handler: func(ctx context.Context) (mcp.ResourceContent, error) {
		// 파일 콘텐츠를 읽습니다
		imageData := "base64EncodedImageData..." // Base64 예시입니다

		return mcp.ResourceContent{
			URI:      "file:///example/image.png",
			MimeType: "image/png",
			Blob:     imageData, // For 예시입니다
		}, nil
	},
})
```

### Prompt에서 리소스 사용


```go
// 등록합니다
server.RegisterPrompt(mcp.Prompt{
	Name:        "resource-example",
	Description: "A prompt that embeds a resource",
	Arguments: []mcp.PromptArgument{
		{
			Name:        "file_type",
			Description: "Type of file to show (rust or go)",
			Required:    true,
		},
	},
	Handler: func(ctx context.Context, args map[string]string) ([]mcp.PromptMessage, error) {
		var req struct {
			FileType string `json:"file_type"`
		}

		if err := mcp.ParseArguments(args, &req); err != nil {
			return nil, fmt.Errorf("failed to parse args: %w", err)
		}

		var resourceURI, mimeType, fileContent string
		if req.FileType == "rust" {
			resourceURI = "file:///project/src/main.rs"
			mimeType = "text/x-rust"
			fileContent = "fn main() {\n    println!(\"Hello world!\");\n}"
		} else {
			resourceURI = "file:///project/src/main.go"
			mimeType = "text/x-go"
			fileContent = "package main\n\nimport \"fmt\"\n\nfunc main() {\n\tfmt.Println(\"Hello, world!\")\n}"
		}

		// 생성합니다
		return []mcp.PromptMessage{
			{
				Role: mcp.RoleUser,
				Content: mcp.TextContent{
					Text: fmt.Sprintf("Can you explain this %s code?", req.FileType),
				},
			},
			{
				Role: mcp.RoleAssistant,
				Content: mcp.EmbeddedResource{
					Type: mcp.ContentTypeResource,
					Resource: struct {
						URI      string `json:"uri"`
						MimeType string `json:"mimeType"`
						Text     string `json:"text,omitempty"`
						Blob     string `json:"blob,omitempty"`
					}{
						URI:      resourceURI,
						MimeType: mimeType,
						Text:     fileContent,
					},
				},
			},
			{
				Role: mcp.RoleAssistant,
				Content: mcp.TextContent{
					Text: fmt.Sprintf("Above is a simple Hello World example in %s. Let me explain how it works.", req.FileType),
				},
			},
		}, nil
	},
})
```

### Multiple 파일 Resources 예제

```go
// 등록합니다
server.RegisterPrompt(mcp.Prompt{
	Name:        "go-code-example",
	Description: "A prompt that correctly embeds multiple resource files",
	Arguments: []mcp.PromptArgument{
		{
			Name:        "format",
			Description: "How to format the code display",
		},
	},
	Handler: func(ctx context.Context, args map[string]string) ([]mcp.PromptMessage, error) {
		var req struct {
			Format string `json:"format,optional"`
		}

		if err := mcp.ParseArguments(args, &req); err != nil {
			return nil, fmt.Errorf("failed to parse args: %w", err)
		}

		// 가져옵니다
		var mainGoText string = "package main\n\nimport (\n\t\"fmt\"\n\t\"./greeting\"\n)\n\nfunc main() {\n\tfmt.Println(greeting.Hello(\"world\"))\n}"
		var greetingGoText string = "package greeting\n\nfunc Hello(name string) string {\n\treturn \"Hello, \" + name + \"!\"\n}"

		// 생성합니다
		messages := []mcp.PromptMessage{
			{
				Role: mcp.RoleUser,
				Content: mcp.TextContent{
					Text: "Show me a simple Go example with proper imports.",
				},
			},
			{
				Role: mcp.RoleAssistant,
				Content: mcp.TextContent{
					Text: "Here's a simple Go example project:",
				},
			},
			{
				Role: mcp.RoleAssistant,
				Content: mcp.EmbeddedResource{
					Type: mcp.ContentTypeResource,
					Resource: struct {
						URI      string `json:"uri"`
						MimeType string `json:"mimeType"`
						Text     string `json:"text,omitempty"`
						Blob     string `json:"blob,omitempty"`
					}{
						URI:      "file:///project/src/main.go",
						MimeType: "text/x-go",
						Text:     mainGoText,
					},
				},
			},
		}

		// 추가합니다
		if req.Format == "with_explanation" {
			messages = append(messages, mcp.PromptMessage{
				Role: mcp.RoleAssistant,
				Content: mcp.TextContent{
					Text: "This example demonstrates a simple Go application with modular structure. The main.go file imports from a local 'greeting' package that provides the Hello function.",
				},
			})

			// Also 예시입니다
			messages = append(messages, mcp.PromptMessage{
				Role: mcp.RoleAssistant,
				Content: mcp.EmbeddedResource{
					Type: mcp.ContentTypeResource,
					Resource: struct {
						URI      string `json:"uri"`
						MimeType string `json:"mimeType"`
						Text     string `json:"text,omitempty"`
						Blob     string `json:"blob,omitempty"`
					}{
						URI:      "file:///project/src/greeting/greeting.go",
						MimeType: "text/x-go",
						Text:     greetingGoText,
					},
				},
			})
		}

		return messages, nil
	},
})
```

### 완전한 Application 예제

Here's 완전한 예제 demonstrating 모든 컴포넌트:

```go
package main

import (
	"context"
	"fmt"
	"log"
	"time"

	"github.com/zeromicro/go-zero/core/conf"
	"github.com/zeromicro/go-zero/core/logx"
	"github.com/zeromicro/go-zero/mcp"
)

func main() {
	// 로드합니다
	var c mcp.McpConf
	if err := conf.Load("config.yaml", &c); err != nil {
		log.Fatalf("Failed to load config: %v", err)
	}

	// Set up logging
	logx.DisableStat()

	// 생성합니다
	server := mcp.NewMcpServer(c)
	defer server.Stop()

	// 등록합니다
	echoTool := mcp.Tool{
		Name:        "echo",
		Description: "Echoes back the message provided by the user",
		InputSchema: mcp.InputSchema{
			Properties: map[string]any{
				"message": map[string]any{
					"type":        "string",
					"description": "The message to echo back",
				},
				"prefix": map[string]any{
					"type":        "string",
					"description": "Optional prefix to add to the echoed message",
					"default":     "Echo: ",
				},
			},
			Required: []string{"message"},
		},
		Handler: func(ctx context.Context, params map[string]any) (any, error) {
			var req struct {
				Message string `json:"message"`
				Prefix  string `json:"prefix,optional"`
			}

			if err := mcp.ParseArguments(params, &req); err != nil {
				return nil, fmt.Errorf("failed to parse args: %w", err)
			}

			prefix := "Echo: "
			if len(req.Prefix) > 0 {
				prefix = req.Prefix
			}

			return prefix + req.Message, nil
		},
	}
	server.RegisterTool(echoTool)

	// 등록합니다
	server.RegisterPrompt(mcp.Prompt{
		Name:        "greeting",
		Description: "A simple greeting prompt",
		Arguments: []mcp.PromptArgument{
			{
				Name:        "name",
				Description: "The name to greet",
				Required:    true,
			},
		},
		Content: "Hello {{name}}! How can I assist you today?",
	})

	// 등록합니다
	server.RegisterPrompt(mcp.Prompt{
		Name:        "dynamic-prompt",
		Description: "A prompt that uses a handler to generate dynamic content",
		Arguments: []mcp.PromptArgument{
			{
				Name:        "username",
				Description: "User's name for personalized greeting",
				Required:    true,
			},
			{
				Name:        "topic",
				Description: "Topic of expertise",
				Required:    true,
			},
		},
		Handler: func(ctx context.Context, args map[string]string) ([]mcp.PromptMessage, error) {
			var req struct {
				Username string `json:"username"`
				Topic    string `json:"topic"`
			}

			if err := mcp.ParseArguments(args, &req); err != nil {
				return nil, fmt.Errorf("failed to parse args: %w", err)
			}

			// 생성합니다
			currentTime := time.Now().Format(time.RFC1123)
			return []mcp.PromptMessage{
				{
					Role: mcp.RoleUser,
					Content: mcp.TextContent{
						Text: fmt.Sprintf("Hello, I'm %s and I'd like to learn about %s.", req.Username, req.Topic),
					},
				},
				{
					Role: mcp.RoleAssistant,
					Content: mcp.TextContent{
						Text: fmt.Sprintf("Hello %s! I'm an AI assistant and I'll help you learn about %s. The current time is %s.",
							req.Username, req.Topic, currentTime),
					},
				},
			}, nil
		},
	})

	// 등록합니다
	server.RegisterResource(mcp.Resource{
		Name:        "example-doc",
		URI:         "file:///example/doc.txt",
		Description: "An example document",
		MimeType:    "text/plain",
		Handler: func(ctx context.Context) (mcp.ResourceContent, error) {
			return mcp.ResourceContent{
				URI:      "file:///example/doc.txt",
				MimeType: "text/plain",
				Text:     "This is the content of the example document.",
			}, nil
		},
	})

	// 시작합니다
	fmt.Printf("Starting MCP server on %s:%d\n", c.Host, c.Port)
	server.Start()
}
```

## 오류 처리

MCP 구현은 포괄적인 오류 처리를 제공합니다.

- 도구 실행 오류를 client에 올바르게 보고합니다.
- 누락되었거나 유효하지 않은 매개변수를 감지하고 적절한 오류 코드로 보고합니다.
- 리소스와 prompt 조회 실패를 graceful하게 처리합니다.
- 오래 실행되는 도구 실행은 context 기반 timeout으로 처리합니다.
- panic recovery로 서버 crash를 방지합니다.

## 고급 기능

- **Annotation**: content에 audience와 priority metadata 추가
- **콘텐츠 타입**: text, image, audio 및 기타 콘텐츠 형식 지원
- **임베디드 리소스**: prompt 응답에 파일 리소스를 직접 포함
- **context 인식**: 모든 handler가 timeout과 cancellation 지원을 위한 `context.Context`를 받음
- **Progress token**: 오래 실행되는 작업의 진행 상황 추적 지원
- **커스터마이징 가능한 timeout**: 도구와 작업의 실행 timeout 설정

## 성능 고려 사항

- 도구 실행은 blocking을 막기 위해 설정 가능한 timeout 안에서 실행됩니다.
- 효율적인 client 추적과 정리로 리소스 누수를 방지합니다.
- 공유 리소스에는 mutex 보호를 사용해 동시성을 올바르게 처리합니다.
- buffered message channel로 client 메시지 전달 시 blocking을 방지합니다.
