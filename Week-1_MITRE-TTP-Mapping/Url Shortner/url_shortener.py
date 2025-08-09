from flask import Flask, request, redirect, render_template_string
import string

app = Flask(__name__)

# Base62 characters
BASE62 = string.ascii_letters + string.digits

# Dictionary to store URL mappings
url_mapping = {}
counter = 0

def encode(num):
    """Encode a number to a base62 string."""
    if num == 0:
        return BASE62[0]
    base = len(BASE62)
    encoded = []
    while num > 0:
        num, rem = divmod(num, base)
        encoded.append(BASE62[rem])
    return ''.join(reversed(encoded))

@app.route('/', methods=['GET', 'POST'])
def home():
    """Render the home page and handle URL shortening."""
    if request.method == 'POST':
        global counter
        long_url = request.form['url']
        counter += 1
        short_slug = encode(counter)
        url_mapping[short_slug] = long_url
        return render_template_string('''
            <style>
                body { font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 20px; }
                .container { max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 5px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }
                h1 { text-align: center; color: #333; }
                form { display: flex; flex-direction: column; }
                input[type="text"] { padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 5px; }
                button { padding: 10px; background-color: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer; }
                button:hover { background-color: #218838; }
                .result { margin-top: 20px; text-align: center; }
            </style>
            <div class="container">
                <h1>URL Shortener</h1>
                <form action="/" method="POST">
                    <input type="text" id="url" name="url" placeholder="Enter your long URL here" required>
                    <button type="submit">Shorten</button>
                </form>
                <div class="result">
                    <h2>Shortened URL:</h2>
                    <a href="/{{ short_slug }}">/{{ short_slug }}</a>
                </div>
            </div>
        ''', short_slug=short_slug)
    
    return '''
        <style>
            body { font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 20px; }
            .container { max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 5px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }
            h1 { text-align: center; color: #333; }
            form { display: flex; flex-direction: column; }
            input[type="text"] { padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 5px; }
            button { padding: 10px; background-color: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer; }
            button:hover { background-color: #218838; }
        </style>
        <div class="container">
            <h1>URL Shortener</h1>
            <form action="/" method="POST">
                <input type="text" id="url" name="url" placeholder="Enter your long URL here" required>
                <button type="submit">Shorten</button>
            </form>
        </div>
    '''

@app.route('/<slug>')
def redirect_to_url(slug):
    """Redirect to the original URL based on the slug."""
    original_url = url_mapping.get(slug)
    if original_url:
        return redirect(original_url)
    return "URL not found", 404

if __name__ == '__main__':
    app.run(debug=True)
