import express from "express";
import axios from "axios";
import cors from "cors";


const app = express();
app.use(express.json());

app.use(cors());

app.post("/ia", async (req, res) => {
  try {
    const { text } = req.body;
    if (!text) {
      return res.status(400).send("Texto não fornecido");
    }

    const response = await axios.post("http://localhost:11434/api/generate", {
      model: "llama3.2",
      prompt: text,
      stream: false,
    });

    const respData = response.data.response.toString();
    res.send(respData);
  } catch (error) {
    console.error("Erro ao chamar a API:", error);
    res.status(500).send("Erro no servidor ao processar a IA");
  }
});

app.listen(7000, () => {
  console.log("Server running on port 7000");
});
