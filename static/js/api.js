const API_BASE_URL = ''; // Use relative paths

console.log('API v1.1.0 loaded');
const API = {
    async request(endpoint, method = 'GET', body = null) {
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
            },
        };

        const token = localStorage.getItem('token');
        if (token) {
            options.headers['Authorization'] = `Bearer ${token}`;
        }

        if (body) {
            options.body = JSON.stringify(body);
        }

        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
            if (response.status === 401) {
                // Token expired or invalid
                localStorage.removeItem('token');
                window.location.reload();
            }
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'API request failed');
            }
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },

    // Auth
    login(username, password) {
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);

        return fetch(`${API_BASE_URL}/token`, {
            method: 'POST',
            body: formData
        }).then(res => res.json());
    },

    // Tournaments
    getTournaments() {
        return this.request('/tournaments/');
    },

    createTournament(data) {
        return this.request('/tournaments/', 'POST', data);
    },

    deleteTournament(id) {
        console.log('API.deleteTournament called with id:', id);
        return this.request(`/tournaments/${id}`, 'DELETE');
    },

    getTournament(id) {
        return this.request(`/tournaments/${id}`);
    },

    generateFixtures(id) {
        return this.request(`/tournaments/${id}/fixtures`, 'POST');
    },

    // Standings
    getStandings(id) {
        return this.request(`/tournaments/${id}/standings`);
    },

    // Teams
    createTeam(data) {
        return this.request('/teams/', 'POST', data);
    },

    // Matches
    updateScore(matchId, scores) {
        return this.request(`/matches/${matchId}/score`, 'POST', scores);
    },

    getRecentMatches() {
        return this.request('/matches/recent');
    },

    getRankings() {
        return this.request('/rankings/players');
    }
};
