---
title: File Upload
description: Handle multipart file uploads in go-zero HTTP services.
sidebar:
  order: 6

---


go-zero exposes the raw `http.Request` inside every handler, so standard Go multipart handling applies. This guide covers single-file upload, validation, multiple files, and cloud storage integration.

## API Definition

```text
service upload-api {
    @handler UploadFile
    post /upload/file returns (UploadResp)

    @handler UploadMultiple
    post /upload/multiple returns (UploadMultipleResp)
}

type UploadResp {
    Filename string `json:"filename"`
    Size     int64  `json:"size"`
    URL      string `json:"url"`
}

type UploadMultipleResp {
    Files []UploadResp `json:"files"`
}
```

## Handler Implementation

```go title="internal/handler/uploadfilehandler.go"
func UploadFileHandler(svcCtx *svc.ServiceContext) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        // 32 MB max in-memory; larger parts spool to disk
        if err := r.ParseMultipartForm(32 << 20); err != nil {
            httpx.Error(w, err)
            return
        }

        file, header, err := r.FormFile("file")
        if err != nil {
            httpx.Error(w, err)
            return
        }
        defer file.Close()

        // Validate MIME type by reading the first 512 bytes
        buf := make([]byte, 512)
        n, _ := file.Read(buf)
        mimeType := http.DetectContentType(buf[:n])
        if !isAllowedType(mimeType) {
            httpx.Error(w, fmt.Errorf("unsupported file type: %s", mimeType), http.StatusUnsupportedMediaType)
            return
        }
        // Seek back to start after reading header
        file.Seek(0, io.SeekStart)

        // Delegate to logic layer
        l := logic.NewUploadFileLogic(r.Context(), svcCtx)
        resp, err := l.UploadFile(file, header)
        if err != nil {
            httpx.Error(w, err)
            return
        }
        httpx.OkJson(w, resp)
    }
}

func isAllowedType(mime string) bool {
    allowed := map[string]bool{
        "image/jpeg": true,
        "image/png":  true,
        "image/gif":  true,
        "application/pdf": true,
    }
    return allowed[mime]
}
```

## Logic Layer — Save to Disk

```go title="internal/logic/uploadfilelogic.go"
func (l *UploadFileLogic) UploadFile(file multipart.File, header *multipart.FileHeader) (*types.UploadResp, error) {
    // Validate size
    const maxSize = 10 << 20  // 10 MB
    if header.Size > maxSize {
        return nil, errorx.NewCodeError(400, "file exceeds 10 MB limit")
    }

    // Sanitize filename
    safeFilename := fmt.Sprintf("%d_%s", time.Now().UnixNano(),
        filepath.Base(filepath.Clean(header.Filename)))

    dst, err := os.Create(filepath.Join(l.svcCtx.Config.UploadDir, safeFilename))
    if err != nil {
        return nil, err
    }
    defer dst.Close()

    size, err := io.Copy(dst, file)
    if err != nil {
        return nil, err
    }

    return &types.UploadResp{
        Filename: header.Filename,
        Size:     size,
        URL:      "/files/" + safeFilename,
    }, nil
}
```

## Cloud Storage (S3 / Alibaba OSS)

For production, upload to object storage instead of local disk:

```go
import (
    "github.com/aws/aws-sdk-go-v2/service/s3"
)

func (l *UploadFileLogic) uploadToS3(file multipart.File, key string) (string, error) {
    _, err := l.svcCtx.S3.PutObject(l.ctx, &s3.PutObjectInput{
        Bucket: aws.String(l.svcCtx.Config.S3Bucket),
        Key:    aws.String(key),
        Body:   file,
    })
    if err != nil {
        return "", err
    }
    return fmt.Sprintf("https://%s.s3.amazonaws.com/%s",
        l.svcCtx.Config.S3Bucket, key), nil
}
```

## Multiple Files

```go title="internal/logic/uploadmultiplelogic.go"
func (l *UploadMultipleLogic) UploadMultiple(r *http.Request) (*types.UploadMultipleResp, error) {
    if err := r.ParseMultipartForm(64 << 20); err != nil {
        return nil, err
    }

    var results []types.UploadResp
    for _, headers := range r.MultipartForm.File {
        for _, header := range headers {
            f, err := header.Open()
            if err != nil {
                return nil, err
            }
            resp, err := l.UploadFile(f, header)
            f.Close()
            if err != nil {
                return nil, err
            }
            results = append(results, *resp)
        }
    }
    return &types.UploadMultipleResp{Files: results}, nil
}
```

## Server Configuration

```yaml title="etc/app.yaml"
# Limit total request body size at the framework level
MaxBytes: 67108864   # 64 MB
UploadDir: ./uploads
```

## Test

```bash
# Single file
curl -X POST http://localhost:8888/upload/file \
  -F "file=@photo.png"
# {"filename":"photo.png","size":204800,"url":"/files/17...photo.png"}

# Multiple files
curl -X POST http://localhost:8888/upload/multiple \
  -F "file=@a.jpg" -F "file=@b.png"
```

## Best Practices

- **Validate both size and MIME type** — do not rely on the file extension alone.
- **Sanitize filenames** to prevent path traversal (`../../etc/passwd` style) attacks.
- **Never serve uploaded files from the same origin** without content-type validation; use a separate domain or object-storage URL.
- For large files (>100 MB), consider **multipart chunked upload** and a background assembly job.
