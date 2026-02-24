---
title: 文件上传
description: 处理 multipart 文件上传请求。
sidebar:
  order: 6

---

# 文件上传

go-zero 的每个 handler 都可访问原始 `http.Request`，因此标准 Go multipart 处理将直接适用。

## API 定义

```text
service upload-api {
    @handler UploadFile
    post /upload/file returns (UploadResp)
}

type UploadResp {
    Filename string `json:"filename"`
    Size     int64  `json:"size"`
    URL      string `json:"url"`
}
```

## Handler 实现

```go title="internal/handler/uploadfilehandler.go"
func UploadFileHandler(svcCtx *svc.ServiceContext) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        // 最多 32 MB 不落盘，超出部分自动落盘
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

        // 通过读取前 512 字节检测 MIME 类型
        buf := make([]byte, 512)
        n, _ := file.Read(buf)
        mimeType := http.DetectContentType(buf[:n])
        if !isAllowedType(mimeType) {
            httpx.Error(w, fmt.Errorf("不支持的文件类型: %s", mimeType),
                http.StatusUnsupportedMediaType)
            return
        }
        file.Seek(0, io.SeekStart)

        l := logic.NewUploadFileLogic(r.Context(), svcCtx)
        resp, err := l.UploadFile(file, header)
        if err != nil {
            httpx.Error(w, err)
            return
        }
        httpx.OkJson(w, resp)
    }
}
```

## Logic 层—存储到本地

```go title="internal/logic/uploadfilelogic.go"
func (l *UploadFileLogic) UploadFile(file multipart.File, header *multipart.FileHeader) (*types.UploadResp, error) {
    // 校验大小
    const maxSize = 10 << 20  // 10 MB
    if header.Size > maxSize {
        return nil, errorx.NewCodeError(400, "文件超过 10 MB 限制")
    }

    // 安全处理文件名，防路径穿越
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

## 云存储（S3 / OSS）

生产环境建议将文件上传到对象存储而非本地磁盘：

```go
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

## 服务配置

```yaml title="etc/app.yaml"
MaxBytes: 67108864   # 请求体最大 64 MB
UploadDir: ./uploads
```

## 测试

```bash
curl -X POST http://localhost:8888/upload/file \
  -F "file=@photo.png"
# {"filename":"photo.png","size":204800,"url":"/files/17...photo.png"}
```

## 最佳实践

- **同时校验大小和 MIME 类型**，不要仅依赖文件后缀名。
- **对文件名进行安全处理**，防止路径穿越攻击。
- 超过 100 MB 的大文件建议采用**分片上传 + 后台合并任务**的方式。
