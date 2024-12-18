#!/bin/bash

# 默认服务器
SERVER=${1:-mydev}

# 检查服务器配置是否存在
if ! ssh -q $SERVER exit; then
    echo "错误：无法连接到服务器 $SERVER"
    exit 1
fi

echo "正在部署到服务器: $SERVER"

# 同步代码到服务器
rsync -avz --progress \
    --exclude '__pycache__' \
    --exclude '*.pyc' \
    --exclude '.DS_Store' \
    --exclude 'divination.log' \
    ./ $SERVER:/root/divination/

if [ $? -ne 0 ]; then
    echo "错误：文件同步失败"
    exit 1
fi

# SSH到服务器重启服务
ssh $SERVER "cd /root/divination && echo '停止旧服务...' && pkill -f 'uvicorn web:app'"
ssh $SERVER "cd /root/divination && echo '启动新服务...' && nohup uvicorn web:app --host 0.0.0.0 --port 8001 > divination.log 2>&1 &"
