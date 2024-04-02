    docker build -t openstack-swift-docker 


    docker run -v /srv --name SWIFT_DATA busybox


    docker run -d --name openstack-swift -p 12345:8080 --volumes-from SWIFT_DATA -t openstack-swift-docker


    docker ps


    pip install python-swiftclient安装库


    swift -A http://127.0.0.1:12345/auth/v1.0 -U test:tester -K testing stat