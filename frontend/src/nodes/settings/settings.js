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

    return (
        <div className="settings">
            <div className="settings-header">
                <i className="fas fa-cog settings-icon"></i>Account Settings
            </div>
            {showPasswordForm ? (
                <>
                    <div className="password-input">
                        <input
                            type={showCurrentPassword ? 'text' : 'password'}
                            placeholder="Current Password"
                            value={currentPassword}
                            onChange={(e) => setCurrentPassword(e.target.value)}
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
                        />
                        <i
                            className={`fas fa-eye${showNewPassword ? '-slash' : ''} password-toggle`}
                            onClick={() => setShowNewPassword(!showNewPassword)}
                        ></i>
                    </div>
                    <button onClick={handleChangePassword} className="confirm-btn">
                        Confirm Password Change
                    </button>
                </>
            ) : (
                <button onClick={() => setShowPasswordForm(true)} className="change-btn">
                    Change Password
                </button>
            )}
            {showEmailForm ? (
                <>
                    <input
                        type="email"
                        placeholder="Current Email"
                        value={currentEmail}
                        onChange={(e) => setCurrentEmail(e.target.value)}
                    />
                    <input
                        type="email"
                        placeholder="New Email"
                        value={newEmail}
                        onChange={(e) => setNewEmail(e.target.value)}
                    />
                    <button onClick={handleChangeEmail} className="confirm-btn">
                        Confirm Email Change
                    </button>
                </>
            ) : (
                <button onClick={() => setShowEmailForm(true)} className="change-btn">
                    Change Email
                </button>
            )}
            <button
                onClick={() => {
                    if (window.confirm('Are you sure you want to delete your account?')) handleDeleteAccount();
                }}
                className="delete-account-btn"
            >
                Delete Account
            </button>
        </div>
    );
};

export default Settings;