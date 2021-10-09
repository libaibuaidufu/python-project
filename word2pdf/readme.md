### docker 快速使用

**必须：复制到windows 中文字体 simsun.ttc 到 当前文件夹目录，以避免中文乱码**

```shell
cd word2pdf
docker build -t word2pdf:v1 .
docker run -d -p 5000:5000 -v ~/word2pdf/download_files:/code/download_files -v ~/word2pdf/upload_files:/code/upload_files --name word2pdf word2pdf:v1
```
