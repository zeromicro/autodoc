---
title: 파일 업로드
description: go-zero HTTP 서비스에서 multipart 파일 업로드를 처리하는 방법입니다.
sidebar:
  order: 6

---


go-zero는 모든 handler 안에서 원본 `http.Request`를 사용할 수 있으므로 표준 Go multipart 처리 방식을 그대로 적용할 수 있습니다. 이 가이드는 단일 파일 업로드, 검증, 여러 파일 업로드, cloud storage 연동을 다룹니다.

## API 정의

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

## handler 구현

```go title="internal/handler/uploadfilehandler.go"
func UploadFileHandler(svcCtx *svc.ServiceContext) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        // 메모리에는 최대 32MB까지만 보관하고, 더 큰 part는 디스크에 임시 저장합니다
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

        // 처음 512 byte를 읽어 MIME type을 검증합니다
        buf := make([]byte, 512)
        n, _ := file.Read(buf)
        mimeType := http.DetectContentType(buf[:n])
        if !isAllowedType(mimeType) {
            httpx.Error(w, fmt.Errorf("unsupported file type: %s", mimeType), http.StatusUnsupportedMediaType)
            return
        }
        // header를 읽은 뒤 파일 포인터를 다시 처음으로 되돌립니다
        file.Seek(0, io.SeekStart)

        // 로직 계층에 위임합니다
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

## 로직 계층 — 디스크에 저장

```go title="internal/logic/uploadfilelogic.go"
func (l *UploadFileLogic) UploadFile(file multipart.File, header *multipart.FileHeader) (*types.UploadResp, error) {
    // 크기를 검증합니다
    const maxSize = 10 << 20  // 10 MB
    if header.Size > maxSize {
        return nil, errorx.NewCodeError(400, "file exceeds 10 MB limit")
    }

    // 파일 이름을 안전하게 정리합니다
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

## Cloud Storage(S3 / Alibaba OSS)

프로덕션에서는 로컬 디스크 대신 object storage에 업로드하는 것을 권장합니다.

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

## 여러 파일 업로드

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

## 서버 설정

```yaml title="etc/app.yaml"
# 프레임워크 계층에서 전체 요청 본문 크기를 제한합니다
MaxBytes: 67108864   # 64 MB
UploadDir: ./uploads
```

## 테스트

```bash
# 단일 파일
curl -X POST http://localhost:8888/upload/file \
  -F "file=@photo.png"
# {"filename":"photo.png","size":204800,"url":"/files/17...photo.png"}

# 여러 파일
curl -X POST http://localhost:8888/upload/multiple \
  -F "file=@a.jpg" -F "file=@b.png"
```

## 모범 사례

- **크기와 MIME type을 모두 검증하세요** — 파일 확장자만 신뢰하지 마세요.
- **파일 이름을 sanitize하세요** — `../../etc/passwd` 같은 path traversal 공격을 방지해야 합니다.
- **content-type 검증 없이 업로드 파일을 같은 origin에서 제공하지 마세요** — 별도 domain이나 object-storage URL을 사용하세요.
- 큰 파일(100MB 초과)은 **multipart chunked upload**와 background assembly job 사용을 고려하세요.
