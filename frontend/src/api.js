export async function askQuestion(question) {
  const response = await fetch("http://127.0.0.1:8000/query", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ question })
  });

  if (!response.ok) {
    throw new Error("Backend error");
  }

  return response.json();
}