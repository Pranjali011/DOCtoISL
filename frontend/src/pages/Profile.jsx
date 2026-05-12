import React, { useEffect, useState } from "react";
import "../styles/profile.css";
import userIcon from "../assets/user-icon.png";

import { getProfile, updateProfile } from "../api/profile";

export default function Profile() {
  const storedUser = JSON.parse(localStorage.getItem("user"));
  const userId = storedUser?.id;
  const token = storedUser?.token;

  const [profile, setProfile] = useState({
    name: "",
    email: "",
    phone: "",
  });

  const [editing, setEditing] = useState(false);
  const [status, setStatus] = useState("");

  useEffect(() => {
    async function fetchProfile() {
      try {
        const data = await getProfile(userId, token);

        setProfile({
          name: data.name || "",
          email: data.email || "",
          phone: data.phone || "",
        });
      } catch (error) {
        console.error("Failed to load profile:", error);
        setStatus("Failed to load profile");
      }
    }

    if (userId) fetchProfile();
  }, [userId, token]);

  const handleChange = (e) => {
    setProfile({ ...profile, [e.target.name]: e.target.value });
  };

  const handleSave = async () => {
    try {
      setStatus("Saving...");
      await updateProfile(userId, profile, token);
      setStatus("Profile updated successfully!");
      setEditing(false);
    } catch (error) {
      console.error(error);
      setStatus("Failed to update profile");
    }
  };

  return (
    <div className="profile-container">
      <div className="profile-box">
        <h2 className="profile-heading">My Profile</h2>

        <div className="profile-top">
          <img src={userIcon} alt="User" className="profile-avatar" />
        </div>

        <div className="profile-grid">
          <div className="profile-field">
            <label>Name</label>
            <input
              type="text"
              name="name"
              disabled={!editing}
              value={profile.name}
              onChange={handleChange}
            />
          </div>

          <div className="profile-field">
            <label>Email</label>
            <input
              type="email"
              name="email"
              disabled={!editing}
              value={profile.email}
              onChange={handleChange}
            />
          </div>

          <div className="profile-field">
            <label>Phone</label>
            <input
              type="text"
              name="phone"
              disabled={!editing}
              value={profile.phone}
              onChange={handleChange}
            />
          </div>
        </div>

        {status && <p className="profile-status">{status}</p>}

        {!editing ? (
          <button className="edit-btn" onClick={() => setEditing(true)}>
            Edit Profile
          </button>
        ) : (
          <button className="save-btn" onClick={handleSave}>
            Save Changes
          </button>
        )}
      </div>
    </div>
  );
}
