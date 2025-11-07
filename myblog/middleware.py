import time
from django.http import HttpResponseForbidden
# 自定义中间件，记录请求耗时
class LogMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        # 请求前记录时间
        start_time = time.time()

        # 继续处理请求->视图
        response = self.get_response(request)

        # 响应后计算耗时
        duration = time.time() - start_time
        print(f"[LOG] {request.method} {request.path} - 耗时{duration:.3f}s")

        return response
# 拦截请求（比如 IP 限制）
class IPBlockMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response
        self.blocked_ips = ['192.168.1.100']
        # self.blocked_ips = ['192.168.1.100', '127.0.0.1']
    def __call__(self, request):
        ip = self.get_client_ip(request)
        if ip in self.blocked_ips:
            return HttpResponseForbidden("您的IP被禁止访问！")
        return self.get_response(request)
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

# 给所有响应添加自定义头
class AddHeaderMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        response = self.get_response(request)
        response['X-Powered-By'] = 'MyBlog'
        return response

