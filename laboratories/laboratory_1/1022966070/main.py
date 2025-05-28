from notification_system.adapters.primary.web.flask_app import create_app
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)