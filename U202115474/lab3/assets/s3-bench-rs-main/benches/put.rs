//! Put 请求测试

use criterion::async_executor::FuturesExecutor;
use criterion::{criterion_group, criterion_main, Criterion};
use reqwest::Url;
use s3_bench_rs::{PutTaskBuilder, Task, TaskBuiler};

const ENDPOINT: &str = "http://127.0.0.1:12345/auth/v1.0";
const KEY: &str = "chris:chris1234";
const SECRET: &str = "testing";
const BUCKET: &str = "user_uploads";
const OBJECT: &str = "test.txt";

async fn put() {
    let put_task_builder =
        PutTaskBuilder::new(ENDPOINT.parse::<Url>().unwrap(), KEY, SECRET, "minio");
    let task = put_task_builder.spawn(BUCKET, OBJECT);
    let _ = task.run().await;
}

use std::thread;
use tokio::task;
#[tokio::main]
async fn putn(n: usize) {
    let mut handles = vec![];
    for _ in 0..n {
        let handle = thread::spawn(move || async {
            let task = task::spawn(put());
            task
        });
        handles.push(handle);
    }

    // 等待所有线程完成
    for handle in handles {
        let _ = handle.join().unwrap().await;
    }
}
fn criterion_benchmark(c: &mut Criterion) {
    let mut c = c.benchmark_group("Async GetObject");
    c.measurement_time(std::time::Duration::new(10, 0));
    c.sample_size(10);
    for i in 1..=10 {
        c.bench_function(format!("Async PutObject withConcurrency:{}", i), move |b| {
            b.to_async(FuturesExecutor).iter(|| async {
                putn(i);
            })
        });
    }
}

criterion_group!(benches, criterion_benchmark);
criterion_main!(benches);
