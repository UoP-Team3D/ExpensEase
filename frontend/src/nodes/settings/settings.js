import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Settings = () => {
    const navigate = useNavigate();
    const [newPassword, setNewPassword] = useState('');
    const [newEmail, setNewEmail] = useState('');

    const handleChangePassword = async () => {
        const url = 'http://127.0.0.1:5000/api/v1/change_password';
        const body = JSON.stringify({
            new_password: newPassword
        });

        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: body
        });

        const data = await response.json();
        if (response.ok) {
            alert('Password updated successfully');
            setNewPassword('');
        } else {
            alert(data.message || 'Failed to update password');
        }
    };

    const handleChangeEmail = async () => {
        const url = 'http://127.0.0.1:5000/api/v1/change_email';
        const body = JSON.stringify({ new_email: newEmail });

        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: body
        });

        const data = await response.json();
        if (response.ok) {
            alert('Email updated successfully');
            setNewEmail('');
        } else {
            alert(data.message || 'Failed to update email');
        }
    };

    const handleDeleteAccount = async () => {
        if (!window.confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
            return;
        }

        const url = 'http://127.0.0.1:5000/api/v1/delete_account';
        const response = await fetch(url, {
            method: 'DELETE'
        });

        const data = await response.json();
        if (response.ok) {
            alert('Account deleted successfully');
            navigate('/login'); // Redirect to login after account deletion
        } else {
            alert(data.message || 'Failed to delete account');
        }
    };

    return (
        <div className="settings">
            <h1>Account Settings</h1>
            <input type="password" placeholder="New Password" value={newPassword} onChange={e => setNewPassword(e.target.value)} />
            <button onClick={handleChangePassword}>Change Password</button>
            <input type="email" placeholder="New Email" value={newEmail} onChange={e => setNewEmail(e.target.value)} />
            <button onClick={handleChangeEmail}>Change Email</button>
            <button onClick={handleDeleteAccount}>Delete Account</button>
        </div>
    );
};

export default Settings;
