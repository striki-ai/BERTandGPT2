docker build  -t docker-registry-internal.netcetera.com/nca-349-6/nca-public-qa:0.0.1-master --build-arg TAG=docker-registry-internal.netcetera.com/nca-349-6/nca-public-qa:0.0.1-master --build-arg VAR_VERSION=0.0.1 --build-arg VAR_BRANCH=master ./
docker push docker-registry-internal.netcetera.com/nca-349-6/nca-public-qa:0.0.1-master
