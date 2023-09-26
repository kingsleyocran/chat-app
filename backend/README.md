# Backend Workflow for Chat App

Welcome to the backend part of the Chat App project. This section provides an overview of the key components and steps required to set up and run the backend services.

## Table of Contents

- [Backend Workflow for Chat App](#backend-workflow-for-chat-app)
  - [Table of Contents](#table-of-contents)
  - [Dependencies](#dependencies)
  - [Documentation](#documentation)
  - [Services](#services)
  - [Streams](#streams)
  - [Tech Stacks](#tech-stacks)
  - [Admin Panel Sample](#admin-panel-sample)
  - [Starting the Application](#starting-the-application)
    - [Troubleshooting](#troubleshooting)

![Backend Workflow](https://github.com/kingsleyocran/chat-app/blob/development/resources/backend_workflow.jpg)

## Dependencies

The `dependencies` directory contains other applications and services that support the functionality of the backend. It includes Docker configurations to simplify the setup process.

## Documentation

The `docs` folder contains code documentation for the backend codebase, which can be helpful for understanding the structure and functionality of the code.

## Services

The `services` directory encompasses backend services such as APIs, Websockets, and plugins that interact with other services. These services play a crucial role in handling various aspects of the Chat App.

## Streams

The `streams` directory includes Kafka Stream connectors and KSQL stream queries. These components facilitate data streaming and processing within the Chat App.

## Tech Stacks

![Tech Stack](https://github.com/kingsleyocran/chat-app/blob/development/resources/resources.jpg)

## Admin Panel Sample

Here's a sample screenshot of the admin panel, providing an overview of the application's functionality:

![Admin Panel](https://github.com/kingsleyocran/chat-app/blob/development/resources/admin_panel.png)

## Starting the Application

Before starting the application, please ensure you have Docker installed, as well as at least 12GB of available storage space.

1. Navigate to the `dependencies` directory or folder and run the following command to start the required services:

   ```bash
   $ docker compose -f docker-compose-dependency.yaml up
   ```

2. In the `streams` directory, perform the following steps:

   - Send a POST request to the Kafka Connect service using the sink connector JSON file:

     ```bash
     $ curl --location 'http://localhost:9095/connectors/' --header 'Content-Type: application/json' --data '{
         "name": "elasticsearch-sink",
         "config": {
             "connector.class": "io.confluent.connect.elasticsearch.ElasticsearchSinkConnector",
             "tasks.max": "1",
             "topics": "elasticsearch_users",
             "connection.url": "http://elasticsearch:9200",
             "type.name": "_doc",
             "key.converter": "org.apache.kafka.connect.storage.StringConverter",
             "value.converter": "org.apache.kafka.connect.json.JsonConverter",
             "value.converter.schemas.enable": "false",
             "schema.ignore": "true",
             "key.ignore": "false",
             "write.method": "UPSERT",
             "transforms": "Cast",
             "transforms.Cast.type": "org.apache.kafka.connect.transforms.Cast$Key",
             "transforms.Cast.spec": "string"
         }
     }'
     ```

   - Send a POST request to the Kafka Connect service using the source connector JSON file:

     ```bash
     $ curl --location 'http://localhost:9095/connectors/' --header 'Content-Type: application/json' --data '{
     	 	"name": "postgres-source-connector",
     		"config": {
     			"connector.class": "io.debezium.connector.postgresql.PostgresConnector",
             	"tasks.max": "1",
                 "database.hostname": "postgres",
                 "database.port": "5432",
                 "database.user": "admin",
                 "database.password": "admin",
                 "database.dbname": "chat_app_database",
                 "database.server.id": "184054",
                 "topic.prefix": "users_topic",
                 "schema.history.internal.kafka.bootstrap.servers": "kafka:9092",
                 "schema.history.internal.kafka.topic": "schema-changes.chat_app_database",
     			"value.converter": "io.apicurio.registry.utils.converter.AvroConverter",
      			"value.converter.apicurio.registry.url": "http://apicurio:8080/apis /registry/v2",
                 "value.converter.apicurio.registry.auto-register": true,
                 "value.converter.apicurio.registry.find-latest": true,
                 "value.converter.apicurio.registry.as-confluent": true,
                 "value.converter.apicurio.registry.use-id": "contentId",
                 "value.converter.apicurio.registry.headers.enabled": false
       }
     }'
     ```

     **Note:** Before sending the POST request for the sink connector, ensure you have downloaded the Elasticsearch connector JAR file. You can copy the JAR file to Kafka Connect using the following command:

     ```bash
     docker cp {elasticsearch connector JAR lib folder} kafka_connect:/kafka/lib
     ```

3. Enter the ksqlDB server using the following command:

   ```bash
   docker compose exec -it ksql_server bash ksql
   ```

4. Copy the contents of the `streams.sql` file located in the `sql` directory and paste it into the ksqlDB console.

### Troubleshooting

If you encounter any issues during setup or operation, you can check the logs of the dependency services by running the following command:

```bash
docker compose logs -f {service name}
```

For addressing an Elasticsearch disk threshold error, you can use the following command:

```bash
curl -XPUT -H "Content-Type: application/json" http://localhost:6383/_cluster/settings -d '{
    "transient": {
        "cluster.routing.allocation.disk.threshold_enabled": false
    }
}'
```

This command disables the Elasticsearch disk threshold to resolve the issue.

That's it! You should now have the backend of the Chat App up and running. If you have any further questions or issues, please refer to the documentation or reach out to the project maintainers.