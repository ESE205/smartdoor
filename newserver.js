const express = require('express');
const app = express();
const bodyParser = require('body-parser');
app.use(bodyParser.json());
const MessagingResponse = require('twilio').twiml.MessagingResponse;

let i = 0;

let access = [];

let map = {};

app.get('/textuser/:photoName', async (req,res) => {

access[i] = 'pending';
map[req.params.photoName] = i;
console.log('texting for authorization with photo ${req.params.photoName}');
const accountSid = '###';
const authToken = '###';
const client = require('twilio')(accountSid, authToken);

const message = await client.messages
    .create({
        body: 'This person is at your door, do you want to let them in?',
        from: '###',
        mediaUrl: 'static ip',
        to: '###'
    });

console.log(message.sid);
res.send("OK");

});

app.post('/sms', (req,res) => {
    const twiml = new MessagingResponse();

    twiml.message('Thank you for your response.  The visitor is being informed of your decision');

    res.writeHead(200, {'Content-Type': 'text/xml'});
    acces[i] = 'approved';
    i++;
    res.end(twiml.toString());

});

app.get('/accessstatus/:filename', async (req, res) => {

    res.json({
        "status": access[map[req.params.filename]]
    });

});

app.listen(1337);

