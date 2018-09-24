import cache
from config.config import get_cfg_serviceid
from resources.global_resources.variables import serviceType
from log.save_log import save_log_item


logTimeFormat = '%Y/%m/%d %H.%M.%S.%f'


def logging_service():
    while True:
        #
        item = cache.logQ.get()
        #
        item['timestamp'] = item['timestamp'].strftime(logTimeFormat)
        item['service_id'] = get_cfg_serviceid()
        item['service_type'] = serviceType
        #
        save_log_item(item)

# Standard logging values:
# - timestamp
# - service_id
# - service_type
# - process (internal/inbound/outbound)
# - result
# - description
# - exception [optional]

# Internal requests
# - operation

# Inbound requests
# - client_ip
# - client_user
# - server_ip
# - server_port
# - server_method
# - server_request_uri
# - server_request_query
# - server_request_body
# - http_response_code

# Outbound requests
# - service_ip
# - service_port
# - service_method
# - service_request_uri
# - service_request_query
# - service_request_body
# - http_response_code
