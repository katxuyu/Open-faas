import json
from kafka import KafkaProducer
import logging



X_API_KEY = 'qQo/5QYrV2C6z/dzq3BT76msgynltWG4/uTw3kdyApU='

bootstrap_servers='pkc-56d1g.eastus.azure.confluent.cloud:9092'
security_protocol="SASL_SSL"
sasl_mechanism="PLAIN"
sasl_plain_username="QYE5N4VSJU4XM2FH"
sasl_plain_password="cyfQL6HUiExwcPI+QyoeYGQGZZC+PDis8WaAYiWMvhuYHFj6a6kc57pnDGoqUwVJ"



def send_payload(t, m):
    producer = KafkaProducer(bootstrap_servers='pkc-56d1g.eastus.azure.confluent.cloud:9092',
                             security_protocol="SASL_SSL",
                             sasl_mechanism="PLAIN",
                             sasl_plain_username="QYE5N4VSJU4XM2FH",
                             sasl_plain_password="cyfQL6HUiExwcPI+QyoeYGQGZZC+PDis8WaAYiWMvhuYHFj6a6kc57pnDGoqUwVJ",
                            value_serializer=lambda v: json.dumps(v).encode('utf-8')
                            )

    # producer = KafkaProducer(bootstrap_servers='20.24.19.71:9092',
    #                          security_protocol="SASL_SSL",
    #                          sasl_mechanism="PLAIN",
    #                          sasl_plain_username="admin",
    #                          sasl_plain_password="Qs9eqXV4x39b1HUitgsfuZSbLiY5MBOlmCiKbnRkddbQKzcVs8snh89uZEo3HWE",
    #                         value_serializer=lambda v: json.dumps(v).encode('utf-8')
    #                         )
    producer.send(t, key=b'foo', value=m)


def authorized(headers, app_id):
  print(headers)
  if ('x-api-key' in headers and headers.get('x-api-key') == X_API_KEY) or ('v3authorization' in headers and headers.get('v3authorization') == app_id):
    return True
  else:
    return False

def send_payload_to_kafka(client, category, payload):

  #payload = request.json
  if client == "pwxpayloads":
    temp_payload = payload
    full_message = {"category": category, "payload" : payload}
  else:
    temp_payload = payload['payload']
    full_message = payload

  if ("end_device_ids" in temp_payload and "application_ids" in temp_payload["end_device_ids"] and "uplink_message" in temp_payload) or category == 'INMARSAT':
    send_payload(client,full_message)
  else:
    print("Silently dropping invalid payload")

def handle(event, context):
  request = event
  if request.method == 'GET':
      return {
                "statusCode": 405,
                "body": "Method not allowed. You performed a GET request. You need to do a POST request with a JSON payload"
            }
  else:
      payload = json.loads((request.body).decode('utf-8'))
      application_id = payload["end_device_ids"]["application_ids"]["application_id"]
      if authorized(request.headers, application_id):
          send_payload_to_kafka("pwxpayloads", 'PACKETTHINGS', payload)
          return {
                "statusCode": 200,
                "body": {"message": "OK"},
                "headers": {
                    "Content-Type": "application/json"
                }
            }
      else:
          return {
              "statusCode": 401,
              "body": "Not Authorized"
          }


# def handle(event, context):
#     b =  (event.body).decode('utf-8')
#     b = json.loads(b)
#     return {
#         "statusCode": 200,
#         "body": {"message": f"Hello from OpenFaaS! {b['application_id']}"},
#         "headers": {
#             "Content-Type": "application/json"
#         }
#     }