const API_URL = "http://localhost:3000/api"; // Zorg dat dit klopt met jouw backend

export async function fetchCommand(boxId) {
  const response = await fetch(`${API_URL}/command/${boxId}`);
  return response.json();
}

export async function updateCommand(boxId, command) {
  const response = await fetch(`${API_URL}/command/${boxId}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(command),
  });
  return response.text();
}
