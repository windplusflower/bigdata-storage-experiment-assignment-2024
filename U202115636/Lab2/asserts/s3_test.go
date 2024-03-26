package main

import (
	"fmt"
	"os"
	"testing"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/s3"
	"github.com/aws/aws-sdk-go/service/s3/s3manager"
)

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
	fmt.Printf("bucket created successfully\n\n")
	return sess
}

func DestroySession(sess *session.Session) {
	svc := s3.New(sess)
	fmt.Printf("\nDestroying test session\n")
	fmt.Printf("deleting bucket with name of testbucket\n")
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
	}else {
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
	fmt.Println("try to upload file with content: Hello ceph!")
	defer f.Close()
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
