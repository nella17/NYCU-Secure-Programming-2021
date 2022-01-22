const { response } = require('express');
const express = require('express');
const handlebars = require('handlebars');
const { createProxyMiddleware } = require('http-proxy-middleware');
const { secret } = require('./secret.js');

const app = express();

// Proxy endpoints
// Try to figure out the path!
app.use(`/2nd_stage_${secret}`, createProxyMiddleware({
    target: "http://jinja",
    changeOrigin: true,
    pathRewrite: {
        [`^/2nd_stage_${secret}`]: '',
    },
}));

app.get("/source", (_, response) => {
    response.sendFile(__filename);
});

app.get('/', (_, response) => {
    response.sendFile(__dirname + "/index.html");
});

app.get("/welcome", (request, response) => {
    const name = request.query.name ?? 'Guest';
    if (name.includes('secret')) {
        response.send("Hacker!");
        return;
    }
    const template = handlebars.compile(`<h1>Hello ${name}! SSTI me plz.</h1>`);
    response.send(template({ name, secret }));
})


app.listen(3000, '0.0.0.0');
