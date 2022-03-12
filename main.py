from Website import create_app

app = create_app()

#allow any changes in the program to be updated by refreshing the page
if __name__ == '__main__':
    app.run(debug=True)