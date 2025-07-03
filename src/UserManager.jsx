import React, { useEffect, useState } from 'react';

const API_GET_URL = '/api/getUser'; // À adapter selon votre configuration API Gateway
const API_POST_URL = '/api/postUser'; // À adapter selon votre configuration API Gateway

export default function UserManager() {
  const [users, setUsers] = useState([]);
  const [form, setForm] = useState({ userId: '', email: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Récupérer la liste des utilisateurs
  const fetchUsers = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await fetch(API_GET_URL);
      if (!res.ok) throw new Error('Erreur lors de la récupération des utilisateurs');
      const data = await res.json();
      setUsers(data.users || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  // Ajouter un utilisateur
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);
    try {
      const res = await fetch(API_POST_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });
      const data = await res.json();
      if (res.ok) {
        setSuccess('Utilisateur ajouté !');
        setForm({ userId: '', email: '' });
        fetchUsers();
      } else {
        setError(data.message || 'Erreur lors de l\'ajout');
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 500, margin: 'auto', padding: 20 }}>
      <h2>Gestion des utilisateurs</h2>
      <form onSubmit={handleSubmit} style={{ marginBottom: 20 }}>
        <input
          type="text"
          placeholder="User ID"
          value={form.userId}
          onChange={e => setForm({ ...form, userId: e.target.value })}
          required
          style={{ marginRight: 10 }}
        />
        <input
          type="email"
          placeholder="Email"
          value={form.email}
          onChange={e => setForm({ ...form, email: e.target.value })}
          required
          style={{ marginRight: 10 }}
        />
        <button type="submit" disabled={loading}>Ajouter</button>
      </form>
      {error && <div style={{ color: 'red' }}>{error}</div>}
      {success && <div style={{ color: 'green' }}>{success}</div>}
      <h3>Liste des utilisateurs</h3>
      {loading ? (
        <div>Chargement...</div>
      ) : (
        <ul>
          {users.length === 0 && <li>Aucun utilisateur</li>}
          {users.map(u => (
            <li key={u.userId}>{u.userId} - {u.email}</li>
          ))}
        </ul>
      )}
    </div>
  );
}
