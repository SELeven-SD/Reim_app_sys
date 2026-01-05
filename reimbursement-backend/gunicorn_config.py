bind = "0.0.0.0:8000"
# 增加worker数量，建议为CPU核心数的一半
workers = 16
# 使用gevent异步worker以支持更多并发连接
worker_class = "gevent"
# 每个worker的最大并发连接数（gevent模式下）
worker_connections = 1000
# 定期重启worker以防止内存泄漏
max_requests = 1000
max_requests_jitter = 50
# 超时时间
timeout = 30
# 日志配置
accesslog = "-"
errorlog = "-"
loglevel = "info"
