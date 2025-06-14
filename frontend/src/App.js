import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import LevelPage from "./pages/LevelPage";
import "./styles.css";
import "./fonts/JetBrainsMono.ttf";

function App() {
  return (
    <Router>
      <div className="container">
        <nav className="navbar">
          <Link to="/">Level Page</Link>
          <Link to="/profile">Profile Page</Link>
        </nav>

        <Routes>
          <Route path="/" element={<LevelPage />} />
          {/* <Route path="/profile" element={<ProfilePage />} /> */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
