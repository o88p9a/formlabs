from app import create_app, create_kafka_producer

app = create_app()
app.config['KAFKA_PRODUCER'] = create_kafka_producer(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
