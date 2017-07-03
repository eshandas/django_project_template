from django.conf.urls import url

from .views import (
    AllLogs,
    AllRequestLogs,
    AllEventLogs,
    TestLogs,
    TestRequestLogs,
    TestEventLogs,
)

urlpatterns = [
    url(r'^all/$', AllLogs.as_view(), name='all_logs'),
    url(r'^requests/all/$', AllRequestLogs.as_view(), name='all_request_logs'),
    url(r'^events/all/$', AllEventLogs.as_view(), name='all_event_logs'),
    url(r'^test/$', TestLogs.as_view(), name='test'),
    url(r'^requests/test/$', TestRequestLogs.as_view(), name='request_test'),
    url(r'^events/test/$', TestEventLogs.as_view(), name='event_test'),
]
