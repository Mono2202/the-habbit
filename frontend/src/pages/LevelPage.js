import React, { useEffect, useState } from "react";
import PhotoGallery from "../components/PhotoGallery";
import LoadingWheel from "../components/LoadingWheel";
import './LevelPage.css';

function LevelPage() {
  const [xp, setXP] = useState(0);
  const [percentage, setPercentage] = useState(0);
  const [goal_xp, setGoalXP] = useState(50);
  const [level, setLevel] = useState(0);

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getXP();
  }, []);

  async function getXP() {
    try {
        const xp_result = await fetch(process.env.REACT_APP_BACKEND_URL + "/api/xp/get_xp");
        const xp_result_json = await xp_result.json();
        setXP(xp_result_json["xp"]);

        const goal_xp_result = await fetch(process.env.REACT_APP_BACKEND_URL + "/api/xp/get_goal_xp");
        const goal_xp_result_json = await goal_xp_result.json();
        setGoalXP(goal_xp_result_json["goal_xp"]);

        const level_result = await fetch(process.env.REACT_APP_BACKEND_URL + "/api/xp/get_level");
        const level_result_json = await level_result.json();
        setLevel(level_result_json["level"]);

        setPercentage((xp_result_json["xp"] / goal_xp_result_json["goal_xp"]) * 100);
    } catch (err) {
        console.error("Error:", err);
    } finally {
        setLoading(false);
    }
  }

  if (loading) {
    return <LoadingWheel />
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
        <p>{xp} / {goal_xp} XP</p>
        </div>

        {/* <div><PhotoGallery /></div> */}
        </>
    );
  }
}

export default LevelPage;
