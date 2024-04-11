//! Get 请求测试

use criterion::async_executor::FuturesExecutor;
use criterion::{criterion_group, criterion_main, Criterion};
use reqwest::Url;
use s3_bench_rs::{GetTaskBuilder, Task, TaskBuiler};

const ENDPOINT: &str = "http://127.0.0.1:12345/auth/v1.0";
const KEY: &str = "chris:chris1234";
const SECRET: &str = "testing";
const BUCKET: &str = "user_uploads";
const OBJECT: &str = "test.txt";
//#[tokio::main]
async fn get()  {
    let get_task_builder = GetTaskBuilder::new(
        ENDPOINT.parse::<Url>().expect("endpoint is a valid Url"),
        KEY,
        SECRET,
        "minio",
    );
    let task = get_task_builder.spawn(BUCKET, OBJECT);
    let _ = task.run().await;
}
use tokio::task;
use std::thread;
#[tokio::main]
async fn getn(n:usize){
    let mut handles = vec![];
    for _ in 0..n {
        let handle = thread::spawn(move || async {
            let task=task::spawn(get());
            task
        });
        handles.push(handle);
    }

    // 等待所有线程完成
    for handle in handles {
        let _=handle.join().unwrap().await;
    }
}
fn criterion_benchmark(c: &mut Criterion) {
    let mut c = c.benchmark_group("Async GetObject");
    c.measurement_time(std::time::Duration::new(10, 0));
    c.sample_size(10);
    c.bench_function("Async GetObject1", move |b| {
        b.to_async(FuturesExecutor).iter(|| async {
            getn(1);
        })
    });
    c.bench_function("Async GetObject2", move |b| {
        b.to_async(FuturesExecutor).iter(|| async {
            getn(2);
        })
    });
}

criterion_group!(benches, criterion_benchmark);
criterion_main!(benches);
