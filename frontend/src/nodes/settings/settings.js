import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './../general.css';

const Settings = () => {
    const navigate = useNavigate();
    const [showPasswordForm, setShowPasswordForm] = useState(false);
    const [currentPassword, setCurrentPassword] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [showCurrentPassword, setShowCurrentPassword] = useState(false);
    const [showNewPassword, setShowNewPassword] = useState(false);
    const [showEmailForm, setShowEmailForm] = useState(false);
    const [currentEmail, setCurrentEmail] = useState('');
    const [newEmail, setNewEmail] = useState('');

    const handleChangePassword = async () => {
        const url = 'http://127.0.0.1:5000/api/v1/change_password';
        
        const body = JSON.stringify({
            password: currentPassword,
            new_password: newPassword
        });

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
                body: body
            });

            const data = await response.json();
            if (response.ok) {
                alert('Password updated successfully');
                setCurrentPassword('');
                setNewPassword('');
                setShowPasswordForm(false);
            } else {
                alert(data.message || 'Failed to update password');
            }
        } catch (error) {
            alert('Network error, please try again later.');
        }
    };

    const handleChangeEmail = async () => {
        const url = 'http://127.0.0.1:5000/api/v1/change_email';
        const body = JSON.stringify({
            current_email: currentEmail,
            new_email: newEmail
        });

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
                body: body
            });

            const data = await response.json();
            if (response.ok) {
                alert('Email updated successfully');
                setCurrentEmail('');
                setNewEmail('');
                setShowEmailForm(false);
            } else {
                alert(data.message || 'Failed to update email');
            }
        } catch (error) {
            alert('Network error, please try again later.');
        }
    };

    const handleDeleteAccount = async () => {
        const url = 'http://127.0.0.1:5000/api/v1/delete_account';
        try {
            const response = await fetch(url, {
                method: 'DELETE',
                credentials: 'include',
            });

            const data = await response.json();
            if (response.ok) {
                alert('Account deleted successfully');
                navigate('/login');
            } else {
                alert(data.message || 'Failed to delete account');
            }
        } catch (error) {
            alert('Server error, please try again later.');
        }
    };

    const cancelPasswordChange = () => {
        setShowPasswordForm(false);
        setCurrentPassword('');
        setNewPassword('');
    };

    const cancelEmailChange = () => {
        setShowEmailForm(false);
        setCurrentEmail('');
        setNewEmail('');
    };

    return (
        <div className="settings-container">
            <div className="settings-header">
                <i className="fas fa-cog settings-icon"></i>
                <h1 className="settings-title">Account Settings</h1>
            </div>
            <div className="settings-content">
                <div className="settings-section">
                    <h2 className="section-title">Change Password</h2>
                    {showPasswordForm ? (
                        <div className="password-form">
                            <div className="password-input">
                                <input
                                    type={showCurrentPassword ? 'text' : 'password'}
                                    placeholder="Current Password"
                                    value={currentPassword}
                                    onChange={(e) => setCurrentPassword(e.target.value)}
                                    className="input-field settings-input"
                                />
                                <i
                                    className={`fas fa-eye${showCurrentPassword ? '-slash' : ''} password-toggle`}
                                    onClick={() => setShowCurrentPassword(!showCurrentPassword)}
                                ></i>
                            </div>
                            <div className="password-input">
                                <input
                                    type={showNewPassword ? 'text' : 'password'}
                                    placeholder="New Password"
                                    value={newPassword}
                                    onChange={(e) => setNewPassword(e.target.value)}
                                    className="input-field settings-input"
                                />
                                <i
                                    className={`fas fa-eye${showNewPassword ? '-slash' : ''} password-toggle`}
                                    onClick={() => setShowNewPassword(!showNewPassword)}
                                ></i>
                            </div>
                            <div className="form-actions">
                                <button onClick={handleChangePassword} className="confirm-btn">
                                    Confirm Password Change
                                </button>
                                <button onClick={cancelPasswordChange} className="cancel-btn">
                                    Cancel
                                </button>
                            </div>
                        </div>
                    ) : (
                        <button onClick={() => setShowPasswordForm(true)} className="change-btn">
                            Change Password
                        </button>
                    )}
                </div>
                <div className="settings-section">
                    <h2 className="section-title">Change Email</h2>
                    {showEmailForm ? (
                        <div className="email-form">
                            <input
                                type="email"
                                placeholder="Current Email"
                                value={currentEmail}
                                onChange={(e) => setCurrentEmail(e.target.value)}
                                className="input-field settings-input"
                            />
                            <input
                                type="email"
                                placeholder="New Email"
                                value={newEmail}
                                onChange={(e) => setNewEmail(e.target.value)}
                                className="input-field settings-input"
                            />
                            <div className="form-actions">
                                <button onClick={handleChangeEmail} className="confirm-btn">
                                    Confirm Email Change
                                </button>
                                <button onClick={cancelEmailChange} className="cancel-btn">
                                    Cancel
                                </button>
                            </div>
                        </div>
                    ) : (
                        <button onClick={() => setShowEmailForm(true)} className="change-btn">
                            Change Email
                        </button>
                    )}
                </div>
                <div className="settings-section">
                    <h2 className="section-title">Delete Account</h2>
                    <button
                        onClick={() => {
                            if (window.confirm('Are you sure you want to delete your account?')) handleDeleteAccount();
                        }}
                        className="delete-account-btn"
                    >
                        Delete Account
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Settings;