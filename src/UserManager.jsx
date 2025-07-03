import React, { useEffect, useState } from "react";

// Remplace ces URLs par celles de tes endpoints API Gateway
const API_GET_URL =
  "https://ah15paxh5f.execute-api.eu-west-1.amazonaws.com/dev/get";
const API_POST_URL =
  "https://ah15paxh5f.execute-api.eu-west-1.amazonaws.com/dev/post";

export default function UserManager() {
  const [users, setUsers] = useState([]);
  const [form, setForm] = useState({ email: "" });
  const [searchEmail, setSearchEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  // Récupérer l'utilisateur par email
  const fetchUsers = async (email) => {
    setLoading(true);
    setError("");
    try {
      let url = API_GET_URL;
      if (email) {
        url += `?email=${encodeURIComponent(email)}`;
      }
      const res = await fetch(url);
      if (!res.ok) {
        if (res.status === 404) {
          setUsers([]);
          setError("Aucun utilisateur trouvé");
          return;
        }
        throw new Error("Erreur lors de la récupération des utilisateurs");
      }
      const data = await res.json();
      // L'API retourne un objet utilisateur unique, on le met dans un tableau pour l'affichage
      setUsers(data.user ? [data.user] : [data]);
      setError("");
    } catch (err) {
      setError(err.message);
      setUsers([]);
    } finally {
      setLoading(false);
    }
  };

  // Recherche automatique au chargement (optionnel)
  useEffect(() => {
    fetchUsers();
  }, []);

  // Ajouter un utilisateur
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    setLoading(true);
    try {
      const res = await fetch(API_POST_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: form.email }),
      });
      const data = await res.json();
      if (res.ok) {
        setSuccess("Utilisateur ajouté !");
        setForm({ email: "" });
        fetchUsers();
      } else {
        setError(data.message || "Erreur lors de l'ajout");
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Gérer la recherche par email
  const handleSearch = (e) => {
    e.preventDefault();
    fetchUsers(searchEmail);
  };

  return (
    <div style={{ maxWidth: 500, margin: "auto", padding: 20 }}>
      <h2>Gestion des utilisateurs</h2>
      <form onSubmit={handleSubmit} style={{ marginBottom: 20 }}>
        <input
          type="email"
          placeholder="Email"
          value={form.email}
          onChange={(e) => setForm({ email: e.target.value })}
          required
          style={{ marginRight: 10 }}
        />
        <button type="submit" disabled={loading}>
          Ajouter
        </button>
      </form>
      <form onSubmit={handleSearch} style={{ marginBottom: 20 }}>
        <input
          type="email"
          placeholder="Rechercher par email"
          value={searchEmail}
          onChange={(e) => setSearchEmail(e.target.value)}
          style={{ marginRight: 10 }}
        />
        <button type="submit" disabled={loading}>
          Rechercher
        </button>
      </form>
      {error && <div style={{ color: "red" }}>{error}</div>}
      {success && <div style={{ color: "green" }}>{success}</div>}
      <h3>Résultat</h3>
      {loading ? (
        <div>Chargement...</div>
      ) : (
        <ul>
          {users.length === 0 && <li>Aucun utilisateur</li>}
          {users.map((u) => (
            <li key={u.userId}>
              {u.userId} - {u.email}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
