# 循环执行10次测试, 分别保存在normal_{i}.log 和 prof_{i}.log 中
for i in {1..10}; do
    echo "Test $i"
    mkdir -p logs
    go test -v -run TestConcurrency4 demo -count=1 > logs/normal_$i.log
    go test -v -run TestConcurrency3 demo -count=1 > logs/prof_$i.log
    # sleep 5s to wait 
    sleep 5
done