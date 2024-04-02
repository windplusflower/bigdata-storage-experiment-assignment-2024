# author: ZMY
# -d 后台运行 --volumes-from 数据卷容器
# host port 12345 to docker port 8080
run(){
    echo "Docker run Swift..."
    if docker ps -a | grep SWIFT_DATA; then
        docker start SWIFT_DATA
    else
        echo "First Run SWIFT_DATA "
        docker run -v /srv --name SWIFT_DATA busybox
    fi
    if docker ps -a | grep swift; then
        docker start swift
    else
        echo "First Run swift"
        docker run -d --name swift -p 12345:8080 --volumes-from SWIFT_DATA -t morrisjobke/docker-swift-onlyone
    fi
    echo docker ps | grep SWIFT_DATA
    echo docker ps | grep swift
}
stop(){
    echo "Docker stop Swift..."
    docker stop swift
    docker stop SWIFT_DATA
}
test_stat(){
    echo "Test Swift Status..."
    swift -A http://127.0.0.1:12345/auth/v1.0 -U test:tester -K testing stat
}
test_list(){
    echo "Test Swift list..."
    swift -A http://127.0.0.1:12345/auth/v1.0 -U test:tester -K testing list
}
test_connect(){
    echo "Test Swift connect..."
    echo "Upload test.txt and download test.txt"
    swift -A http://127.0.0.1:12345/auth/v1.0 -U test:tester -K testing upload swift test.txt
    swift -A http://127.0.0.1:12345/auth/v1.0 -U test:tester -K testing download swift test.txt
}
if [ "$1" = "run" ]; then
    run
elif [ "$1" = "stop" ]; then
    stop
elif [ "$1" = "test-stat" ]; then
    test_stat
elif [ "$1" = "test-list" ]; then
    test_list
elif [ "$1" = "test-connect" ]; then
    test_connect
elif [ "$1" = "test-all" ]; then 
    test_stat
    test_list
    test_connect
else
    echo "Usage: $0 run | stop | test-stat | test-list | test-connect | test-all"
    exit 1
fi