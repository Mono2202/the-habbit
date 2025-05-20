import React, { useEffect, useState } from "react";
import { PICTURES } from '../consts/ImageFiles';
import PhotoGallery from "../components/PhotoGallery";
import LoadingWheel from "../components/LoadingWheel";
import './LevelPage.css';

function LevelPage() {
  const [user_info, setUserInfo] = useState({
    xp: 0,
    percentage: 0,
    xp_goal: 50,
    level: 0,
  });

  const [loading, setLoading] = useState(true);

  const [selectedPhoto, setSelectedPhoto] = useState(null);

  useEffect(() => {
    getXP();

    const interval = setInterval(getXP, 5000);
    return () => clearInterval(interval);
  }, []);

  async function getXP() {
    try {
        const user_info_result = await fetch(process.env.REACT_APP_BACKEND_URL + "/api/xp/get_user_info");
        const user_info_result_json = await user_info_result.json();
        setUserInfo({
          xp: user_info_result_json["xp"],
          xp_goal: user_info_result_json["xp_goal"],
          level: user_info_result_json["level"],
          percentage: (user_info_result_json["xp"] / user_info_result_json["xp_goal"]) * 100,
        });

    } catch (err) {
        console.error("Error:", err);
    } finally {
        setLoading(false);
    }
  }
  
  useEffect(() => {
    if (selectedPhoto == null) {
      const filteredPics = PICTURES.filter(pic => {
        const levelNumber = parseInt(pic.split('_')[0].split('/').at(-1));
        return levelNumber === (parseInt(user_info.level));
      });
      setSelectedPhoto(filteredPics[0]);
    }
  }, [selectedPhoto, user_info.level])

  const handlePhotoClick = (photoPath) => {
    setSelectedPhoto(photoPath);
  };

  if (loading) {
    return <LoadingWheel />
  }

  else {
    return (
        <>
        <div className="level-page">
        <img
            src={selectedPhoto}
            alt="Profile"
            className="profile-pic"
        />
        <h2>Level {user_info.level}</h2>
        <div className="progress-container">
            <div className="progress-bar" style={{ width: `${user_info.percentage}%` }}></div>
        </div>
        <p>{user_info.xp} / {user_info.xp_goal} XP</p>
        </div>

        <div><PhotoGallery level={user_info.level} onPhotoClick={handlePhotoClick}/></div>
        </>
    );
  }
}

export default LevelPage;
