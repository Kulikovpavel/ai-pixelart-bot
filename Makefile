login:
	gcloud auth login --project $(PROJECT)

deploy-webhook:
    cd webhook; gcloud beta functions deploy webhook --set-env-vars 'TELEGRAM_TOKEN=$(TELEGRAM_TOKEN)' 'PROJECT=$(PROJECT)' --runtime python37 --trigger-http

deploy-convert:
    cd convert; gcloud beta functions deploy convert --set-env-vars 'TELEGRAM_TOKEN=$(TELEGRAM_TOKEN)' 'PROJECT=$(PROJECT)' --runtime python37 --trigger-http

register:
	curl "https://api.telegram.org/bot$(TELEGRAM_TOKEN)/setWebhook?url=https://us-central1-$(PROJECT).cloudfunctions.net/webhook"
