package main

import (
	"fmt"
	"math"
	"os"
	"sync"
	"testing"
	"time"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/s3"
	"github.com/aws/aws-sdk-go/service/s3/s3manager"
)

type uploadType func(*s3manager.Uploader, int, int)
type downloadType func(*s3manager.Downloader, int, int)

func setupSession() *session.Session {
	sess := session.Must(session.NewSession(
		&aws.Config{
			Endpoint:         aws.String("http://localhost:7480"),
			Region:           aws.String("us-east-1"), // 添加这一行
			S3ForcePathStyle: aws.Bool(true),          // 添加这一行
		},
	))
	// create test bucket

	svc := s3.New(sess)
	fmt.Println("Setting up test session")
	fmt.Println("creating bucket with name of testbucket")
	_, err := svc.CreateBucket(&s3.CreateBucketInput{
		Bucket: aws.String("testbucket"),
		CreateBucketConfiguration: &s3.CreateBucketConfiguration{
			LocationConstraint: aws.String(""),
		},
	})
	if err != nil {
		fmt.Println("failed to create bucket", err)
		return nil
	}

	err = svc.WaitUntilBucketExists(&s3.HeadBucketInput{
		Bucket: aws.String("testbucket"),
	})
	if err != nil {
		fmt.Println("failed to wait for bucket to exist", err)
		return nil
	}
	fmt.Println("bucket created successfully")
	return sess
}

func DestroySession(sess *session.Session) {
	svc := s3.New(sess)
	fmt.Printf("\nDestroying test session\n")
	fmt.Println("deleting bucket with name of testbucket")
	// delete all objects in the bucket
	err := svc.ListObjectsPages(&s3.ListObjectsInput{
		Bucket: aws.String("testbucket"),
	}, func(p *s3.ListObjectsOutput, last bool) (shouldContinue bool) {
		for _, obj := range p.Contents {
			_, err := svc.DeleteObject(&s3.DeleteObjectInput{
				Bucket: aws.String("testbucket"),
				Key:    obj.Key,
			})
			if err != nil {
				fmt.Println("failed to delete object", err)
				return false
			}
			err = svc.WaitUntilObjectNotExists(&s3.HeadObjectInput{
				Bucket: aws.String("testbucket"),
				Key:    obj.Key,
			})
			if err != nil {
				fmt.Println("failed to wait for object to be deleted", err)
				return false
			}
		}
		return true
	})
	if err != nil {
		fmt.Println("failed to list objects", err)
	}
	// delete the bucket
	_, e := svc.DeleteBucket(&s3.DeleteBucketInput{
		Bucket: aws.String("testbucket"),
	})
	if e != nil {
		fmt.Println("failed to delete bucket", err)
	}
	fmt.Printf("bucket deleted successfully\n\n")

}
func NewUploader(sess *session.Session) *s3manager.Uploader {
	uploader := s3manager.NewUploader(sess)
	return uploader
}

func NewDownloader(sess *session.Session) *s3manager.Downloader {
	downloader := s3manager.NewDownloader(sess)
	return downloader
}

func TestCeph(t *testing.T) {
	sess := setupSession()
	if sess == nil {
		return
	}
	fmt.Println("==== test ceph ====")
	// try list buckets
	svc := s3.New(sess)
	buckets, err := svc.ListBuckets(nil)
	if err != nil {
		fmt.Println("failed to list buckets", err)
		return
	}
	fmt.Println("buckets:")
	for _, b := range buckets.Buckets {
		fmt.Print("  ")
		fmt.Println(*b.Name)
	}
	fmt.Println("==== test ceph end ====")
	defer DestroySession(sess)
}

func TestUpload(t *testing.T) {
	sess := setupSession()
	fmt.Println("==== test upload ====")
	if sess == nil {
		return
	}
	defer DestroySession(sess)
	uploader := NewUploader(sess)
	f, err := os.Open("test.txt")
	if err != nil {
		fmt.Println("failed to open file", err)
		return
	}
	defer f.Close()
	// list objects in the bucket
	svc := s3.New(sess)
	objects, err := svc.ListObjects(&s3.ListObjectsInput{
		Bucket: aws.String("testbucket"),
	})
	if err != nil {
		fmt.Println("failed to list objects", err)
		return
	}
	fmt.Println("objects in the bucket before upload:")
	if (objects.Contents) != nil {
		for _, obj := range objects.Contents {
			fmt.Print("  ")
			fmt.Println(*obj.Key)
		}
	} else {
		fmt.Println("  No objects in the bucket")
	}
	_, err = uploader.Upload(&s3manager.UploadInput{
		Bucket: aws.String("testbucket"),
		Key:    aws.String("test.txt"),
		Body:   f,
	})
	if err != nil {
		fmt.Println("failed to upload file", err)
		return
	}
	fmt.Println("file uploaded successfully")
	// list objects in the bucket

	objects, err = svc.ListObjects(&s3.ListObjectsInput{
		Bucket: aws.String("testbucket"),
	})
	if err != nil {
		fmt.Println("failed to list objects", err)
		return
	}
	fmt.Println("objects in the bucket:")
	for _, obj := range objects.Contents {
		fmt.Print("  ")
		fmt.Println(*obj.Key)
	}
	fmt.Println("==== test upload end ====")
}

func TestDownload(t *testing.T) {
	sess := setupSession()
	fmt.Println("==== test download ====")
	if sess == nil {
		return
	}
	defer DestroySession(sess)
	uploader := NewUploader(sess)
	f, err := os.Open("test.txt")
	if err != nil {
		fmt.Println("failed to open file", err)
		return
	}
	defer f.Close()
	fmt.Println("try to upload file with content: Hello ceph!")
	_, err = uploader.Upload(&s3manager.UploadInput{
		Bucket: aws.String("testbucket"),
		Key:    aws.String("test.txt"),
		Body:   f,
	})
	if err != nil {
		fmt.Println("failed to upload file", err)
		return
	}
	fmt.Println("file uploaded successfully")
	downloader := NewDownloader(sess)
	file, err := os.Create("test1.txt")
	if err != nil {
		fmt.Println("failed to create file", err)
		return
	}
	defer file.Close()
	_, err = downloader.Download(file,
		&s3.GetObjectInput{
			Bucket: aws.String("testbucket"),
			Key:    aws.String("test.txt"),
		})
	if err != nil {
		fmt.Println("failed to download file", err)
		return
	}
	// print the file content
	_, _ = file.Seek(0, 0)
	fmt.Println("down load file content:")
	buf := make([]byte, 1024)
	for {
		n, _ := file.Read(buf)
		if n == 0 {
			break
		}
		fmt.Print(string(buf[:n]))
	}
	fmt.Println()
	fmt.Println("==== test download end ====")
}

func concurrencyUpload(sess *session.Session, s int32, concurrency int, totalFileSize int, upload uploadType) {
	// 每个文件大小为参数s
	fileSize := int(s)
	// 计算文件数量
	fileCount := totalFileSize / fileSize
	// 计算每个节点需要上传的文件数量
	fileCountPerNode := fileCount / int(concurrency)
	if fileCount < concurrency {
		concurrency = fileCount
		fileCountPerNode = 1
	}
	// 计算最后一个节点需要上传的文件数量
	lastNodeFileCount := fileCount - fileCountPerNode*int(concurrency-1)
	// 创建一个WaitGroup
	var wg sync.WaitGroup
	// 创建10个goroutine并发上传文件

	for i := 0; i < concurrency; i++ {
		wg.Add(1)
		go func(i int) {
			defer wg.Done()
			uploader := NewUploader(sess)
			if i == concurrency-1 {
				upload(uploader, int(lastNodeFileCount), i)
			} else {
				upload(uploader, int(fileCountPerNode), i)
			}
		}(i)
	}
	// 等待所有goroutine上传完成
	wg.Wait()
}

func concurrencyDownload(sess *session.Session, s int32, concurrency int, totalFileSize int, download downloadType) {
	// 每个文件大小为参数s
	fileSize := int(s)
	// 计算文件数量
	fileCount := totalFileSize / fileSize
	// 计算每个节点需要上传的文件数量
	fileCountPerNode := fileCount / int(concurrency)
	if fileCount < concurrency {
		concurrency = fileCount
		fileCountPerNode = 1
	}
	// 计算最后一个节点需要上传的文件数量
	lastNodeFileCount := fileCount - fileCountPerNode*int(concurrency-1)
	// 创建一个WaitGroup
	var wg sync.WaitGroup
	// 创建10个goroutine并发上传文件
	for i := 0; i < concurrency; i++ {
		wg.Add(1)
		go func(i int) {
			defer wg.Done()
			downloader := NewDownloader(sess)
			if i == concurrency-1 {
				download(downloader, int(lastNodeFileCount), i)
			} else {
				download(downloader, int(fileCountPerNode), i)
			}
		}(i)
	}
	// 等待所有goroutine上传完成
	wg.Wait()
}

// 10 线程并发上传 1M 文件
func TestConcurrency1(t *testing.T) {
	sess := setupSession()
	if sess == nil {
		return
	}
	concurrency := 10
	totalFileSize := 1024 * 1024
	for i := 0; i <= 9; i++ {
		s := math.Pow(2, float64(i)) * 1024
		testConcurreny(int32(s), sess, concurrency, totalFileSize, SingleUpload, SingleDownload)
	}
	defer DestroySession(sess)
}

// 4M 文件 10-100 线程并发上传, block 为8K
func TestConcurrency2(t *testing.T) {
	sess := setupSession()
	if sess == nil {
		return
	}
	concurrency := 1
	totalFileSize := 4 * 1024 * 1024
	blockSize := 8 * 1024
	for i := 1; i <= 10; i++ {
		fmt.Println("number of threads:", concurrency*i)
		testConcurreny(int32(blockSize), sess, concurrency, totalFileSize, SingleUpload, SingleDownload)
		time.Sleep(1 * time.Second) // Sleep for 1 second to wait for resource release
	}
	defer DestroySession(sess)
}

// 尾延迟测试, 对冲请求
func TestConcurrency3(t *testing.T) {
	sess := setupSession()
	if sess == nil {
		return
	}
	concurrency := 10
	totalFileSize := 10 * 1024 * 1024
	blockSize := 4 * 1024
	testConcurreny(int32(blockSize), sess, concurrency, totalFileSize, SingleUploadWithTailProf, SingleDownloadWithTailProf)
	defer DestroySession(sess)
}

// 尾延迟测试, 无对冲请求
func TestConcurrency4(t *testing.T) {
	sess := setupSession()
	if sess == nil {
		return
	}
	concurrency := 10
	totalFileSize := 10 * 1024 * 1024
	blockSize := 4 * 1024
	testConcurreny(int32(blockSize), sess, concurrency, totalFileSize, SingleUpload, SingleDownload)
	defer DestroySession(sess)
}

func testConcurreny(blockSize int32, sess *session.Session, concurrency int, totalFileSize int, upload uploadType, download downloadType) {
	var begin int64
	var end int64
	createFiles(int(blockSize), concurrency, totalFileSize)
	//  记录开始时间
	begin = makeTimestamp()
	concurrencyUpload(sess, blockSize, concurrency, totalFileSize, upload)
	//  记录结束时间
	end = makeTimestamp()
	fmt.Println(blockSize/1024, "KB: concurrent upload time:", end-begin, "ms")
	err := os.Mkdir("data", os.ModePerm)
	if err != nil {
		return
	}
	begin = makeTimestamp()
	concurrencyDownload(sess, blockSize, concurrency, totalFileSize, download)
	end = makeTimestamp()
	fmt.Println(blockSize/1024, "KB: concurrent download time:", end-begin, "ms")

	err = os.RemoveAll("src")
	if err != nil {
		return
	}
	err = os.RemoveAll("data")
	if err != nil {
		return
	}
}

func SingleUploadWithTailProf(uploader *s3manager.Uploader, fileNum int, id int) {
	var wg sync.WaitGroup
	var wg2 sync.WaitGroup
	for i := 1; i <= fileNum; i++ {
		timeCh := make(chan int64, 1)
		resultCh := make(chan int64, 1)
		wg.Add(1)
		go func(i int) {
			go func() {
				defer wg.Done()
				file, err := os.Open(fmt.Sprintf("src/test%d_%d.txt", id, i))
				if err != nil {
					return
				}
				defer file.Close()
				begin := makeTimestamp()
				_, err = uploader.Upload(&s3manager.UploadInput{
					Bucket: aws.String("testbucket"),
					Key:    aws.String(fmt.Sprintf("src/test%d_%d.txt", id, i)),
					Body:   file,
				})
				end := makeTimestamp()
				if err != nil {
					return
				} else {
					resultCh <- end - begin
				}
			}()
			select {
			case result := <-resultCh:
				fmt.Printf("%-4d upload time: %-3d ms\n", id*fileNum+i, result)
			case <-time.After(150 * time.Millisecond):
				wg2.Add(1)
				go func(i int) {
					defer wg2.Done()
					file, err := os.Create(fmt.Sprintf("src/test%d_%d.txt", id, i))
					if err != nil {
						return
					}
					defer file.Close()
					begin := makeTimestamp()
					_, err = uploader.Upload(&s3manager.UploadInput{
						Bucket: aws.String("testbucket"),
						Key:    aws.String(fmt.Sprintf("src/test%d_%d.txt", id, i)),
						Body:   file,
					})
					end := makeTimestamp()
					if err != nil {
						return
					} else {
						timeCh <- end - begin + 150
					}
				}(i)
			}
		}(i)
		wg.Wait()
		wg2.Wait()
		// resp
		var resp int64 = math.MaxInt64
		select {
		case result, ok := <-resultCh:
			if ok {
				resp = result
			}
		default:
		}
		select {
		case t, ok := <-timeCh:
			if ok {
				resp = min(resp, t)
			}
		default:
		}
		close(resultCh)
		close(timeCh)
		if resp != math.MaxInt64 {
			fmt.Printf("%-4d upload time: %-3d ms\n", id*fileNum+i, resp)
		}
	}
	wg.Wait()
	wg2.Wait()
}
func SingleDownloadWithTailProf(downloader *s3manager.Downloader, fileNum int, id int) {
	var wg sync.WaitGroup
	var wg2 sync.WaitGroup
	for i := 1; i <= fileNum; i++ {
		timeCh := make(chan int64, 1)
		resultCh := make(chan int64, 1)
		wg.Add(1)
		go func(i int) {
			go func() {
				defer wg.Done()
				file, err := os.Create(fmt.Sprintf("data/test%d_%d.txt", id, i))
				if err != nil {
					return
				}
				defer file.Close()
				begin := makeTimestamp()
				_, err = downloader.Download(file,
					&s3.GetObjectInput{
						Bucket: aws.String("testbucket"),
						Key:    aws.String(fmt.Sprintf("src/test%d_%d.txt", id, i)),
					})
				end := makeTimestamp()
				if err != nil {
					return
				} else {
					resultCh <- end - begin
				}
			}()
			select {
			case result := <-resultCh:
				fmt.Printf("%-4d download time: %-3d ms\n", id*fileNum+i, result)
			case <-time.After(8 * time.Millisecond):
				wg2.Add(1)
				go func(i int) {
					defer wg2.Done()
					file, err := os.Open(fmt.Sprintf("data/test%d_%d.txt", id, i))
					if err != nil {
						return
					}
					defer file.Close()
					begin := makeTimestamp()
					_, err = downloader.Download(file,
						&s3.GetObjectInput{
							Bucket: aws.String("testbucket"),
							Key:    aws.String(fmt.Sprintf("src/test%d_%d.txt", id, i)),
						})
					end := makeTimestamp()
					if err != nil {
						return
					} else {
						timeCh <- end - begin + 8
					}
				}(i)
			}
		}(i)
		wg.Wait()
		wg2.Wait()
		// resp
		var resp int64 = math.MaxInt64
		select {
		case result, ok := <-resultCh:
			if ok {
				resp = result
			}
		default:
		}
		select {
		case t, ok := <-timeCh:
			if ok {
				resp = min(resp, t)
			}
		default:
		}
		if resp != math.MaxInt64 {
			fmt.Printf("%-4d download time: %-3d ms\n", id*fileNum+i, resp)
		}
		close(resultCh)
		close(timeCh)
	}
	wg.Wait()
	wg2.Wait()
}
func SingleUpload(u *s3manager.Uploader, fileNum int, id int) {
	for i := 1; i <= fileNum; i++ {
		f, err := os.Open(fmt.Sprintf("src/test%d_%d.txt", id, i))
		if err != nil {
			return
		}
		begin := makeTimestamp()
		_, err = u.Upload(&s3manager.UploadInput{
			Bucket: aws.String("testbucket"),
			Key:    aws.String(fmt.Sprintf("src/test%d_%d.txt", id, i)),
			Body:   f,
		})
		end := makeTimestamp()
		fmt.Printf("%-4d upload time: %-3d ms\n", id*fileNum+i, end-begin)
		if err != nil {
			f.Close()
			return
		}

	}
}

func SingleDownload(downloader *s3manager.Downloader, fileNum int, id int) {
	for i := 1; i <= fileNum; i++ {
		file, err := os.Create(fmt.Sprintf("data/test%d_%d.txt", id, i))
		if err != nil {
			return
		}
		begin := makeTimestamp()
		_, err = downloader.Download(file,
			&s3.GetObjectInput{
				Bucket: aws.String("testbucket"),
				Key:    aws.String(fmt.Sprintf("src/test%d_%d.txt", id, i)),
			})
		end := makeTimestamp()
		fmt.Printf("%-4d download time: %-3d ms\n", id*fileNum+i, end-begin)
		file.Close()
		if err != nil {
			return
		}
	}
}

func createFiles(s int, concurrency int, totalFileSize int) {
	err := os.Mkdir("src", os.ModePerm)
	if err != nil {
		return
	}
	// 每个文件大小为参数s
	fileSize := int(s)
	// 计算文件数量
	fileCount := totalFileSize / fileSize
	// 计算每个节点需要上传的文件数量
	fileCountPerNode := fileCount / int(concurrency)
	if fileCount < concurrency {
		concurrency = fileCount
		fileCountPerNode = 1
	}
	// 计算最后一个节点需要上传的文件数量
	lastNodeFileCount := fileCount - fileCountPerNode*int(concurrency-1)
	for c := 0; c < concurrency-1; c++ {
		for i := 0; i < fileCountPerNode; i++ {
			f, err := os.Create(fmt.Sprintf("src/test%d_%d.txt", c, i))
			if err != nil {
				return
			}
			_, err = f.Write(make([]byte, fileSize))
			if err != nil {
				f.Close()
				return
			}
			f.Close()
		}
	}
	for i := 0; i < lastNodeFileCount; i++ {
		f, err := os.Create(fmt.Sprintf("src/test%d_%d.txt", concurrency-1, i))

		if err != nil {
			return
		}
		_, err = f.Write(make([]byte, fileSize))
		if err != nil {
			f.Close()
			return
		}
		f.Close()

	}
}

func makeTimestamp() int64 {
	return time.Now().UnixNano() / int64(time.Millisecond)
}
