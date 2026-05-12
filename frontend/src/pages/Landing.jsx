// src/pages/Landing.jsx
import React from "react";
import { Link } from "react-router-dom";
import "../styles/landing.css";
import logo from "../assets/logo.png";
import illustration from "../assets/login-illustration.png";

export default function Landing() {
  return (
    <div className="landing-container">
      <div className="landing-left">
        <img src={logo} alt="Doc2Sign Logo" className="landing-logo" />

        <h1 className="landing-title">Welcome to Doc2Sign</h1>
        <p className="landing-subtitle">
          Upload documents, generate summaries, and translate them into Indian Sign Language.
          Everything in one simple, beautiful interface.
        </p>

        <div className="landing-buttons">
          <Link to="/login" className="btn-primary">Login</Link>
          <Link to="/signup" className="btn-secondary">Create Account</Link>
        </div>
      </div>

      <div className="landing-right">
        <img src={illustration} alt="Illustration" className="landing-illustration" />
      </div>
    </div>
  );
}
