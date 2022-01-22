const express = require('express');
const emojiMap = require('emojilib/simplemap.json')
const http = require("http");
const assert = require('assert');

const { FLAG } = require('./secret.js');

const app = express();
app.use(express.json());

app.get('/', (_, response) => {
    response.sendFile(__dirname + "/index.html");
});

app.get("/source", (_, response) => {
    response.sendFile(__filename);
});

app.post("/public_api", (request, response) => {
    const text = request.body.text.toString();

    if (!text.match(/^\S+$/) || text.includes(".")) {
        response.send({ error: "Bad parameter" });
        return;
    }

    const url = `http://127.0.0.1:7414/api/v1/emoji/${text}`;
    http.get(url, result => {
        result.setEncoding("utf-8");
        if (result.statusCode === 200)
            result.on('data', data => response.send(JSON.parse(data)));
        else
            response.send({ error: result.statusCode });
    });
});

// public server
app.listen(80, "0.0.0.0");


const apiServer = express();

const apiRouter = express.Router();
apiRouter.use('/emoji/:text', (req, res, next) => {
    const text = req.params.text;
    if (text in emojiMap) res.send({ result: emojiMap[text] });
    else res.send({ error: 'No such emoji.' });
});
apiRouter.use('/looksLikeFlag', (req, res, next) => {
    assert(FLAG.match(/^FLAG{[a-z0-9_]+}$/));

    res.send({ looksLikeFlag: FLAG.includes(req.query.flag) });
});
apiServer.use('/api/v1', apiRouter);

// local server
apiServer.listen(7414, "127.0.0.1");
