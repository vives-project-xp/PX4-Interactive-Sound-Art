import express from 'express';
import cors from 'cors';

const app = express();

app.use(cors());
app.use(express.json());

// In-memory opslag voor commando's per box
const boxCommands = {};

// Endpoint: Update commando voor een specifieke box
app.post('/api/command/:boxId', (req, res) => {
  const boxId = req.params.boxId;
  const command = req.body;
  boxCommands[boxId] = command;
  console.log(`Commando voor box ${boxId} bijgewerkt:`, command);
  res.status(200).send(`Commando voor box ${boxId} bijgewerkt.`);
});

// Endpoint: Haal het huidige commando op voor een specifieke box
app.get('/api/command/:boxId', (req, res) => {
  const boxId = req.params.boxId;
  const command = boxCommands[boxId] || {};
  res.json(command);
});

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server draait op http://localhost:${port}`);
});
