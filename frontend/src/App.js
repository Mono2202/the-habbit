import React, { useState } from 'react';

function App() {
  const [response, setResponse] = useState(null);

  const sendData = async () => {
    try {
      const res = await fetch('http://localhost:5000/api/get_xp', {
        method: 'GET',
      });

      const result = await res.json();
      setResponse(result);
    } catch (err) {
      console.error('Error:', err);
      setResponse('Error sending data');
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>React → Flask API</h1>
      <button onClick={sendData}>Send Data</button>
      {response && <p>Response: {response["xp"]}</p>}
    </div>
  );
}

export default App;