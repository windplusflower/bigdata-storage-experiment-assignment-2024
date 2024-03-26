//! Get 请求测试

use criterion::async_executor::FuturesExecutor;
use criterion::{criterion_group, criterion_main, Criterion};
use reqwest::Url;
use s3_bench_rs::{GetTaskBuilder, StdError, Task, TaskBuiler};

const ENDPOINT: &str = "http://127.0.0.1:9000";
const KEY: &str = "admin";
const SECRET: &str = "password";
const BUCKET: &str = "myminio";
const OBJECT: &str = "wzy/minio.exe";
#[tokio::main]
async fn get() -> Result<String, Box<StdError>> {
    let get_task_builder = GetTaskBuilder::new(
        ENDPOINT.parse::<Url>().expect("endpoint is a valid Url"),
        KEY,
        SECRET,
        "minio",
    );
    let task = get_task_builder.spawn(BUCKET, OBJECT);
    let text = task.run().await?;
    Ok(text)
}

fn criterion_benchmark(c: &mut Criterion) {
    c.bench_function("Async GetObject", move |b| {
        b.to_async(FuturesExecutor).iter(|| async {
            let _ret = get();
        })
    });
}

criterion_group!(benches, criterion_benchmark);
criterion_main!(benches);
