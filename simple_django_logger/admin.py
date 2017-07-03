from django.contrib import admin

from .models import (
    Log,
    RequestLog,
    EventLog,
)


class LogAdmin(admin.ModelAdmin):
    readonly_fields = [
        'log_level', 'request_url', 'request_method', 'get_data',
        'request_body', 'cookies', 'meta',
        'exception_type', 'message', 'stack_trace', 'user_id',
        'user_name', 'request_browser', 'request_os', 'request_device',
        'response_body', 'response_status', 'response_headers', 'response_content_type',
        'is_mobile', 'is_tablet', 'is_touch_capable', 'is_pc',
        'is_bot', 'created_on']

    def has_add_permission(self, request):
        return False


class RequestLogAdmin(admin.ModelAdmin):
    readonly_fields = [
        'method', 'url', 'request_data', 'request_headers',
        'response_text', 'response_status', 'response_reason',
        'response_time', 'created_on']

    def has_add_permission(self, request):
        return False


class EventLogAdmin(admin.ModelAdmin):
    readonly_fields = [
        'log_level', 'message', 'stack_trace', 'tag',
        'created_on']

    def has_add_permission(self, request):
        return False


admin.site.register(Log, LogAdmin)
admin.site.register(RequestLog, RequestLogAdmin)
admin.site.register(EventLog, EventLogAdmin)
