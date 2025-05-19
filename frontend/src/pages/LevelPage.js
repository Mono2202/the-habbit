import React, { useEffect, useState } from "react";
import PhotoGallery from "../components/PhotoGallery";
import './LevelPage.css';

function LevelPage() {
  const level = 5;
  const xpToNextLevel = 50;

  const [user_xp, setUserXP] = useState(0);
  const [percentage, setPercentage] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getUserXP();
  });

  async function getUserXP() {
    try {
        const result = await fetch(process.env.REACT_APP_BACKEND_URL + "/api/get_xp");
        const json_result = await result.json();
        setUserXP(json_result["xp"]);
        setPercentage((user_xp / xpToNextLevel) * 100);
    } catch (err) {
        console.error("Error:", err);
    } finally {
        setLoading(false);
    }
  }

  if (loading) {
    return <div>Loading...</div>
  }

  else {
    return (
        <>
        <div className="level-page">
        <img
            src="https://art.pixilart.com/7b2d1341e20f674.png"
            alt="Profile"
            className="profile-pic"
        />
        <h2>Level {level}</h2>
        <div className="progress-container">
            <div className="progress-bar" style={{ width: `${percentage}%` }}></div>
        </div>
        <p>{user_xp} / {xpToNextLevel} XP</p>
        </div>

        <div><PhotoGallery /></div>
        </>
    );
  }
}

export default LevelPage;
