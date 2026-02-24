#!/usr/bin/env python3
"""Fix frontmatter titles and add descriptions to imported docs."""
import os
import re

FIXES = {
    # tasks/installation
    "tasks/installation/go-zero.md":         ("Install go-zero", "Install the go-zero framework as a dependency in your Go module."),
    "tasks/installation/golang.md":          ("Install Go", "Download and install the Go programming language on Linux, macOS, or Windows."),
    "tasks/installation/goctl.md":           ("Install goctl", "Install the go-zero code generation tool goctl."),
    "tasks/installation/goctl-intellij.md":  ("GoLand Plugin", "Install and use the goctl plugin for JetBrains GoLand IDE."),
    "tasks/installation/goctl-vscode.md":    ("VS Code Extension", "Install and use the goctl extension for Visual Studio Code."),
    "tasks/installation/protoc.md":          ("Install protoc", "Install the Protocol Buffers compiler and the Go gRPC plugins."),
    # tasks/create
    "tasks/create/command.md":               ("Create Project (CLI)", "Scaffold a new go-zero project from the command line."),
    "tasks/create/goland.md":                ("Create Project (GoLand)", "Scaffold a new go-zero project from JetBrains GoLand."),
    "tasks/create/vscode.md":                ("Create Project (VS Code)", "Scaffold a new go-zero project from Visual Studio Code."),
    # tasks/dsl
    "tasks/dsl/api.md":                      ("API Syntax", "Write and validate go-zero .api DSL files."),
    "tasks/dsl/proto.md":                    ("Proto Syntax", "Write Protocol Buffer .proto files for go-zero gRPC services."),
    # tasks/cli
    "tasks/cli/api-demo.md":                 ("API Demo Code Generation", "Generate a complete HTTP service from an .api file using goctl."),
    "tasks/cli/api-format.md":               ("API File Formatting", "Format go-zero .api files with goctl."),
    "tasks/cli/grpc-demo.md":                ("gRPC Demo Code Generation", "Generate a gRPC service from a .proto file using goctl."),
    "tasks/cli/mongo.md":                    ("MongoDB Model Generation", "Generate MongoDB model code with goctl."),
    "tasks/cli/mysql.md":                    ("MySQL Model Generation", "Generate MySQL model code with goctl."),
    # tasks/log
    "tasks/log/log.md":                      ("Logging", "Configure and use structured logging in go-zero."),
    # tasks
    "tasks/memory-cache.md":                 ("Memory Cache", "Use in-process memory caching in go-zero services."),
    "tasks/configcenter.md":                 ("Config Center", "Integrate go-zero with a remote configuration center."),
    "tasks/static-configuration/configuration.md": ("Static Configuration", "Load and manage static YAML/JSON configuration files in go-zero."),
    # tasks/mongo
    "tasks/mongo/conn.md":                   ("MongoDB Connection", "Create a MongoDB connection in go-zero."),
    "tasks/mongo/curd.md":                   ("MongoDB CRUD", "Perform create, read, update, and delete operations with MongoDB."),
    # tasks/mysql
    "tasks/mysql/mysql.md":                  ("MySQL Quickstart", "Connect to MySQL and run queries in go-zero."),
    # tasks/redis
    "tasks/redis/redis.md":                  ("Redis Quickstart", "Connect to Redis and run commands in go-zero."),
    # tasks/queue
    "tasks/queue/delay-queue.md":            ("Delay Queue", "Use a delay queue in go-zero with beanstalkd."),
    "tasks/queue/message-queue.md":          ("Message Queue", "Use a message queue in go-zero with Kafka."),
    # tutorials/cli
    "tutorials/cli/overview.md":             ("goctl Overview", "Overview of the goctl code generation tool."),
    "tutorials/cli/quickstart.md":           ("goctl Quickstart", "Get started with goctl code generation."),
    "tutorials/cli/api.md":                  ("goctl API", "Generate HTTP service code from an .api file."),
    "tutorials/cli/rpc.md":                  ("goctl RPC", "Generate gRPC service code from a .proto file."),
    "tutorials/cli/model.md":                ("goctl Model", "Generate database model code with goctl."),
    "tutorials/cli/docker.md":               ("goctl Docker", "Generate a Dockerfile with goctl."),
    "tutorials/cli/kube.md":                 ("goctl Kubernetes", "Generate Kubernetes deployment manifests with goctl."),
    "tutorials/cli/env.md":                  ("goctl Environment", "Check and configure the goctl build environment."),
    "tutorials/cli/config.md":               ("goctl Configuration", "Manage goctl configuration."),
    "tutorials/cli/bug.md":                  ("goctl Bug Report", "Report a goctl bug with goctl bug."),
    "tutorials/cli/completion.md":           ("Shell Completion", "Set up shell auto-completion for goctl."),
    "tutorials/cli/migrate.md":              ("goctl Migrate", "Migrate goctl templates to the latest version."),
    "tutorials/cli/style.md":                ("goctl Style", "Configure the naming style for generated code."),
    "tutorials/cli/swagger.md":              ("goctl Swagger", "Generate Swagger/OpenAPI documentation with goctl."),
    "tutorials/cli/template.md":             ("goctl Template", "Customize goctl code generation templates."),
    "tutorials/cli/upgrade.md":              ("goctl Upgrade", "Upgrade goctl to the latest version."),
    # tutorials/api
    "tutorials/api/faq.md":                  ("API FAQ", "Frequently asked questions about the go-zero .api DSL."),
    "tutorials/api/import.md":               ("API Import", "Organize .api files with import statements."),
    "tutorials/api/jwt.md":                  ("API JWT Auth", "Declare JWT authentication in an .api file."),
    "tutorials/api/middleware.md":           ("API Middleware Declaration", "Declare middleware in an .api file."),
    "tutorials/api/parameter.md":            ("API Parameters", "Define request and response parameters in an .api file."),
    "tutorials/api/route-group.md":          ("API Route Groups", "Group routes in an .api file."),
    "tutorials/api/route-prefix.md":         ("API Route Prefix", "Add a URL prefix to a route group."),
    "tutorials/api/route-rule.md":           ("API Route Rules", "Define routing rules in an .api file."),
    "tutorials/api/route-sse.md":            ("SSE Routes", "Define Server-Sent Events routes in an .api file."),
    "tutorials/api/signature.md":            ("Request Signing", "Add HMAC signature verification to API routes."),
    "tutorials/api/type.md":                 ("API Types", "Define request and response types in an .api file."),
    # tutorials/configuration
    "tutorials/configuration/overview.md":    ("Configuration Overview", "Overview of go-zero service configuration."),
    "tutorials/configuration/log.md":         ("Log Configuration", "Configure structured logging in go-zero."),
    "tutorials/configuration/service.md":     ("Service Configuration", "Full reference for go-zero HTTP service configuration."),
    "tutorials/configuration/prometheus.md":  ("Prometheus Configuration", "Configure Prometheus metrics in go-zero."),
    "tutorials/configuration/auto-validation.md": ("Config Auto-Validation", "Automatically validate configuration on startup."),
    # tutorials/gateway
    "tutorials/gateway/grpc.md":             ("gRPC Gateway", "Expose gRPC services over HTTP using go-zero's gateway."),
    "tutorials/gateway/http.md":             ("HTTP Gateway", "Proxy HTTP requests through the go-zero gateway."),
    # tutorials/grpc
    "tutorials/grpc/interceptor.md":         ("gRPC Interceptors", "Add server-side and client-side interceptors to gRPC services."),
    "tutorials/grpc/server/configuration.md":("gRPC Server Configuration", "Full reference for go-zero gRPC server configuration."),
    "tutorials/grpc/server/example.md":      ("gRPC Server Example", "Complete example of a go-zero gRPC server."),
    "tutorials/grpc/client/configuration.md":("gRPC Client Configuration", "Full reference for go-zero gRPC client configuration."),
    "tutorials/grpc/client/conn.md":         ("gRPC Client Connection", "Create a gRPC client connection in go-zero."),
    # tutorials/http/server
    "tutorials/http/server/configuration.md":("HTTP Server Configuration", "Full reference for go-zero HTTP server configuration."),
    "tutorials/http/server/error.md":        ("Error Handling", "Handle and format errors in go-zero HTTP services."),
    "tutorials/http/server/request-body.md": ("Request Body", "Parse request bodies in go-zero HTTP handlers."),
    "tutorials/http/server/response-body.md":("Response Body", "Write response bodies in go-zero HTTP handlers."),
    "tutorials/http/server/response-ext.md": ("Response Extensions", "Extended response helpers in go-zero HTTP services."),
    "tutorials/http/server/sse.md":          ("Server-Sent Events", "Stream data to clients using SSE in go-zero."),
    # tutorials/http
    "tutorials/http/client/index.md":        ("HTTP Client", "Make HTTP calls from go-zero services."),
    # tutorials/log
    "tutorials/log/log.md":                  ("Logging", "Configure and use go-zero's structured logging (logx)."),
    # tutorials/mcp
    "tutorials/mcp/servers.md":              ("MCP Servers", "Build Model Context Protocol servers with go-zero."),
    # tutorials/mongo
    "tutorials/mongo/connection.md":         ("MongoDB Connection", "Connect to MongoDB in a go-zero service."),
    "tutorials/mongo/curd.md":               ("MongoDB CRUD", "Perform CRUD operations with MongoDB in go-zero."),
    "tutorials/mongo/cache.md":              ("MongoDB Caching", "Add caching to MongoDB queries in go-zero."),
    # tutorials/mysql
    "tutorials/mysql/connection.md":         ("MySQL Connection", "Connect to MySQL in a go-zero service."),
    "tutorials/mysql/curd.md":               ("MySQL CRUD", "Perform CRUD operations with MySQL in go-zero."),
    "tutorials/mysql/cache.md":              ("MySQL Caching", "Add caching to MySQL queries with go-zero sqlc."),
    "tutorials/mysql/bulk-insert.md":        ("MySQL Bulk Insert", "Perform bulk inserts efficiently in go-zero."),
    "tutorials/mysql/local-transaction.md":  ("Local Transactions", "Use local transactions with go-zero sqlx."),
    "tutorials/mysql/distribute-transaction.md":("Distributed Transactions", "Use distributed transactions with go-zero."),
    # tutorials/ops
    "tutorials/ops/prepare.md":              ("Environment Setup", "Prepare the CI/CD environment (GitLab, Jenkins, Harbor, Kubernetes)."),
    "tutorials/ops/docker-compose.md":       ("Docker Compose Deployment", "Deploy go-zero services with Docker Compose."),
    "tutorials/ops/machine.md":              ("Machine Deployment", "Deploy go-zero services to a physical or virtual machine."),
    "tutorials/ops/k8s.md":                  ("Kubernetes CI/CD Pipeline", "Deploy go-zero services to Kubernetes via a Jenkins CI/CD pipeline."),
    # tutorials/proto
    "tutorials/proto/spec.md":               ("Proto Spec", "go-zero Protocol Buffer specification and conventions."),
    "tutorials/proto/services-group.md":     ("Services Grouping", "Organize multiple services in a single .proto file."),
    "tutorials/proto/faq.md":                ("Proto FAQ", "Frequently asked questions about go-zero Proto usage."),
    # tutorials/queue
    "tutorials/queue/kafka.md":              ("Kafka Queue", "Use Kafka as a message queue in go-zero."),
    "tutorials/queue/beanstalkd.md":         ("Beanstalkd Queue", "Use Beanstalkd as a delay queue in go-zero."),
    # tutorials/redis
    "tutorials/redis/db-selection.md":       ("Redis DB Selection", "Configure Redis database selection in go-zero."),
    "tutorials/redis/metric.md":             ("Redis Metrics", "Monitor Redis connection metrics in go-zero."),
    "tutorials/redis/redis-lock.md":         ("Redis Distributed Lock", "Implement distributed locks with Redis in go-zero."),
    # tutorials/service-governance
    "tutorials/service-governance/breaker.md":    ("Circuit Breaker", "Configure circuit breaking in go-zero services."),
    "tutorials/service-governance/limiter.md":    ("Rate Limiter", "Configure rate limiting in go-zero services."),
    "tutorials/service-governance/loadbalance.md":("Load Balancing", "Configure load balancing in go-zero RPC clients."),
    # tutorials/cron-job
    "tutorials/cron-job/k8s.md":             ("Cron Jobs on Kubernetes", "Schedule cron jobs with go-zero on Kubernetes."),
    # tutorials/customization
    "tutorials/customization/template.md":   ("Template Customization", "Customize goctl code generation templates."),
    # concepts
    "concepts/architecture-evolution.md":    ("Architecture Evolution", "How go-zero's architecture evolved from monolith to microservices."),
    "concepts/components.md":               ("Component Architecture", "Overview of go-zero's core components and their relationships."),
    "concepts/keywords.md":                 ("Keywords", "Key terms and concepts in the go-zero ecosystem."),
    "concepts/layout.md":                   ("Project Layout", "Standard directory structure for go-zero projects."),
    # components
    "components/fx.md":                      ("FX Pipeline", "Build data pipelines with go-zero's FX streaming utility."),
    "components/mr.md":                      ("MapReduce", "Concurrent map-reduce for Go with go-zero mr."),
    "components/limiter/peroid.md":          ("Period Limiter", "Limit request rates per period with go-zero."),
    "components/limiter/token.md":           ("Token Bucket Limiter", "Limit request rates with a token bucket in go-zero."),
    "components/log/logc.md":                ("logc", "Context-aware structured logging with go-zero logc."),
    "components/log/logx.md":                ("logx", "Structured logging with go-zero logx."),
    "components/syncx/limit.md":             ("syncx Limit", "Concurrency limit primitive from go-zero syncx."),
    # faq
    "faq/deploy/binary-size.md":             ("Reducing Binary Size", "Tips to reduce the Go binary size for production deployments."),
    "faq/http/cors.md":                      ("CORS Configuration", "Configure Cross-Origin Resource Sharing in go-zero HTTP services."),
    "faq/http/fileserver.md":                ("File Server", "Serve static files from a go-zero HTTP service."),
    "faq/log/fileconsole.md":                ("Log to File and Console", "Output logs to both file and console in go-zero."),
    # reference
    "reference/releases/v1.9.0.md":         ("Release v1.9.0", "go-zero v1.9.0 release notes and migration guide."),
    "reference/proto.md":                   ("Proto Reference", "Protocol Buffer usage reference for go-zero."),
    "reference/goctl-plugins.md":           ("goctl Plugins", "Extend goctl with community plugins."),
    # contributing
    "contributing/contributors.md":          ("Contributors", "The people who built go-zero."),
    # tutorials/microservice
    "tutorials/microservice/service-discovery.md": ("Service Discovery", "Register and discover services in go-zero microservices."),
    "tutorials/microservice/load-balancing.md":    ("Load Balancing", "Configure load balancing in go-zero microservices."),
    "tutorials/microservice/distributed-tracing.md":("Distributed Tracing", "Add distributed tracing to go-zero microservices."),
    # monitor
    "tutorials/monitor/index.md":            ("Monitoring & Observability", "Monitor go-zero services with metrics, tracing, and logging."),
}

docs_root = "src/content/docs"
updated = 0
skipped = 0

for rel_path, (new_title, new_desc) in FIXES.items():
    full_path = os.path.join(docs_root, rel_path)
    if not os.path.exists(full_path):
        skipped += 1
        continue

    with open(full_path, encoding='utf-8') as f:
        original = f.read()

    # Must start with YAML frontmatter
    if not original.startswith("---\n"):
        skipped += 1
        continue

    # Find closing ---
    close_idx = original.find("\n---\n", 4)
    if close_idx == -1:
        skipped += 1
        continue

    fm_raw = original[4:close_idx]   # everything between opening and closing ---
    body = original[close_idx + 5:]   # everything after closing ---\n

    # Update title
    if re.search(r'^title:', fm_raw, re.MULTILINE):
        fm_raw = re.sub(r'^title:.*$', f'title: {new_title}', fm_raw, flags=re.MULTILINE, count=1)
    else:
        fm_raw = f'title: {new_title}\n' + fm_raw

    # Update or add description
    if new_desc:
        if re.search(r'^description:', fm_raw, re.MULTILINE):
            fm_raw = re.sub(r'^description:.*$', f'description: {new_desc}', fm_raw, flags=re.MULTILINE, count=1)
        else:
            # Insert after title line
            fm_raw = re.sub(
                r'^(title:.*)$',
                r'\1\ndescription: ' + new_desc,
                fm_raw,
                flags=re.MULTILINE,
                count=1,
            )

    new_content = "---\n" + fm_raw + "\n---\n" + body

    if new_content != original:
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        updated += 1

print(f"Updated {updated} EN files, skipped {skipped}")
