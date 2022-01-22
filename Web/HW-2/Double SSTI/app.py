from flask import Flask, render_template_string, request, send_file

app = Flask(__name__)


@app.get("/")
def home():
    return """
    <h1>Stage 0x02</h1>
    <form method="POST">
        <input type="text" name="name" placeholder="Your name">
        <button>submit</button>
    </form>
    """


@app.post("/")
def welcome_message():
    name = request.form.get('name')
    if any(map(lambda word: word in name, ['__', '[', ']', '.', 'config'])):
        return "Hacker!"

    return render_template_string("<p>Hello, " + name + "</p>")


if __name__ == '__main__':
    app.run(threaded=True, debug=True)
