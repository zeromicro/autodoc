---
title: File Upload
description: Handle multipart file uploads in go-zero HTTP services.
sidebar:
  order: 4
---

# File Upload

go-zero exposes the raw `http.Request` inside every handler, so standard Go multipart handling applies.

## API Definition

```text
service upload-api {
    @handler UploadFile
    post /upload/file returns (UploadResp)
}

type UploadResp {
    Filename string `json:"filename"`
    Size     int64  `json:"size"`
}
```

## Handler Implementation

```go title="internal/handler/uploadfilehandler.go"
func UploadFileHandler(svcCtx *svc.ServiceContext) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
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

        dst, _ := os.Create("./uploads/" + filepath.Base(header.Filename))
        defer dst.Close()
        size, _ := io.Copy(dst, file)

        httpx.OkJson(w, &types.UploadResp{Filename: header.Filename, Size: size})
    }
}
```

## Test

```bash
curl -X POST http://localhost:8888/upload/file -F "file=@photo.png"
# {"filename":"photo.png","size":204800}
```

## Limit File Size

```yaml
MaxBytes: 33554432  # 32 MB
```
