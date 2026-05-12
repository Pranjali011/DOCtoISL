import React from "react";
import { Link } from "react-router-dom";
import "../styles/navbar.css";

import logo from "../assets/logo.png";
import userIcon from "../assets/user-icon.png";
import sunIcon from "../assets/theme-light.png";
import moonIcon from "../assets/theme-dark.png";

import { useTheme } from "../context/ThemeContext";

export default function Navbar() {
  const { theme, toggleTheme } = useTheme();

  return (
    <nav className="nav">
      {/* LEFT SIDE */}
      <div className="nav-left">
        <img src={logo} alt="logo" className="nav-logo" />
        <h2 className="nav-title">Doc2Sign</h2>

        <Link to="/home" className="nav-link">Home</Link>
        <Link to="/history" className="nav-link">History</Link>
        <Link to="/documents" className="nav-link">Documents</Link>
        <Link to="/profile" className="nav-link">Profile</Link>
      </div>

      {/* RIGHT SIDE */}
      <div className="nav-right">

        {/* THEME TOGGLE */}
        <img
          src={theme === "light" ? moonIcon : sunIcon}
          alt="theme toggle"
          className="nav-icon"
          onClick={toggleTheme}
        />

        {/* PROFILE ICON */}
        <Link to="/profile">
          <img
            src={userIcon}
            alt="user"
            className="nav-user-icon"
          />
        </Link>

      </div>
    </nav>
  );
}
