use std::{fs::File, io::{self, Write}, path::{Path, PathBuf}, str::FromStr};

use aws_sdk_s3::{error::SdkError, primitives::ByteStream, Client, Error};
use aws_credential_types::{provider::SharedCredentialsProvider, Credentials};
use aws_sdk_s3::operation::{create_bucket::CreateBucketOutput, create_bucket::CreateBucketError, 
                            put_object::PutObjectOutput, put_object::PutObjectError};

const ACCESS_KEY_ID: &str = "swift123:swift123";
const SECRET_ACCESS_KEY: &str = "swift_key";

async fn create_s3_client(show_config:bool) -> Client {
//     let access_key_id = "swift123:swift123";
//     let secret_access_key = "swift_key";
    
    let config = aws_config::from_env()
        .endpoint_url("http://127.0.0.1:12345".to_string())
        .credentials_provider(SharedCredentialsProvider::new(Credentials::from_keys(
            ACCESS_KEY_ID.to_string(),
            SECRET_ACCESS_KEY.to_string(),
            None,
        )))
        .load()
        .await;
    let s3_local_config = aws_sdk_s3::config::Builder::from(&config).build();
    if show_config {
        println!("{:#?}", s3_local_config);
    }
    let client = Client::from_conf(s3_local_config);
    return client;
}

async fn show_all_buckets(client:&Client) -> Result<(), Error>{
    let resp = client.list_buckets().send().await?;
    println!("Found {} buckets", resp.buckets().len());
    for bucket in resp.buckets() {
        println!("{}", bucket.name().unwrap_or_default());
    }
    Ok(())
}

async fn list_objects(client:&Client, bucket:&str) -> Result<(), Error> {
    let mut resp = client.list_objects_v2()
        .bucket(bucket.to_owned())
        .max_keys(50)
        .into_paginator().send();
    while let Some(result) = resp.next().await {
        match result {
            Ok(output) => {
                for object in output.contents() {
                    println!(" - {}", object.key().unwrap_or("Unknown"));
                }
            }
            Err(err) => {
                eprintln!("{err:?}");
            }
        }
    }
    Ok(())
}

async fn create_bucket(
    client: &Client,
    bucket_name: &str,
    region: &str,
) -> Result<CreateBucketOutput, SdkError<CreateBucketError>> {
    let constraint = aws_sdk_s3::types::BucketLocationConstraint::from(region);
    let cfg = aws_sdk_s3::types::CreateBucketConfiguration::builder()
        .location_constraint(constraint)
        .build();
    client
        .create_bucket()
        .create_bucket_configuration(cfg)
        .bucket(bucket_name)
        .send()
        .await
}

async fn delete_bucket(client: &Client, bucket_name: &str) -> Result<(), Error> {
    client.delete_bucket().bucket(bucket_name).send().await?;
    println!("Bucket deleted!");
    Ok(())
}

async fn upload_object(
    client: &Client,
    bucket_name: &str,
    file_name: &str,
    key: &str,
) -> Result<PutObjectOutput, SdkError<PutObjectError>> {
    let body = ByteStream::from_path(Path::new(file_name)).await;
    client
        .put_object()
        .bucket(bucket_name)
        .key(key)
        .body(body.unwrap())
        .send()
        .await
}

async fn get_object(client: &Client, bucket: &str, object: &str, destination: PathBuf) -> Result<usize, anyhow::Error> {

    let mut file = File::create(destination)?;

    let mut object = client
        .get_object()
        .bucket(bucket)
        .key(object)
        .send()
        .await?;

    let mut byte_count = 0_usize;
    while let Some(bytes) = object.body.try_next().await? {
        let bytes_len = bytes.len();
        file.write_all(&bytes)?;
        //trace!("Intermediate write of {bytes_len}");
        byte_count += bytes_len;
    }

    Ok(byte_count)
}

async fn remove_object(client: &Client, bucket: &str, key: &str) -> Result<(), Error> {
    client.delete_object()
        .bucket(bucket)
        .key(key)
        .send().await?;
    println!("Object deleted!");
    Ok(())
}

fn get_target_type(target_name: &str) -> i32 {
    match target_name {
        "bucket" => { 0 }
        "object" => { 1 }
        _ => {
            println!("Error: Invalid Target Type, try bucket or object!");
            -1
        }
    }
}

#[tokio::main]
async fn main() -> Result<(), Error> {
    let client = create_s3_client(false).await;
    show_all_buckets(&client).await?;
    let _region: &str = "us-east-1";
    println!("Input help for help!");
    loop {
        let mut input = String::new();
        io::stdin().read_line(&mut input).expect("Failed to read the input!");
        // 去掉两端空格
        let input = input.trim();
        let args: Vec<&str> = input.split_whitespace().collect();
        let command = match args.get(0) {
            Some(cmd) => *cmd,
            None => {
                println!("No command read.");
                continue;
            }
        };
        //println!("{input}");
        match command {
            "quit" => {
                println!("Exiting the Aws terminal ...");
                break;
            }
            "help" => {
                println!("Please read the loop part in the main.rs.");
                println!("create : create bucket [bucket_name] \n// create a bucket named [bucket_name].");
                println!("         create object [bucket_name] [local_object_path] [object_key] \n// create an object in [bucket_name] named [object_key] from [local_object_path].");
                println!("read   : read [bucket_name] [object_key] [output_file_path] \n// read the [object_key] in [bucket_name] to the local [output_file_path].");
                println!("delete : delete bucket [bucket_name] \n// delete the bucket named [bucket_name].");
                println!("       : delete object [bucket_name] [object_key] \n// delete the [object_key] in the [bucket_name].");
                println!("ls     : ls \n// list all the buckets.");
                println!("lso    : lso [bucket_name] \n// list all the objects(max 50) in the [bucket_name].");
            }
            "create" => {
                let target_name = match args.get(1) {
                    Some(typ) => *typ,
                    None => {
                        println!("Error: You need to specify the operation target type!");
                        continue;
                    }
                };
                let target_type: i32 = get_target_type(target_name);
                if target_type == -1 {continue;}
                let bucket_name = match args.get(2) {
                    Some(name) => *name,
                    None => {
                        println!("Error: You need to give the bucket name!");
                        continue;
                    }
                };
                if target_type == 0 { // bucket
                    create_bucket(&client, bucket_name, _region).await?;
                    println!("Bucket created!");
                } else if target_type == 1 { // object
                    let file_path = match args.get(3) {
                        Some(path) => *path,
                        None => {
                            println!("Error: You need to give the object path!");
                            continue;
                        }
                    };
                    let key = match args.get(4) {
                        Some(key) => *key,
                        None => {
                            println!("Error: You need to give the object key!");
                            continue;
                        }
                    };
                    upload_object(&client, bucket_name, file_path, key).await?;
                    println!("Object created!");
                }
            }
            "read" => { // read objects from one bucket
                let bucket = match args.get(1) {
                    Some(name) => *name,
                    None => {
                        println!("Error: You need to give the bucket name!");
                        continue;
                    }
                };
                let object = match args.get(2) {
                    Some(key) => *key,
                    None => {
                        println!("Error: You need to give the object key!");
                        continue;
                    }
                };
                let destination = match args.get(3) {
                    Some(path) => PathBuf::from_str(*path),
                    None => {
                        println!("Error: You neef to give the output file path!");
                        continue;
                    }
                };
                if let  Ok(dest) = destination {
                    match get_object(&client, bucket, object, dest).await {
                        Ok(bytes_write) => {
                            println!("Wrote {bytes_write} to the file.");
                        }
                        Err(err) => {
                            eprintln!("Error: {}", err);
                        }
                    }
                }
                
            }
            // "update" => {

            // }
            "delete" => {
                let target_name = match args.get(1) {
                    Some(typ) => *typ,
                    None => {
                        println!("Error: You need to specify the operation target type!");
                        continue;
                    }
                };
                let target_type: i32 = get_target_type(target_name);
                if target_type == -1 {continue;}
                let bucket_name = match args.get(2) {
                    Some(name) => *name,
                    None => {
                        println!("Error: You need to give the bucket name!");
                        continue;
                    }
                };
                if target_type == 0 {
                    delete_bucket(&client, bucket_name).await?;
                } else if target_type == 1 {
                    let key = match args.get(3) {
                        Some(key) => *key,
                        None => {
                            println!("Error: You need to give the key of the object!");
                            continue;
                        }
                    };
                    remove_object(&client, bucket_name, key).await?;
                    
                }
            }
            "ls" => { // list all buckets
                println!("Listing all the buckets.");
                show_all_buckets(&client).await?;
            }
            "lso" => { // list objects
                let bucket_name = match args.get(1) {
                    Some(name) => *name,
                    None => {
                        println!("Error: you need to specify the bucket name!");
                        continue;
                    }
                };
                println!("Listing the objects in the bucket: {}", bucket_name);
                list_objects(&client, bucket_name).await?;
            }
            _ => {
                println!("Invalid command: {}", command);
            }
        }
    }

    Ok(())
}
