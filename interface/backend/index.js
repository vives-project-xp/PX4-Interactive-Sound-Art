import express from "express";
import cors from "cors";
import axios from "axios";

const app = express();
const PORT = 4000;

app.use(cors());
app.use(express.json());

// Store commands per box
const commands = {};

// GET: Retrieve current command for a box
app.get("/command/:boxId", (req, res) => {
    const { boxId } = req.params;
    res.json(commands[boxId] || { instrument: "", color: "", effect: "" });
});

// POST: Update command for a box and send it to the RPi
app.post("/command/:boxId", async (req, res) => {
    const { boxId } = req.params;
    const { instrument, color, effect } = req.body;
    
    commands[boxId] = { instrument, color, effect };
    console.log(`✅ Updated ${boxId}:`, commands[boxId]);

    // Send command to Raspberry Pi (Replace with actual IP of RPi)
    const raspberryPiIP = "http://192.168.1.100:5000"; // Change this!
    try {
        await axios.post(`${raspberryPiIP}/update`, commands[boxId]);
        console.log(`✅ Sent to Raspberry Pi:`, commands[boxId]);
    } catch (error) {
        console.error("❌ Failed to send command to Raspberry Pi", error.message);
    }

    res.json({ message: "Command updated successfully", command: commands[boxId] });
});

// Start server
app.listen(PORT, "0.0.0.0", () => {
    console.log(`🚀 Backend running on http://0.0.0.0:${PORT}`);
});
